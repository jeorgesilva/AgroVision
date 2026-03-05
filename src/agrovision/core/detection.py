# src/agrovision/core/detection.py
from typing import List
from pathlib import Path
from agrovision.models.yolo import WeedDetector as YoloWeedDetector
from agrovision.data.loaders import list_images

def run_batch_detection(model_path: str, input_dir: str):
    detector = YoloWeedDetector(model_path)
    images = list_images(input_dir)
    results = []
    for img in images:
        pred = detector.detect(str(img))
        results.append((img, pred))
    return results
