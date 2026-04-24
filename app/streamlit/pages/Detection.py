import streamlit as st
import sys
import os
from pathlib import Path

# 1. SETUP DE CAMINHOS (Sempre no topo)
sys.path.append("/content/drive/MyDrive/Agroview/AgroVision/src")

# 2. IMPORTS DO PROJETO
from agrovision.data.pre_processing import convert_ecw_to_cog
from agrovision.pipelines.detect_weeds import run_detection_pipeline
from agrovision.pipelines.vra_mapping import run_vra_mapping_pipeline
from agrovision.utils.session_manager import SessionManager

# 3. IMPORTS DE TERCEIROS
import numpy as np
from PIL import Image
import rasterio
from rasterio.plot import reshape_as_image

# -----------------------------
# Configuração da Página
# -----------------------------
st.set_page_config(page_title="AgroVision Detection", page_icon="🌿", layout="wide")
Image.MAX_IMAGE_PIXELS = None

def load_image_robust(image_path):
    try:
        return Image.open(image_path).convert("RGB")
    except:
        with rasterio.open(image_path) as src:
            # Downsample para visualização rápida no Streamlit
            data = src.read(out_shape=(src.count, 512, 512))
            img_array = reshape_as_image(data[:3, :, :])
            return Image.fromarray(img_array.astype('uint8'))

# -----------------------------
# Lógica de Inicialização
# -----------------------------
base_data_dir = "/content/drive/MyDrive/Agroview/AgroVision/src/agrovision/data"
session_mgr = SessionManager(base_data_dir)

st.title("🌿 AgroVision Detection")

with st.sidebar:
    st.header("⚙️ Configurações")
    grid_size = st.number_input("Tamanho da Grelha (m)", min_value=1.0, value=10.0)
    if st.button("🔄 Reiniciar Sessão"):
        SessionManager.clear_st_session()
        st.rerun()

# -----------------------------
# Input de Arquivos (Upload ou Local)
# -----------------------------
col_up, col_loc = st.columns(2)

with col_up:
    uploaded_file = st.file_uploader("Upload Ortomosaico (< 200MB)", type=["tif", "tiff", "ecw"])

with col_loc:
    local_path_input = st.text_input("Caminho no Drive (para arquivos > 200MB):", 
                                    placeholder="/content/drive/MyDrive/Fazenda/mapa_20gb.tif")

# Determinar qual fonte usar
input_source = uploaded_file if uploaded_file else local_path_input

# Determinar qual fonte usar
input_source = uploaded_file if uploaded_file else local_path_input

if input_source:
    # 1. Gerenciamento de Sessão (Executa para qualquer uma das fontes)
    source_name = uploaded_file.name if uploaded_file else os.path.basename(local_path_input)
    
    if "current_session" not in st.session_state or st.session_state.get("last_file") != source_name:
        session = session_mgr.create_session(prefix="job")
        st.session_state["current_session"] = session
        st.session_state["last_file"] = source_name
        
        # ---------------------------------------------------------
        # CASO 1: UPLOAD VIA NAVEGADOR
        # ---------------------------------------------------------
        if uploaded_file:
            bronze_path = os.path.join(session["paths"]["bronze"], uploaded_file.name)
            with open(bronze_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("🔄 Convertendo arquivo enviado..."):
                proc_path = convert_ecw_to_cog(bronze_path)
                st.session_state["current_ortho_path"] = proc_path
        
        # ---------------------------------------------------------
        # CASO 2: CAMINHO DIRETO DO DRIVE (ARQUIVOS GIGANTES)
        # ---------------------------------------------------------
        else:
            if os.path.exists(local_path_input):
                with st.spinner("🔄 Analisando arquivo gigante (Convertendo ECW para COG se necessário)..."):
                    # Definimos que, se for ECW, a conversão será guardada na pasta Bronze da sessão atual
                    nome_base = os.path.basename(local_path_input)
                    nome_tif = Path(nome_base).with_suffix('.tif').name
                    destino_bronze = os.path.join(session["paths"]["bronze"], nome_tif)
                    
                    # O conversor é inteligente: se for TIF, ele apenas devolve o caminho original (não gasta espaço). 
                    # Se for ECW, ele converte para TIF de forma segura.
                    proc_path = convert_ecw_to_cog(local_path_input, output_path=destino_bronze)
                    st.session_state["current_ortho_path"] = proc_path
                
                st.success("✅ Arquivo processado e vinculado com sucesso!")
            else:
                st.error("❌ Caminho local não encontrado no Drive.")
                st.stop()

    # Recuperar estado da sessão
    session = st.session_state["current_session"]
    image_path = st.session_state["current_ortho_path"]
    
    # Preview
    with st.expander("👁️ Visualizar Ortomosaico", expanded=True):
        st.image(load_image_robust(image_path), caption="🖼️ Preview Web (A Inteligência Artificial utilizará a resolução nativa).", use_column_width=True)

    # -----------------------------
    # Botão de Processamento
    # -----------------------------
    # (Mantenha o resto do código igual daqui para a frente: if st.button("🚀 Iniciar Processamento..."))
    # -----------------------------
    # Botão de Processamento
    # -----------------------------
    if st.button("🚀 Iniciar Processamento Inteligente", type="primary", use_container_width=True):
        status = st.status("⚙️ AgroVision Engine em execução...", expanded=True)
        
        try:
            model_path = "/content/drive/MyDrive/Agroview/AgroVision/checkpoint_emergencia_v12.pt"
            
            # Passo 1: IA (Silver)
            # Nota: Passamos a PASTA onde o arquivo está como input_dir
            status.write(f"🔍 [Silver] Detetando com YOLOv12 (Fatiamento Ativo)...")
            run_detection_pipeline(model_path, image_path, session["paths"]["silver"])
            # Passo 2: Mapeamento (Gold)
            status.write("🗺️ [Gold] Gerando Grelha VRA e Analytics...")
            det_json = os.path.join(session["paths"]["silver"], "detections.json")
            vra_geo = os.path.join(session["paths"]["gold"], "vra.geojson")
            
            run_vra_mapping_pipeline(det_json, image_path, vra_geo, grid_size=grid_size)
            
            # Guardar para a página de visualização
            st.session_state["vra_path"] = vra_geo
            st.session_state["ortho_path"] = image_path
            st.session_state["shp_dir"] = os.path.join(session["paths"]["gold"], "shapefile")
            
            status.update(label="✅ Processamento Concluído!", state="complete")
            st.success("Tudo pronto! O Shapefile e o Relatório PDF foram gerados.")
            st.page_link("pages/VRA.py", label="Ver Resultados e Download", icon="🗺️")

        except Exception as e:
            st.error(f"Erro Crítico: {e}")
            status.update(label="❌ Falha no Pipeline", state="error")