# scripts/run_vra_mapping.py
import argparse

from agrovision.config import GRID_SIZE
from agrovision.pipelines.vra_mapping import run_vra_mapping_pipeline


def main():
    parser = argparse.ArgumentParser(description="Run VRA mapping pipeline.")
    parser.add_argument("--detections", type=str, required=True, help="Path to the detections JSON file.")
    parser.add_argument("--transform", type=str, required=True, help="Path to the transform JSON file.")
    parser.add_argument("--output", type=str, required=True, help="Path to the output GeoJSON file.")
    parser.add_argument("--grid_size", type=int, default=GRID_SIZE, help="Grid size in meters.")
    args = parser.parse_args()

    run_vra_mapping_pipeline(args.detections, args.transform, args.output, args.grid_size)


if __name__ == "__main__":
    main()
