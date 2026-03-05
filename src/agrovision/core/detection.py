# src/agrovision/core/detection.py
from ultralytics import YOLO


class WeedDetector:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def detect(self, image_path: str) -> list:
        """Performs weed detection on an image."""
        results = self.model(image_path)
        detections = []
        for result in results:
            for box in result.boxes:
                detections.append(
                    {
                        "box": box.xyxy[0].tolist(),
                        "confidence": box.conf[0].item(),
                        "class": self.model.names[int(box.cls[0].item())],
                    }
                )
        return detections
