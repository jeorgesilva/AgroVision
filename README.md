# 🌱 AgroVision — Precision Weed Detection & VRA Mapping

AgroVision is an applied AgTech project combining **Computer Vision** and **Geospatial Analysis** to enable **precision herbicide application**.

## 🎯 Features
- Weed detection using **YOLOv8**
- Geospatial processing with **GeoPandas**
- Automatic generation of **Variable-Rate Application (VRA)** maps
- Export to **GeoJSON** for QGIS or agricultural controllers

## 🧠 Tech Stack
Python • YOLOv8 • OpenCV • GeoPandas • Shapely • Rasterio

## 🏗️ Architecture & Workflow

```text
┌─────────────────┐      ┌────────────────────┐      ┌─────────────────────┐
│ 1. Image Upload │ ───> │ 2. YOLOv8 Model    │ ───> │ Detected: e.g.,     │
│  (Streamlit UI) │      │ (Object Detection) │      │ "Soybean Rust"      │
└─────────────────┘      └────────────────────┘      └─────────┬───────────┘
                                                               │
┌──────────────────────────────────────────────────────────────┴───────────┐
│ 3. CrewAI Orchestration (Multi-Agent System)                             │
│                                                                          │
│  🧑‍🔬 Agent 1: Chief Agronomist        👨‍🌾 Agent 2: Treatment Specialist  │
│  Analyzes biological impact and   ──>  Formulates chemical/organic       │
│  contagion risks.                      treatment & preventive measures.  │
└──────────────────────────────────────────────┬───────────────────────────┘
                                               │
┌──────────────────────────────────────────────▼───────────────────────────┐
│ 4. Final Output                                                          │
│ Bounding box visuals + Comprehensive, step-by-step agronomic report      │
└──────────────────────────────────────────────────────────────────────────┘

```

## 📁 Project Structure

```text
AgroVision/
├── README.md
├── requirements.txt
├── pyproject.toml
├── src/
│   └── agrovision/
│       ├── __init__.py
│       ├── config.py
│       ├── data/
│       │   ├── __init__.py
│       │   ├── loaders.py
│       │   ├── geo_utils.py
│       │   └── transforms.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── yolo.py
│       ├── pipelines/
│       │   ├── __init__.py
│       │   ├── detect_weeds.py
│       │   └── vra_mapping.py
│       └── utils/
│           ├── __init__.py
│           └── file_utils.py
├── scripts/
│   ├── run_detection.py
│   └── run_vra_mapping.py
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_train_yolo.ipynb
│   └── 03_vra_demo.ipynb
└── configs/
    ├── yolo.yaml
    └── vra.yaml

```

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Interactive, state-managed UI)
* **Computer Vision:** Ultralytics YOLOv8 (Real-time object detection)
* **Agent Orchestration:** CrewAI & LangChain
* **LLM Provider:** HuggingFace Inference API (`meta-llama/Llama-3.1-8B-Instruct`)
* **Image Processing:** OpenCV & Pillow

## 💡 Why This Architecture? (The Engineering Choice)

* **Hallucination Mitigation:** By anchoring the LLM's context strictly to the YOLOv8 output, and dividing tasks among specialized agents via CrewAI, the system prevents generic or hallucinated agricultural advice.
* **Separation of Concerns:** The vision model handles pixels; the LLM handles text logic. This allows independent scaling and fine-tuning of each component.
* **Cost-Effective:** Utilizes the HuggingFace Router for inference, keeping API costs to a minimum while maintaining high reasoning capabilities.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone [https://github.com/jeorgesilva/agrovision-ai.git](https://github.com/jeorgesilva/agrovision-ai.git)
cd agrovision-ai

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

*(Requires Python 3.9+)*

### 3. Run weed detection

```toml
python scripts/run_detection.py \
--model weights/best.pt \
--input_dir data/images \
--output_dir outputs/detections
```

*Note: Ensure `.streamlit/` is added to your `.gitignore` to prevent leaking API keys.*

### 4. Generate VRA map

```bash
python scripts/run_vra_mapping.py \
--detections outputs/detections.json \
--transform data/transform.json \
--output outputs/vra.geojson
```

## 📦 Output
- Annotated images with weed bounding boxes
- `vra.geojson` containing weed density per grid cell

## 🗺️ Roadmap & Future Enhancements

* [ ] **Custom Dataset Fine-Tuning:** Train YOLOv8 on specific regional datasets (e.g., Brazilian Soybean or German Wheat diseases).
* [ ] **Offline Edge Deployment:** Optimize the YOLO model using TensorRT for offline inference on farm equipment.
* [ ] **Drone Integration:** Process batch images captured by agricultural drones (DJI/XAG) for field-level mapping.
* [ ] **Weather API Integration:** Pass real-time weather data to the CrewAI agents to adjust treatment recommendations (e.g., "Do not spray today due to high winds").

## 👨‍💻 Author

**Jeorge Silva**
*Junior AI Engineer | Bridging Data Science and AgTech*
[LinkedIn](https://www.google.com/search?q=https://linkedin.com/in/jeorgecssilva) | [GitHub](https://www.google.com/search?q=https://github.com/jeorgesilva)

---

*Disclaimer: This is a portfolio proof-of-concept. Real-world agricultural application of chemicals should always be verified by a certified human agronomist.*

```


**Quer que eu te mande agora o link do dataset de folhas do Kaggle e o script curtinho do Google Colab para você treinar o seu YOLOv8 e gerar o arquivo `.pt` real para a pasta `data/models/`?**

```
