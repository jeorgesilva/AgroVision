import argparse
from agrovision.pipelines.detect_weeds import run_detection_pipeline
from agrovision.pipelines.vra_mapping import run_vra_mapping_pipeline

def main():
    parser = argparse.ArgumentParser(description="AgroVision CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Detect
    det_p = subparsers.add_parser("detect")
    det_p.add_argument("--model", required=True)
    det_p.add_argument("--input_dir", required=True)
    det_p.add_argument("--output_dir", required=True)

    # Map
    map_p = subparsers.add_parser("map")
    map_p.add_argument("--detections", required=True)
    map_p.add_argument("--raster", required=True)
    map_p.add_argument("--output", required=True)
    map_p.add_argument("--grid_size", type=float, default=10.0) # <--- AQUI

    args = parser.parse_args()

    if args.command == "detect":
        run_detection_pipeline(args.model, args.input_dir, args.output_dir)
    elif args.command == "map":
        run_vra_mapping_pipeline(args.detections, args.raster, args.output, grid_size=args.grid_size) # <--- AQUI
        
if __name__ == "__main__":
    main()
