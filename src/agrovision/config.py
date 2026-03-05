# src/agrovision/config.py

# YOLO model configuration
YOLO_MODEL_PATH = "weights/best.pt"

# VRA mapping configuration
GRID_SIZE = 10  # meters
MIN_WEED_DENSITY = 0.1  # minimum weed density to be considered for application

# Input/Output paths
INPUT_IMAGE_DIR = "data/images"
OUTPUT_DETECTION_DIR = "outputs/detections"
OUTPUT_VRA_MAP_DIR = "outputs/vra_maps"
