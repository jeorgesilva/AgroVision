# src/agrovision/data/loaders.py

from pathlib import Path
import json
from typing import List, Dict, Any
import geopandas as gpd


VALID_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}


def list_images(input_dir: str) -> List[Path]:
    """Return a list of image file paths inside a directory (recursive)."""
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    return [
        p for p in input_path.rglob("*")
        if p.suffix.lower() in VALID_IMAGE_EXTS
    ]


def load_json(json_path: str) -> Dict[str, Any]:
    """Load a JSON file and return its content."""
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_geojson(geojson_path: str) -> gpd.GeoDataFrame:
    """Load a GeoJSON file into a GeoDataFrame."""
    path = Path(geojson_path)
    if not path.exists():
        raise FileNotFoundError(f"GeoJSON file not found: {geojson_path}")

    return gpd.read_file(path)
