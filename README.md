# 🌱 AgroVision — Precision Weed Detection & VRA Mapping

AgroVision is an applied AgTech project combining **Computer Vision** and **Geospatial Analysis** to enable **precision herbicide application**.

## 🎯 Features
- Weed detection using **YOLOv8**
- Geospatial processing with **GeoPandas**
- Automatic generation of **Variable-Rate Application (VRA)** maps
- Export to **GeoJSON** for QGIS or agricultural controllers
- Interactive web application with **Streamlit**

## 🧠 Tech Stack
Python • YOLOv8 • OpenCV • GeoPandas • Shapely • Rasterio • Streamlit

## 📁 Project Structure
```text
AgroVision/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── data/
│   ├── images/
│   ├── transforms/
│   └── raw/                # opcional
├── weights/
│   └── best.pt
├── outputs/
│   ├── detections/
│   └── vra/
├── configs/
│   ├── yolo.yaml
│   └── vra.yaml
├── src/
│   └── agrovision/
│       ├── __init__.py
│       ├── config.py
│       ├── core/           # lógica central do projeto
│       │   ├── detection.py
│       │   ├── geoprocess.py
│       │   └── mapping.py
│       ├── data/           # loaders e transforms
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
│       ├── utils/
│       │   ├── __init__.py
│       │   └── file_utils.py
│       └── interfaces/
│           ├── cli.py      # comandos CLI
│           └── streamlit_app.py
├── scripts/
│   ├── run_detection.py    # wrappers simples chamando interfaces.cli
│   └── run_vra_mapping.py
└── app/
    └── streamlit/
        ├── Home.py
        ├── Detection.py
        └── VRA.py
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/jeorgesilva/agrovision-ai.git
cd agrovision-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

*(Requires Python 3.9+)*

### 3. Run Weed Detection

You can run the weed detection pipeline using the main CLI script or the simplified script.

Using the main CLI:
```bash
python src/agrovision/interfaces/cli.py detect \
--model weights/best.pt \
--input_dir data/images \
--output_dir outputs/detections
```

Or using the script:
```bash
python scripts/run_detection.py
```

### 4. Generate VRA Map

Similarly, you can generate the VRA map using the main CLI or the script.

Using the main CLI:
```bash
python src/agrovision/interfaces/cli.py map \
--detections outputs/detections/detections.json \
--transform data/transforms/transform.json \
--output outputs/vra/vra.geojson
```

Or using the script:
```bash
python scripts/run_vra_mapping.py
```

### 5. Run the Streamlit Web Application

To explore the project's features through an interactive interface, run the Streamlit app:

```bash
streamlit run app/streamlit/Home.py
```

## 📦 Output
- `detections.json` with bounding boxes for each image.
- `vra.geojson` containing weed density per grid cell for use in GIS software.
- Annotated images (if configured).

## 🗺️ Roadmap & Future Enhancements

* [ ] **Custom Dataset Fine-Tuning:** Train YOLOv8 on specific regional datasets.
* [ ] **Offline Edge Deployment:** Optimize the YOLO model using TensorRT for offline inference on farm equipment.
* [ ] **Drone Integration:** Process batch images captured by agricultural drones.
* [ ] **Weather API Integration:** Use real-time weather data to adjust treatment recommendations.

## 👨‍💻 Author

**Jeorge Silva**
*Junior AI Engineer | Bridging Data Science and AgTech*
[LinkedIn](https://linkedin.com/in/jeorgecssilva) | [GitHub](https://github.com/jeorgesilva)

---

*Disclaimer: This is a portfolio proof-of-concept. Real-world agricultural application of chemicals should always be verified by a certified human agronomist.*
