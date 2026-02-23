```markdown
# 🌿 AgroVision AI: Multi-Agent Crop Disease Detection

An enterprise-grade AgTech proof-of-concept that bridges the gap between **Computer Vision** and **Multi-Agent LLM Orchestration** to provide real-time, expert-level agronomic diagnostics.

## 🎯 Project Overview

In precision agriculture, simply detecting a disease is not enough; farmers need immediate, actionable, and accurate treatment plans. **AgroVision AI** solves this by using a two-tier AI architecture:
1. **The Eyes (Computer Vision):** A custom-trained YOLOv8 model detects crop diseases from leaf images.
2. **The Brain (CrewAI Multi-Agent System):** Instead of relying on a single LLM prompt (which is prone to hallucinations), the system triggers a specialized crew of AI agents (a Chief Agronomist and a Treatment Specialist) to debate and generate a factual, step-by-step action plan.

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
agrovision-ai/
├── app/
│   ├── __init__.py
│   └── streamlit_app.py        # Main Streamlit UI (Frontend)
├── core/
│   ├── __init__.py
│   ├── vision.py               # YOLOv8 inference and image processing logic
│   └── crew_logic.py           # CrewAI multi-agent orchestration and LLM config
├── data/
│   ├── sample_images/          # Test images (healthy and diseased leaves)
│   └── models/                 # Trained YOLO weights (e.g., yolov8n.pt)
├── tests/
│   └── __init__.py
├── requirements.txt            # Project dependencies
├── .env.example                # Template for environment variables
├── .gitignore                  # Git ignore file (excludes weights, secrets, etc.)
└── README.md                   # Project documentation

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

### 3. Setup Environment Variables

Create a `.streamlit/secrets.toml` file in the root directory and add your HuggingFace token:

```toml
HUGGINGFACEHUB_API_TOKEN = "your_hf_token_here"

```

*Note: Ensure `.streamlit/` is added to your `.gitignore` to prevent leaking API keys.*

### 4. Run the Application

```bash
streamlit run app/streamlit_app.py

```

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
