from typing import Dict, Any
from ultralytics import YOLO
from PIL import Image
import rasterio
from rasterio.plot import reshape_as_image
import numpy as np

Image.MAX_IMAGE_PIXELS = None

def load_image_robust(image_path):
    """Loads TIFF/GeoTIFF images robustly by converting to RGB uint8."""
    try:
        # Try standard loading first
        return Image.open(image_path).convert("RGB")
    except Exception:
        # Fallback for GeoTIFFs using rasterio
        try:
            with rasterio.open(image_path) as src:
                data = src.read()
                
                # Handle Bands (Select first 3 for RGB)
                if data.shape[0] > 3:
                    data = data[:3, :, :]
                elif data.shape[0] == 1:
                    data = np.repeat(data, 3, axis=0)
                
                img_array = reshape_as_image(data)
                
                # Normalize Data Types (float -> uint8)
                if np.issubdtype(img_array.dtype, np.floating):
                    min_val = np.nanmin(img_array)
                    max_val = np.nanmax(img_array)
                    if max_val > min_val:
                        img_array = ((img_array - min_val) / (max_val - min_val) * 255)
                    else:
                        img_array = np.zeros_like(img_array)
                    img_array = img_array.astype('uint8')
                elif img_array.dtype == 'uint16':
                    img_array = (img_array / 256).astype('uint8')
                
                if img_array.dtype != 'uint8':
                     img_array = img_array.astype('uint8')

                return Image.fromarray(img_array)
        except Exception as e:
            raise ValueError(f"Could not load image: {e}")

class WeedDetector:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def detect(self, source: Any, metadata: dict = None) -> Dict[str, Any]:
        """
        Executa a deteção. O 'source' pode ser uma string (caminho) ou uma imagem PIL (vinda do tiler).
        """
        # Se for um caminho de ficheiro, carrega a imagem. Se for objeto PIL, usa diretamente.
        if isinstance(source, str):
            image = load_image_robust(source)
            source_id = source
        else:
            image = source
            # Usa um ID único para a fatia (ex: nome_x_y)
            source_id = metadata.get("tile_id", "fatia_memoria") if metadata else "fatia_memoria"
        
        results = self.model(image)
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
            "image_path": source_id,
            "detections": detections,
            "image_shape": list(image.size),
            "metadata": metadata or {} # Passamos os metadados (Transformada Afim) para o resultado
        }