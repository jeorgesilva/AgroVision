from agrovision.core.mapping import create_vra_map

def run_vra_mapping_pipeline(detections_path, raster_path, output_path, grid_size=10.0, **kwargs):
    create_vra_map(detections_path, raster_path, output_path, grid_size=grid_size)