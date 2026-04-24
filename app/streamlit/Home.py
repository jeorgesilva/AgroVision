import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AgroVision AI | Precision agriculture",
    page_icon="🌱",
    layout="wide"
)

# -----------------------------
# Estilo Customizado (CSS)
# -----------------------------
st.markdown("""
    <style>
    .main {
        background-color: #0b3661;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
    }
    .feature-card {
        background-color: #0b3661;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2e7d32;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# Header / Banner
# -----------------------------
col_logo, col_text = st.columns([1, 4])
with col_text:
    st.title("🌱 AgroVision AI")
    st.subheader("Artificial Intelligence and High-Performance Geoprocessing")

st.markdown(
    """
    AgroVision is a cutting-edge solution designed for drone operators and rural producers seeking cost reduction and agronomic efficiency. We utilize the YOLOv12 architecture for ultra-precise detection and process large-scale orthomosaics (Big Data) with direct integration into the tractor's monitor.
    """
)

st.divider()

# -----------------------------
# Principais Diferenciais (Analytics & Tech)
# -----------------------------
st.markdown("### 🛠️ Technological Advantages")
c1, c2, c3 = st.columns(3)

with c1:
    st.info("🚀 **Engine**\n\nWeed and tree detection with superior precision, trained for real-world field conditions.")

with c2:
    st.success("🗺️ **VRA Grid Snapping**\n\nGeneration of variable rate maps (SHP) with target-centered grids, ready for DJI and XAG drones.")

with c3:
    st.warning("📊 **Analytics & Reports**\n\nAutomatic calculation of input savings and generation of technical reports in PDF for the end client.")

st.divider()

# -----------------------------
# Navegação Principal
# -----------------------------
st.markdown("### 🎯 Start Operation")

col_det, col_vra = st.columns(2)

with col_det:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("#### 🌿 Detection & Processing")
    st.write("Upload orthomosaics (TIF/ECW) or point to files of up to 20GB on Drive to start the AI analysis.")
    if st.button("Open Weed Detection"):
        st.switch_page("pages/Detection.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col_vra:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown("#### 🗺️ Maps & Reports")
    st.write("Visualize the infestation, analyze savings charts, and download the package for the tractor (SHP) and the report (PDF).")
    if st.button("Abrir VRA Map"):
        st.switch_page("pages/VRA.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# -----------------------------
# Footer / Info de Negócio
# -----------------------------
st.markdown("### 📄 Info")
st.caption("Versão: 3.2")