import argparse
from agrovision.pipelines.detect_weeds import run_detection_pipeline
from agrovision.pipelines.vra_mapping import run_vra_mapping_pipeline


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AgroVision — Precision Weed Detection & VRA Mapping",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  agrovision detect --model weights/best.pt"
            " --input_dir data/images --output_dir outputs/detections\n"
            "  agrovision map --detections outputs/detections/detections.json"
            " --raster data/ortho.tif --output outputs/vra/vra.geojson"
        ),
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    # ── detect ────────────────────────────────────────────────────────────
    det_p = subparsers.add_parser(
        "detect",
        help="Run weed detection on an orthomosaic or a directory of images.",
    )
    det_p.add_argument("--model", required=True, help="Path to YOLO weights (.pt).")
    det_p.add_argument(
        "--input_dir",
        required=True,
        help="GeoTIFF path or directory of image files to process.",
    )
    det_p.add_argument(
        "--output_dir",
        required=True,
        help="Directory where detections.json (Silver layer) will be saved.",
    )

    # ── map ───────────────────────────────────────────────────────────────
    map_p = subparsers.add_parser(
        "map",
        help="Convert detections to a VRA grid map and generate reports.",
    )
    map_p.add_argument(
        "--detections",
        required=True,
        help="Path to detections.json produced by the 'detect' command.",
    )
    map_p.add_argument(
        "--raster",
        required=True,
        help="Path to the source orthomosaic GeoTIFF (used for CRS and transform).",
    )
    map_p.add_argument(
        "--output",
        required=True,
        help="Destination path for the VRA GeoJSON (Gold layer).",
    )
    map_p.add_argument(
        "--grid_size",
        type=float,
        default=10.0,
        help="Application grid cell size in metres (default: 10.0).",
    )

    return parser


def main() -> None:
    args = _build_parser().parse_args()

    if args.command == "detect":
        run_detection_pipeline(args.model, args.input_dir, args.output_dir)
    elif args.command == "map":
        run_vra_mapping_pipeline(
            args.detections, args.raster, args.output, grid_size=args.grid_size
        )


if __name__ == "__main__":
    main()
