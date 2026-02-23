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
