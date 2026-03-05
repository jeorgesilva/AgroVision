# src/agrovision/models/yolo.py
from ultralytics import YOLO


class WeedDetector:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def detect(self, image_path: str) -> Dict[str, Any]:
        """Run weed detection on a single image and return structured results."""
        results = self.model(image_path)

        # YOLO usually returns a list with a single result
        result = results[0]

        detections = []
        for box in result.boxes:
            detections.append({
                "bbox": box.xyxy[0].tolist(),
                "confidence": float(box.conf[0]),
                "class_id": int(box.cls[0]),
                "class_name": self.model.names[int(box.cls[0])]
            })

        return {
            "image_path": str(image_path),
            "detections": detections,
            "image_shape": result.orig_shape
        }

