# scripts/run_vra_mapping.py
import sys
from agrovision.interfaces.cli import main

if __name__ == "__main__":
    # Simulate command line arguments for the mapping command
    sys.argv = [
        sys.argv[0],
        "map",
        "--detections", "outputs/detections/detections.json",
        "--transform", "data/transforms/transform.json",
        "--output", "outputs/vra/vra.geojson"
    ]
    main()
