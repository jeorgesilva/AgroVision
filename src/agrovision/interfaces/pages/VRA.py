import sys
from pathlib import Path

_STREAMLIT_DIR = Path(__file__).resolve().parents[1]
if str(_STREAMLIT_DIR) not in sys.path:
    sys.path.insert(0, str(_STREAMLIT_DIR))

from auth import require_login  # noqa: E402

require_login()

import streamlit as st

# -----------------------------
# Page Config & Logic
# -----------------------------
st.set_page_config(page_title="VRA Map & Reports", page_icon="🗺️", layout="wide")

import sys
import os
import json
import zipfile
import io
from pathlib import Path
import rasterio
import numpy as np
import folium
from folium import raster_layers
from streamlit_folium import st_folium
import geopandas as gpd
from pyproj import Transformer
import warnings
import glob

warnings.filterwarnings("ignore", category=UserWarning, module="geopandas")

# Resolve project root the same way Detection.py does so VRA.py works in any
# environment without hardcoded paths.
_PROJECT_ROOT = Path(__file__).resolve().parents[4]
_SRC_DIR = _PROJECT_ROOT / "src"
try:
    import agrovision  # noqa: F401
except ImportError:
    if _SRC_DIR.is_dir():
        sys.path.insert(0, str(_SRC_DIR))

from agrovision.core.report_gen import PDF_FILENAME

# -----------------------------
# Lógica de Sessão e Caminhos
# -----------------------------
def get_latest_session_paths():
    """Busca a sessão mais recente no Drive de forma exaustiva."""
    base_dir = "/content/drive/MyDrive/Agroview/AgroVision/src/agrovision/data/sessions"
    
    if not os.path.exists(base_dir):
        return None, None, None, None

    sessions = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    if not sessions:
        return None, None, None, None

    # A mais recente
    latest_session = max(sessions, key=os.path.getmtime)
    
    gold_dir = os.path.join(latest_session, "gold")
    bronze_dir = os.path.join(latest_session, "bronze")
    
    vra_path = os.path.join(gold_dir, "vra.geojson")
    raw_path = os.path.join(gold_dir, "raw_detections.geojson")
    shp_dir = os.path.join(gold_dir, "shapefile")
    
    ortho_path = None
    if os.path.exists(bronze_dir):
        files = [f for f in os.listdir(bronze_dir) if f.lower().endswith(('.tif', '.tiff', '.ecw'))]
        if files:
            ortho_path = os.path.join(bronze_dir, files[0])

    if not os.path.exists(vra_path):
        return None, None, None, None

    return vra_path, ortho_path, shp_dir, raw_path

# -----------------------------
# Lógica de Imagem HD (CORRIGIDA)
# -----------------------------
def get_ortho_bounds(tif_path):
    with rasterio.open(tif_path) as src:
        bounds = src.bounds
        crs = src.crs
    transformer = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
    min_lon, min_lat = transformer.transform(bounds.left, bounds.bottom)
    max_lon, max_lat = transformer.transform(bounds.right, bounds.top)
    return [[min_lat, min_lon], [max_lat, max_lon]]

def get_hd_image(tif_path, max_dim=2048):
    """Lê a imagem garantindo alta qualidade (HD) sem rebentar o navegador."""
    with rasterio.open(tif_path) as src:
        # Calcula a escala para não ultrapassar max_dim (ex: 2048px)
        scale = min(max_dim / src.width, max_dim / src.height)
        scale = min(scale, 1.0) # Nunca aumenta, só diminui se necessário
        
        new_height = int(src.height * scale)
        new_width = int(src.width * scale)
        
        data = src.read(
            out_shape=(src.count, new_height, new_width),
            resampling=rasterio.enums.Resampling.bilinear
        )
        img_data = data[:3, :, :].transpose(1, 2, 0)
        
        if img_data.dtype != np.uint8:
            min_val, max_val = np.nanmin(img_data), np.nanmax(img_data)
            if max_val > min_val:
                img_data = ((img_data - min_val) / (max_val - min_val) * 255)
            img_data = img_data.astype(np.uint8)
            
        return img_data

def create_shapefile_zip(gdf, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    shp_path = os.path.join(output_dir, "vra_map.shp")
    gdf_shp = gdf.copy()
    if "weed_count" in gdf_shp.columns: gdf_shp = gdf_shp.rename(columns={"weed_count": "w_count"})
    if "spray_action" in gdf_shp.columns: gdf_shp = gdf_shp.rename(columns={"spray_action": "spray"})
    if "rate_l_ha" in gdf_shp.columns: gdf_shp = gdf_shp.rename(columns={"rate_l_ha": "rate"})
    
    gdf_shp.to_file(shp_path, driver="ESRI Shapefile")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename in os.listdir(output_dir):
            if filename.startswith("vra_map"):
                zip_file.write(os.path.join(output_dir, filename), filename)
    return zip_buffer.getvalue()


# -----------------------------
# INTERFACE PRINCIPAL
# -----------------------------
st.title("🗺️ Mapa de Prescrição (VRA) & Relatórios")

VRA_PATH = st.session_state.get("vra_path")
ORTHO_PATH = st.session_state.get("ortho_path")
SHP_DIR = st.session_state.get("shp_dir")
RAW_PATH = None

# Fallback: Se a sessão for perdida (Refresh da página), tenta ler do disco
if not VRA_PATH or not os.path.exists(VRA_PATH):
    f_vra, f_ortho, f_shp, f_raw = get_latest_session_paths()
    if f_vra:
        VRA_PATH, ORTHO_PATH, SHP_DIR, RAW_PATH = f_vra, f_ortho, f_shp, f_raw
    else:
        st.warning("⚠️ Nenhum mapa VRA encontrado. Por favor, processe um ortomosaico primeiro.")
        st.stop()
else:
    RAW_PATH = os.path.join(os.path.dirname(VRA_PATH), "raw_detections.geojson")

try:
    raw_gdf = gpd.read_file(VRA_PATH)
    
    # Métricas Superiores
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Células (Grelha)", len(raw_gdf))
    
    if "spray_action" in raw_gdf.columns:
        cells_to_spray = raw_gdf[raw_gdf["spray_action"] == 1].shape[0]
        col3.metric("Células a Pulverizar", cells_to_spray)
    
    if "weed_count" in raw_gdf.columns:
        col4.metric("Total de Plantas Detetadas", raw_gdf["weed_count"].sum())

    st.divider()

    if raw_gdf.empty:
        st.success("🎉 O campo está limpo! Não foram detetadas infestações.")
    else:
        vra_gdf_vis = raw_gdf.to_crs("EPSG:4326")
        center_lat, center_lon = vra_gdf_vis.centroid.y.mean(), vra_gdf_vis.centroid.x.mean()

        m = folium.Map(location=[center_lat, center_lon], zoom_start=20, max_zoom=24, tiles="CartoDB positron")

        # 1. Ortomosaico (Agora em Alta Qualidade)
        if ORTHO_PATH and os.path.exists(ORTHO_PATH):
            img_data = get_hd_image(ORTHO_PATH, max_dim=2500) # Alta Resolução
            bounds = get_ortho_bounds(ORTHO_PATH)
            raster_layers.ImageOverlay(image=img_data, bounds=bounds, opacity=0.8, name="Ortomosaico HD").add_to(m)

        # 2. Grelha VRA (Mapa de Calor)
        def style_function(feature):
            count = feature['properties'].get('weed_count', 0)
            if count >= 3:
                return {'fillColor': '#8B0000', 'color': '#660000', 'weight': 2, 'fillOpacity': 0.6}
            elif count == 2:
                return {'fillColor': '#FF4500', 'color': '#CC3300', 'weight': 2, 'fillOpacity': 0.5}
            elif count == 1:
                return {'fillColor': '#FFD700', 'color': '#B8860B', 'weight': 2, 'fillOpacity': 0.4}
            else:
                return {'fillColor': '#00FF00', 'color': '#00CC00', 'weight': 1, 'fillOpacity': 0.1}

        folium.GeoJson(
            data=json.loads(vra_gdf_vis.to_json()),
            name="Grelha de Prescrição VRA",
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(fields=["weed_count", "rate_l_ha"], aliases=["Plantas:", "Taxa (L/ha):"])
        ).add_to(m)

        # 3. Deteções Exatas (O Raio-X)
        if RAW_PATH and os.path.exists(RAW_PATH):
            raw_det_gdf = gpd.read_file(RAW_PATH).to_crs("EPSG:4326")
            def raw_style(feature):
                return {'fillColor': '#0000FF', 'color': '#0000FF', 'weight': 1, 'fillOpacity': 0.3}
                
            folium.GeoJson(
                data=json.loads(raw_det_gdf.to_json()),
                name="Deteções Exatas (Raio-X)",
                style_function=raw_style,
                tooltip=folium.GeoJsonTooltip(fields=["class", "confidence"], aliases=["Classe:", "Confiança:"])
            ).add_to(m)

        folium.LayerControl().add_to(m)
        st_folium(m, width=1200, height=700) # Mapa maior no ecrã

        # -----------------------------
        # ZONA DE DOWNLOADS (O Produto Final)
        # -----------------------------
        st.divider()
        st.markdown("### 📥 Exportação de Resultados")
        
        # 3 Colunas para os botões de download ficarem lado a lado
        c1, c2, c3 = st.columns(3)
        
        # Botão 1: SHP Zipado (Para o Drone)
        zip_data = create_shapefile_zip(raw_gdf, SHP_DIR)
        c1.download_button("🚜 Baixar Shapefile (.zip)", zip_data, "Mapa_VRA_AgroVision.zip", "application/zip", use_container_width=True)

        # Botão 2: GeoJSON Original (Para Programadores/QGIS)
        with open(VRA_PATH, "rb") as f:
            c2.download_button("🌐 Baixar GeoJSON Original", f, "vra_raw.geojson", "application/geo+json", use_container_width=True)

        # Botão 3: O Relatório PDF Comercial
        report_pdf_path = os.path.join(os.path.dirname(VRA_PATH), "reports", PDF_FILENAME)
        if os.path.exists(report_pdf_path):
            with open(report_pdf_path, "rb") as pdf_file:
                c3.download_button("📄 Baixar Relatório Técnico (PDF)", pdf_file, "Relatorio_AgroVision_Cliente.pdf", "application/pdf", type="primary", use_container_width=True)
        else:
            c3.error("Relatório PDF não encontrado.")

except Exception as e:
    st.error(f"Erro ao processar o mapa: {e}")