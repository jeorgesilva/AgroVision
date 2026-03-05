# src/agrovision/data/loaders.py
import os
from typing import List

import cv2


def load_images(image_dir: str) -> List[str]:
    """Loads image paths from a directory."""
    image_paths = []
    for filename in os.listdir(image_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_paths.append(os.path.join(image_dir, filename))
    return image_paths


def read_image(image_path: str):
    """Reads an image from a path."""
    return cv2.imread(image_path)
