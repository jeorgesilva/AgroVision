# 🌾 AgroVision — Precision Weed Detection & VRA Mapping

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Ultralytics YOLO](https://img.shields.io/badge/Ultralytics_YOLO-FF6F00?style=for-the-badge) ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white) ![GeoPandas](https://img.shields.io/badge/GeoPandas-2E8B57?style=for-the-badge&logo=geopandas&logoColor=white) ![Shapely](https://img.shields.io/badge/Shapely-0F172A?style=for-the-badge) ![Rasterio](https://img.shields.io/badge/Rasterio-007ACC?style=for-the-badge) ![Streamlit](https://img.shields.io/badge/Streamlit-FE4B4B?style=for-the-badge&logo=streamlit&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-0db7ed?style=for-the-badge&logo=docker&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

---

Kurzbeschreibung

    AgroVision wandelt Drohnen‑Ortomosaike in VRA‑(Variable Rate Application)‑Prescriptions um.
    Workflow: Detektion (YOLO) → Georeferenzierung → VRA‑Grid → Export (GeoJSON / Shapefile).
    Zielgruppe: Drohnenpiloten und Lohnunternehmer (500–2.000 ha), die präzise, kosten‑ und zeiteffiziente Applikationen benötigen.

---
Hauptfunktionen

    Unkraut‑Detektion mit YOLO (mehrere Arten wählbar).

    Pixel → GPS: automatische Umrechnung über GeoTIFF‑Transform.

    VRA‑Grid (z. B. 5×5 m) mit Dosiszuweisung (z. B. 0 / 150 L/ha).

    Export: GeoJSON, Shapefile (.zip) und PDF‑Kurzberichte.

    Demo‑Interface: Streamlit mit interaktivem Folium/Leaflet‑Kartenviewer.

    Automatisierbare Pipeline: Inferenz → Geoprocess → Export.

---

## Outputs
- `outputs/detections/` → JSON mit Bounding‑Boxes + annotierte Bilder  
- `outputs/vra/vra.geojson` → VRA‑Karte (Grid mit Dichten)  
- Exportierbare GeoJSON/GeoTIFF für GIS‑Workflows

---

## Projektstruktur (Kurz)

    AgroVision/
    ├─ docs/
    │  ├─ map.html
    │  ├─ vra.geojson
    │  └─ images/
    │     └─ map_thumb.png
    ├─ src/
    │  ├─ agrovision/
    │  │  ├─ core/
    │  │  │  └─ geoprocess.py
    │  │  ├─ pipelines/
    │  │  │  └─ vra_mapping.py
    │  │  ├─ models/
    │  │  │  └─ yolo.py
    │  │  └─ interfaces/
    │  │     └─ cli.py
    ├─ app/
    │  └─ streamlit/
    │     └─ VRA.py
    ├─ data/
    │  ├─ raw/
    │  └─ sessions/
    ├─ weights/
    ├─ requirements.txt
    └─ README.md


---

## Schnellstart (lokal)

Klonen

    git clone https://github.com/jeorgesilva/AgroVision.git
    cd AgroVision

Virtuelle Umgebung & Abhängigkeiten

    python -m venv .venv
    source .venv/bin/activate   # macOS / Linux
    .venv\Scripts\activate      # Windows
    pip install -r requirements.txt
    
Modellgewichte

    Kopiere weights/best.pt in weights/.

Detektion (Beispiel CLI)

    python src/agrovision/interfaces/cli.py detect \
      --model weights/best.pt \
      --input_dir data/images \
      --output_dir outputs/detections

VRA‑Erzeugung

    python src/agrovision/interfaces/cli.py map \
      --detections outputs/detections/detections.json \
      --image /path/to/ortho.tif \
      --output outputs/vra/vra.geojson
    
Demo starten

    streamlit run app/streamlit/VRA.py

---


## Hinweise & Best Practices
- **Daten:** Trainingsdaten sind aus Lizenzgründen nicht enthalten — siehe `data/README.md` für Hinweise zur Vorbereitung.  
- **Reproduzierbarkeit:** Versioniere Weights und speichere `transform.json` mit Metadaten (CRS, resolution).  
- **Sicherheit:** Feldbehandlungen immer mit zertifizierten Agronomen abstimmen.

---

## Kontakt
**Jeorge Silva** — AI Engineer  
GitHub: `github.com/jeorgesilva`
---
