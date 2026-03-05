# scripts/run_detection.py
import sys
from agrovision.interfaces.cli import main

if __name__ == "__main__":
    # Simulate command line arguments for the detection command
    sys.argv = [
        sys.argv[0], 
        "detect", 
        "--model", "weights/best.pt",
        "--input_dir", "data/images",
        "--output_dir", "outputs/detections"
    ]
    main()
