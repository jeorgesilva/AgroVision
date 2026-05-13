# src/agrovision/config.py

# YOLO model configuration - Apontando para o modelo da Época 41
YOLO_MODEL_PATH = "checkpoint_emergencia_v12.pt"

# VRA mapping configuration
GRID_SIZE = 10.0  # metros (padrão)
MIN_WEED_DENSITY = 0.1  # minimum weed density

# Input/Output paths
INPUT_IMAGE_DIR = "data/images"
OUTPUT_DETECTION_DIR = "outputs/detections"
OUTPUT_VRA_MAP_DIR = "outputs/vra_maps"
