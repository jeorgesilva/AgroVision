# src/agrovision/pipelines/vra_mapping.py
from agrovision.core.mapping import create_vra_map


def run_vra_mapping_pipeline(detections_path: str, transform_path: str, output_path: str, grid_size: int):
    """Runs the VRA mapping pipeline."""
    create_vra_map(detections_path, transform_path, output_path, grid_size)
