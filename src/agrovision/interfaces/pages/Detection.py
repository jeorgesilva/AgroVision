import sys
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# environment (local, Docker, cloud VM) without hardcoded paths.
#   src/agrovision/interfaces/pages/Detection.py
#   └─ parents[0] = pages/
#   └─ parents[1] = interfaces/
#   └─ parents[2] = agrovision/
#   └─ parents[3] = src/
# #   └─ parents[4] = <project root>
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parents[4]
_STREAMLIT_DIR = Path(__file__).resolve().parents[1]
_SRC_DIR = _PROJECT_ROOT / "src"
_DATA_DIR = _PROJECT_ROOT / "data"
_MODEL_PATH = _PROJECT_ROOT / "checkpoint_emergencia_v12.pt"

# Add src/ to the path only when the package is not already importable
# (i.e. not installed via pip install -e .). Keeps the dev workflow simple.
try:
    import agrovision  # noqa: F401
except ImportError:
    if _SRC_DIR.is_dir():
        sys.path.insert(0, str(_SRC_DIR))

if str(_STREAMLIT_DIR) not in sys.path:
    sys.path.insert(0, str(_STREAMLIT_DIR))

from auth import require_login  # noqa: E402

require_login()

import streamlit as st
import numpy as np
from PIL import Image
import rasterio
from rasterio.plot import reshape_as_image

from agrovision.data.pre_processing import convert_ecw_to_cog
from agrovision.models.yolo import WeedDetector
from agrovision.pipelines.detect_weeds import run_detection_pipeline
from agrovision.pipelines.vra_mapping import run_vra_mapping_pipeline
from agrovision.utils.session_manager import SessionManager

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AgroVision Detection", page_icon="🌿", layout="wide")

# ---------------------------------------------------------------------------
# SEC-01: PIL decompression-bomb protection.
# The global None override was removed from yolo.py; here we also keep the
# default Pillow limit (or the value set in yolo.py) rather than disabling it.
# The preview helper below falls back to rasterio for files that exceed the
# PIL limit, so large GeoTIFFs are still rendered correctly.
# ---------------------------------------------------------------------------


def _preview_image(image_path: str) -> Image.Image:
    """Returns a downsampled RGB preview safe for Streamlit display."""
    try:
        return Image.open(image_path).convert("RGB")
    except Exception:
        with rasterio.open(image_path) as src:
            data = src.read(out_shape=(src.count, 512, 512))
            img_array = reshape_as_image(data[:3, :, :])
            return Image.fromarray(img_array.astype("uint8"))


# ---------------------------------------------------------------------------
# PERF-03: Cache the YOLO model across Streamlit reruns.
# @st.cache_resource keeps a single model instance in memory for the lifetime
# of the server process. Without this, every button click reloads hundreds of
# MB of weights from disk.
# ---------------------------------------------------------------------------
@st.cache_resource
def _load_detector(model_path: str) -> WeedDetector:
    return WeedDetector(model_path)


# ---------------------------------------------------------------------------
# Session manager — sessions stored under <project_root>/data/sessions/
# ---------------------------------------------------------------------------
session_mgr = SessionManager(str(_DATA_DIR))

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.title("🌿 AgroVision Detection")

with st.sidebar:
    st.header("⚙️ Configurações")
    grid_size = st.number_input("Tamanho da Grelha (m)", min_value=1.0, value=10.0)
    if st.button("🔄 Reiniciar Sessão"):
        SessionManager.clear_st_session()
        st.rerun()

col_up, col_loc = st.columns(2)

with col_up:
    uploaded_file = st.file_uploader(
        "Upload Ortomosaico (< 200 MB)", type=["tif", "tiff", "ecw"]
    )

with col_loc:
    local_path_input = st.text_input(
        "Caminho local (para arquivos > 200 MB):",
        placeholder="/home/user/fazenda/mapa_20gb.tif",
    )

input_source = uploaded_file if uploaded_file else local_path_input

if input_source:
    source_name = uploaded_file.name if uploaded_file else os.path.basename(local_path_input)

    if (
        "current_session" not in st.session_state
        or st.session_state.get("last_file") != source_name
    ):
        session = session_mgr.create_session(prefix="job")
        st.session_state["current_session"] = session
        st.session_state["last_file"] = source_name

        if uploaded_file:
            bronze_path = os.path.join(session["paths"]["bronze"], uploaded_file.name)
            with open(bronze_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("🔄 Convertendo arquivo enviado..."):
                proc_path = convert_ecw_to_cog(bronze_path)
                st.session_state["current_ortho_path"] = proc_path
        else:
            if os.path.exists(local_path_input):
                with st.spinner("🔄 Analisando arquivo (convertendo ECW → COG se necessário)..."):
                    nome_tif = Path(local_path_input).with_suffix(".tif").name
                    destino_bronze = os.path.join(session["paths"]["bronze"], nome_tif)
                    proc_path = convert_ecw_to_cog(local_path_input, output_path=destino_bronze)
                    st.session_state["current_ortho_path"] = proc_path
                st.success("✅ Arquivo processado e vinculado com sucesso!")
            else:
                st.error("❌ Caminho não encontrado.")
                st.stop()

    session = st.session_state["current_session"]
    image_path = st.session_state["current_ortho_path"]

    with st.expander("👁️ Visualizar Ortomosaico", expanded=True):
        st.image(
            _preview_image(image_path),
            caption="Preview Web — a IA utilizará a resolução nativa.",
            use_column_width=True,
        )

    if st.button("🚀 Iniciar Processamento Inteligente", type="primary", use_container_width=True):
        if not _MODEL_PATH.exists():
            st.error(
                f"Modelo YOLO não encontrado em `{_MODEL_PATH}`. "
                "Coloque o arquivo de pesos na raiz do projeto."
            )
            st.stop()

        status = st.status("⚙️ AgroVision Engine em execução...", expanded=True)

        try:
            # PERF-03: model loaded once and reused across reruns via cache
            detector = _load_detector(str(_MODEL_PATH))

            status.write("🔍 [Silver] Detectando com YOLOv12 (fatiamento ativo)...")
            run_detection_pipeline(
                str(_MODEL_PATH),
                image_path,
                session["paths"]["silver"],
                detector=detector,
            )

            status.write("🗺️ [Gold] Gerando grelha VRA e analytics...")
            det_json = os.path.join(session["paths"]["silver"], "detections.json")
            vra_geo = os.path.join(session["paths"]["gold"], "vra.geojson")
            run_vra_mapping_pipeline(det_json, image_path, vra_geo, grid_size=grid_size)

            st.session_state["vra_path"] = vra_geo
            st.session_state["ortho_path"] = image_path
            st.session_state["shp_dir"] = os.path.join(session["paths"]["gold"], "shapefile")

            status.update(label="✅ Processamento concluído!", state="complete")
            st.success("Tudo pronto! O Shapefile e o Relatório PDF foram gerados.")
            st.page_link("pages/VRA.py", label="Ver Resultados e Download", icon="🗺️")

        except Exception as e:
            st.error(f"Erro Crítico: {e}")
            status.update(label="❌ Falha no pipeline", state="error")
