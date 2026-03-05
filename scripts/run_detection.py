import argparse
from agrovision.pipelines.detect_weeds import run_detection_pipeline


def main():
    parser = argparse.ArgumentParser(description="Run weed detection pipeline")
    parser.add_argument("--model", required=True, help="Path to YOLO model")
    parser.add_argument("--input_dir", required=True, help="Directory with input images")
    parser.add_argument("--output_dir", required=True, help="Directory to save detections")

    args = parser.parse_args()

    run_detection_pipeline(
        model_path=args.model,
        input_dir=args.input_dir,
        output_dir=args.output_dir
    )


if __name__ == "__main__":
    main()
