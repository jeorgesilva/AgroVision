"""Thin wrapper around the unified CLI for the VRA mapping command.

Usage:
    python scripts/run_vra_mapping.py --detections <path> \
                                       --raster     <path> \
                                       --output     <path> \
                                       [--grid_size <float>]

The 'map' subcommand is inserted automatically.  All argument parsing lives
in a single place (interfaces/cli.py) to avoid duplication.
"""
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_SRC = _PROJECT_ROOT / "src"
try:
    import agrovision  # noqa: F401
except ImportError:
    if _SRC.is_dir():
        sys.path.insert(0, str(_SRC))

from agrovision.interfaces.cli import main  # noqa: E402

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] != "map":
        sys.argv.insert(1, "map")
    main()
