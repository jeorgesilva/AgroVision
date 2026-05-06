import logging
import geopandas as gpd
from shapely import BufferCapStyle
from shapely.geometry import box
import pandas as pd
import numpy as np
import rasterio

logger = logging.getLogger(__name__)

def load_transform(raster_path):
    """
    Loads the affine transform and CRS from a raster file.
    This is used to convert pixel coordinates into real-world coordinates.
    """
    with rasterio.open(raster_path) as src:
        return src.transform, src.crs

def apply_transform(coords, transform):
    """
    Applies affine transform to pixel coordinates.
    coords is expected to be (x, y) in pixel space.
    rasterio transform * (col, row) -> (x, y) in real-world coordinates.
    """
    x, y = coords
    return transform * (x, y)

def create_vra_grid(weeds_gdf: gpd.GeoDataFrame, grid_size: float = 10.0) -> gpd.GeoDataFrame:
    """
    Gera quadrados perfeitos de aplicação (ex: 10x10m) centrados nas deteções.
    Funde zonas que se sobrepõem (intersectam) para não pulverizar duas vezes o mesmo sítio.
    """
    if weeds_gdf.empty:
         return gpd.GeoDataFrame(columns=["geometry", "weed_count", "spray_action"], crs=weeds_gdf.crs)

    original_crs = weeds_gdf.crs

    # 1. Reprojetar para um CRS métrico local para que "10.0" signifique 10 metros reais
    logger.info("Reprojecting to local metric CRS...")
    if original_crs and original_crs.is_geographic:
        projected_crs = weeds_gdf.estimate_utm_crs()
        weeds_projected = weeds_gdf.to_crs(projected_crs)
    else:
        projected_crs = original_crs
        weeds_projected = weeds_gdf.copy()

    # 2. Obter o centro exato de cada "caixa" detetada
    centroids = weeds_projected.geometry.centroid

    # 3. A NOVA LÓGICA (Buffer Quadrado em vez de Snapping)
    # Criamos um "raio" que é metade do tamanho da grelha (ex: 5m para uma grelha de 10m)
    radius = grid_size / 2.0
    
    # Fazemos um buffer retangular em torno do centro exato da planta
    squared_buffers = centroids.buffer(radius, cap_style=BufferCapStyle.square)

    # 4. Unir os quadrados que se sobrepõem (Para não haver duplicação de doses)
    from shapely.ops import unary_union
    merged_zones = unary_union(squared_buffers)

    # Converter de volta para lista de polígonos individuais
    if merged_zones.geom_type == 'Polygon':
        final_polygons = [merged_zones]
    else:
         final_polygons = list(merged_zones.geoms)

    # 5. Construir o GeoDataFrame final com os novos quadrados perfeitos
    grid_gdf = gpd.GeoDataFrame(geometry=final_polygons, crs=projected_crs)

    # 6. Calcular quantas plantas caíram dentro de cada polígono fundido
    # Fazemos um Spatial Join com as deteções originais para contar as ervas em cada bloco
    weeds_projected['dummy'] = 1
    join_gdf = gpd.sjoin(weeds_projected, grid_gdf, how="inner", predicate="within")
    
    # Contagem agrupada pelo índice do polígono final
    counts = join_gdf.groupby('index_right')['dummy'].sum()
    
    # Mapear as contagens de volta para o GeoDataFrame da grelha
    grid_gdf['weed_count'] = grid_gdf.index.map(counts).fillna(0).astype(int)

    # 7. Adicionar lógica de aplicação
    grid_gdf['spray_action'] = grid_gdf['weed_count'].apply(lambda c: 1 if c > 0 else 0)
    grid_gdf['rate_l_ha'] = grid_gdf['spray_action'] * 150.0  # Ex: 150 Litros por Hectare

    # 8. Voltar para o CRS original (GPS / WGS84)
    logger.info("Reprojecting grid back to source CRS...")
    final_grid = grid_gdf.to_crs(original_crs)

    return final_grid