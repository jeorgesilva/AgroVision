# src/agrovision/core/mapping.py
import json
import geopandas as gpd
from shapely.geometry import box

from agrovision.core.geoprocess import create_grid, calculate_weed_density
from agrovision.data.transforms import apply_transform, load_transform


def create_vra_map(detections_path: str, transform_path: str, output_path: str, grid_size: int):
    """Creates a VRA map from detections."""
    with open(detections_path) as f:
        all_detections = json.load(f)

    transform = load_transform(transform_path)

    weed_boxes = []
    for image_name, detections in all_detections.items():
        transformed_detections = apply_transform(detections, transform)
        for detection in transformed_detections:
            x1, y1, x2, y2 = detection["box"]
            weed_boxes.append(box(x1, y1, x2, y2))

    weeds_gdf = gpd.GeoDataFrame(geometry=weed_boxes, crs="EPSG:4326")  # Assuming WGS84

    # Create a grid over the area of the weeds
    grid = create_grid(weeds_gdf, grid_size)

    # Calculate weed density
    grid_with_density = calculate_weed_density(grid, weeds_gdf)

    # Filter for grid cells with weeds
    vra_map = grid_with_density[grid_with_density["weed_density"] > 0]

    # Save to GeoJSON
    vra_map.to_file(output_path, driver="GeoJSON")
    print(f"VRA map saved to {output_path}")
