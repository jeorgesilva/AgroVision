# src/agrovision/core/geoprocess.py
import geopandas as gpd
from shapely.geometry import box


def create_grid(gdf: gpd.GeoDataFrame, grid_size: int) -> gpd.GeoDataFrame:
    """Creates a grid over a GeoDataFrame."""
    xmin, ymin, xmax, ymax = gdf.total_bounds
    grid_cells = []
    for x in range(int(xmin), int(xmax), grid_size):
        for y in range(int(ymin), int(ymax), grid_size):
            grid_cells.append(box(x, y, x + grid_size, y + grid_size))
    return gpd.GeoDataFrame(grid_cells, columns=["geometry"], crs=gdf.crs)


def calculate_weed_density(grid: gpd.GeoDataFrame, weeds: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Calculates weed density per grid cell."""
    grid["weed_density"] = grid.geometry.apply(
        lambda cell: weeds.intersection(cell).area.sum() / cell.area
    )
    return grid
