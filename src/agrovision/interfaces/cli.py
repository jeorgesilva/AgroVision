# src/agrovision/interfaces/cli.py
import argparse

from agrovision.pipelines.detect_weeds import run_detection_pipeline
from agrovision.pipelines.vra_mapping import run_vra_mapping_pipeline
from agrovision.config import GRID_SIZE


def main():
    parser = argparse.ArgumentParser(description="AgroVision CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Detection parser
    detection_parser = subparsers.add_parser("detect", help="Run weed detection pipeline.")
    detection_parser.add_argument("--model", type=str, required=True, help="Path to the YOLO model.")
    detection_parser.add_argument("--input_dir", type=str, required=True, help="Path to the input image directory.")
    detection_parser.add_argument("--output_dir", type=str, required=True, help="Path to the output directory.")

    # VRA mapping parser
    vra_parser = subparsers.add_parser("map", help="Run VRA mapping pipeline.")
    vra_parser.add_argument("--detections", type=str, required=True, help="Path to the detections JSON file.")
    vra_parser.add_argument("--transform", type=str, required=True, help="Path to the transform JSON file.")
    vra_parser.add_argument("--output", type=str, required=True, help="Path to the output GeoJSON file.")
    vra_parser.add_argument("--grid_size", type=int, default=GRID_SIZE, help="Grid size in meters.")

    args = parser.parse_args()

    if args.command == "detect":
        run_detection_pipeline(args.model, args.input_dir, args.output_dir)
    elif args.command == "map":
        run_vra_mapping_pipeline(args.detections, args.transform, args.output, args.grid_size)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
