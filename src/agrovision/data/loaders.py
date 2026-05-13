import os
from pathlib import Path
from typing import Union


def list_images(directory: Union[str, Path]) -> list[Path]:
    """List all images in a directory (recursive)."""
    directory = Path(directory)
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
    images = []
    for root, _, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in extensions:
                images.append(Path(root) / file)
    return images
