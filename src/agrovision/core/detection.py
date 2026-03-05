# src/agrovision/core/detection.py
from agrovision.models.yolo import WeedDetector


def run_detection(model_path: str, image_path: str) -> list:
    """
    Runs weed detection on a single image.
    """
    detector = WeedDetector(model_path)
    detections = detector.detect(image_path)
    return detections
