import json
import os
from tqdm import tqdm

from agrovision.data.loaders import list_images
from agrovision.core.detection import run_batch_detection


def run_detection_pipeline(model_path: str, input_dir: str, output_dir: str):
    """Runs the weed detection pipeline and saves results as JSON."""

    os.makedirs(output_dir, exist_ok=True)

    # Run batch detection (Fase 1.2)
    results = run_batch_detection(model_path, input_dir)

    # Save as a list (consistent with mapping.py)
    output_path = os.path.join(output_dir, "detections.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"Detections saved to {output_path}")
