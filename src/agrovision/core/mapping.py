# src/agrovision/core/mapping.py

import json
import geopandas as gpd
from shapely.geometry import box
from pathlib import Path

from agrovision.core.geoprocess import (
    create_grid,
    calculate_weed_density,
    load_transform,
    apply_transform
)


def create_vra_map(
    detections_path: str,
    transform_path: str,
    output_path: str,
    grid_size: int,
    crs: str = "EPSG:4326"
):
    """Creates a VRA map from YOLO detections and saves it as GeoJSON."""

    detections_path = Path(detections_path)
    if not detections_path.exists():
        raise FileNotFoundError(f"Detections file not found: {detections_path}")

    with open(detections_path, "r", encoding="utf-8") as f:
        all_detections = json.load(f)

    # Expecting a list of detection entries
    # [
    #   {"image_path": "...", "detections": [...], "image_shape": [...]},
    #   ...
    # ]
    transform = load_transform(transform_path)

    geometries = []
    attributes = []

    for entry in all_detections:
        image_path = entry["image_path"]
        detections = entry["detections"]

        transformed = apply_transform(detections, transform)

        for det in transformed:
            x1, y1, x2, y2 = det["bbox"]

            geometries.append(box(x1, y1, x2, y2))
            attributes.append({
                "image": image_path,
                "class": det["class_name"],
                "confidence": det["confidence"]
            })

    weeds_gdf = gpd.GeoDataFrame(attributes, geometry=geometries, crs=crs)

    grid = create_grid(weeds_gdf, grid_size)
    grid_with_density = calculate_weed_density(grid, weeds_gdf)

    vra_map = grid_with_density[grid_with_density["weed_density"] > 0]

    vra_map.to_file(output_path, driver="GeoJSON")
    print(f"VRA map saved to {output_path}")
