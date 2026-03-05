# src/agrovision/pipelines/detect_weeds.py
import json
import os

from tqdm import tqdm

from agrovision.data.loaders import load_images
from agrovision.models.yolo import WeedDetector


def run_detection_pipeline(model_path: str, input_dir: str, output_dir: str):
    """Runs the weed detection pipeline."""
    detector = WeedDetector(model_path)
    image_paths = load_images(input_dir)

    os.makedirs(output_dir, exist_ok=True)

    all_detections = {}
    for image_path in tqdm(image_paths, desc="Detecting weeds"):
        detections = detector.detect(image_path)
        image_name = os.path.basename(image_path)
        all_detections[image_name] = detections

    output_path = os.path.join(output_dir, "detections.json")
    with open(output_path, "w") as f:
        json.dump(all_detections, f, indent=4)

    print(f"Detections saved to {output_path}")
