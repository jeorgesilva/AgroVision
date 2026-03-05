# src/agrovision/data/transforms.py
import json


def load_transform(transform_path: str):
    """Loads a coordinate transformation from a file."""
    with open(transform_path) as f:
        return json.load(f)


def apply_transform(detections: list, transform: dict) -> list:
    """Applies a coordinate transformation to a list of detections."""
    # This is a placeholder for a real coordinate transformation
    # In a real-world scenario, this would involve a proper georeferencing process
    for detection in detections:
        detection["x"] = detection["x"] * transform.get("scale_x", 1) + transform.get("translate_x", 0)
        detection["y"] = detection["y"] * transform.get("scale_y", 1) + transform.get("translate_y", 0)
    return detections
