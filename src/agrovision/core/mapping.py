# src/agrovision/core/mapping.py
import json
import traceback
import geopandas as gpd
from shapely.geometry import box
from pathlib import Path
import rasterio
from rasterio.transform import Affine

# Imports internos do projeto
from agrovision.core.geoprocess import create_vra_grid
from agrovision.core.analytics import generate_report_material
from agrovision.core.report_gen import create_pdf_report, PDF_FILENAME

def create_vra_map(detections_path, raster_path, output_path, **kwargs):
    """
    Transforma detecções de pixels em mapas geográficos (VRA),
    gera analytics visuais e o relatório PDF final.
    """
    detections_path = Path(detections_path)
    if not detections_path.exists(): 
        raise FileNotFoundError(f"Ficheiro de detecções não encontrado: {detections_path}")

    # 1. Carregar as detecções do JSON (Camada Silver)
    with open(detections_path, "r", encoding="utf-8") as f: 
        all_detections = json.load(f)
        
    # 2. Ler o CRS e o transform global do ortomosaico numa única abertura.
    #    O transform global serve de fallback para fatias sem transform_matrix
    #    (modo diretório de imagens). Abrir o raster dentro do loop seria
    #    um open/close por entrada — potencialmente milhares de vezes.
    with rasterio.open(raster_path) as src:
        raster_crs = src.crs
        fallback_transform = src.transform

    geometries = []
    attributes = []

    print("📍 A converter píxeis em coordenadas geográficas reais...")

    for entry in all_detections:
        image_id = entry.get("image_path")
        meta = entry.get("metadata", {})

        if "transform_matrix" in meta:
            transform_fatia = Affine(*meta["transform_matrix"])
        else:
            transform_fatia = fallback_transform

        for det in entry.get("detections", []):
            x1, y1, x2, y2 = det["bbox"]
            
            # Converter coordenadas de pixel para mundo real (UTM/GPS)
            x1_real, y1_real = transform_fatia * (x1, y1)
            x2_real, y2_real = transform_fatia * (x2, y2)
            
            geometries.append(box(
                min(x1_real, x2_real), min(y1_real, y2_real), 
                max(x1_real, x2_real), max(y1_real, y2_real)
            ))
            
            attributes.append({
                "image_source": image_id,
                "class": det.get("class_name", "Unknown"),
                "confidence": det.get("confidence")
            })

    # Caso não haja detecções, criamos um mapa vazio seguro para a Interface não dar erro
    if not geometries:
        print("⚠️ Nenhuma planta detetada. A gerar mapa VRA limpo...")
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Cria GeoJSONs vazios mas com a estrutura correta
        empty_gdf = gpd.GeoDataFrame(columns=["geometry", "weed_count", "spray_action", "rate_l_ha"], crs=raster_crs)
        empty_gdf.to_file(output_path)
        
        raw_path = output_path.parent / "raw_detections.geojson"
        empty_gdf.to_file(raw_path)
        
        print(f"✅ Mapa VRA Vazio guardado em: {output_path}")
        return

    # 3. Criar o GeoDataFrame com as caixas exatas (Camada de "Raio-X")
    weeds_gdf = gpd.GeoDataFrame(attributes, geometry=geometries, crs=raster_crs)
    
    # Salvar as detecções exatas para visualização no mapa interativo
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    raw_path = output_path.parent / "raw_detections.geojson"
    weeds_gdf.to_file(raw_path)
    print(f"🎯 Posições exatas guardadas em: {raw_path}")
    
    # 4. Gerar a Grelha Regular de Aplicação (Grid VRA)
    # Aqui usamos a nova lógica de quadrados centrados na planta
    tamanho_grelha = kwargs.get('grid_size', 10.0) 
    print(f"🚜 A gerar grelha de aplicação em blocos de {tamanho_grelha}x{tamanho_grelha}m...")
    
    zones_gdf = create_vra_grid(weeds_gdf, grid_size=tamanho_grelha)
    
    # 5. Guardar o ficheiro GeoJSON da Grelha (Camada Gold)
    zones_gdf.to_file(output_path)
    print(f"✅ Mapa VRA gerado com sucesso em: {output_path}")

    # ---------------------------------------------------------
    # 6. ANALYTICS: Geração de Gráficos e Imagens para o Relatório
    # ---------------------------------------------------------
    print("📊 A processar estatísticas e gráficos de economia...")
    report_dir = output_path.parent / "reports"
    
    # Gera os PNGs e calcula as métricas finais
    metrics = generate_report_material(zones_gdf, raster_path, str(report_dir))

    # Guardar as métricas em JSON para persistência
    with open(report_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    # ---------------------------------------------------------
    # 7. RELATÓRIO: Geração do PDF Final Profissional
    # ---------------------------------------------------------
    print("📄 A compilar o relatório técnico em PDF...")
    try:
        nome_cliente = kwargs.get("client_name", "Sul Pará Drones")
        pdf_path = create_pdf_report(str(report_dir), client_name=nome_cliente)
        print(f"🏆 Relatório PDF finalizado: {pdf_path}")
    except Exception as e:
        # Log the full traceback so the root cause is visible in server logs.
        # The VRA map itself was already saved, so the pipeline is not aborted.
        print(f"⚠️ Erro ao gerar o PDF — o mapa VRA foi salvo normalmente.\n"
              f"{traceback.format_exc()}")