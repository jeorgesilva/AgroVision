"""Thin wrapper around the unified CLI for the detection command.

Usage (unchanged from the original script):
    python scripts/run_detection.py --model <weights> \
                                    --input_dir <path> \
                                    --output_dir <path>

The 'detect' subcommand is inserted automatically so callers do not need to
know about the subcommand structure of interfaces/cli.py.  All argument
parsing lives in a single place (interfaces/cli.py) to avoid duplication.
"""
import sys
from pathlib import Path

# Ensure the package is importable when running from the project root without
# a prior `pip install -e .`.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SRC = _PROJECT_ROOT / "src"
try:
    import agrovision  # noqa: F401
except ImportError:
    if _SRC.is_dir():
        sys.path.insert(0, str(_SRC))

from agrovision.interfaces.cli import main  # noqa: E402

if __name__ == "__main__":
    # Insert the subcommand only when it was not already supplied.
    if len(sys.argv) < 2 or sys.argv[1] != "detect":
        sys.argv.insert(1, "detect")
    main()
