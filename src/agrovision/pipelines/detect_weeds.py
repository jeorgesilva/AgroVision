# src/agrovision/pipelines/detect_weeds.py
import json
import os
from agrovision.core.detection import run_batch_detection

def run_detection_pipeline(model_path: str, input_dir: str, output_dir: str):
    """
    Executa o pipeline e guarda os resultados. 
    Agora suporta Metadados Espaciais para Ortomosaicos fatiados!
    """
    os.makedirs(output_dir, exist_ok=True)

    raw_results = run_batch_detection(model_path, input_dir)
    formatted_results = []

    for img_path, pred in raw_results:
        entry = {
            "image_path": str(img_path),
            "image_shape": pred.get("image_shape", None),
            "metadata": pred.get("metadata", {}), # <--- A GRANDE ADIÇÃO AQUI
            "detections": []
        }

        for det in pred.get("detections", []):
            entry["detections"].append({
                "bbox": det["bbox"],
                "class_name": det["class_name"],
                "confidence": det["confidence"]
            })

        formatted_results.append(entry)

    output_path = os.path.join(output_dir, "detections.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(formatted_results, f, indent=4)
        
    print(f"✅ Deteções salvas com sucesso em: {output_path}")