"""Smoke tests for CLI entry points.

Goals:
- Prove the module tree imports without ImportError / ModuleNotFoundError.
- Prove each entry-point function dispatches to the correct pipeline without
  actually running YOLO, rasterio, or any I/O.

Heavy dependencies (ultralytics, rasterio, geopandas …) are patched at the
module level so the suite runs in any CI environment, even without GPU drivers
or geospatial system libraries.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Patch heavy optional dependencies before the agrovision package is imported.
# This mirrors what a CI environment without GPU/geo drivers needs.
# ---------------------------------------------------------------------------
_HEAVY = [
    "ultralytics",
    "rasterio", "rasterio.transform", "rasterio.enums", "rasterio.plot",
    "rasterio.windows",
    "geopandas", "fiona", "pyproj", "shapely", "shapely.geometry",
    "shapely.ops",
    "torch", "torchvision",
    "folium", "folium.raster_layers", "streamlit_folium",
    "streamlit",
    "fpdf",
]
for _mod in _HEAVY:
    sys.modules.setdefault(_mod, MagicMock())


# ---------------------------------------------------------------------------
# Import guard — catches any ImportError / ModuleNotFoundError on the spot.
# ---------------------------------------------------------------------------

def test_cli_module_imports_cleanly():
    from agrovision.interfaces import cli  # noqa: F401


def test_pipelines_import_cleanly():
    from agrovision.pipelines import detect_weeds, vra_mapping  # noqa: F401


# ---------------------------------------------------------------------------
# Entry-point dispatch tests — no real pipelines are executed.
# ---------------------------------------------------------------------------

def test_run_detection_dispatches_to_pipeline():
    mock_argv = [
        "agrovision-detect",
        "--model", "weights/best.pt",
        "--input_dir", "data/images",
        "--output_dir", "/tmp/silver",
    ]
    with patch.object(sys, "argv", mock_argv), \
         patch("agrovision.interfaces.cli.run_detection_pipeline") as mock_fn:
        from agrovision.interfaces.cli import run_detection
        run_detection()

    mock_fn.assert_called_once_with("weights/best.pt", "data/images", "/tmp/silver")


def test_run_vra_dispatches_to_pipeline():
    mock_argv = [
        "agrovision-map",
        "--detections", "silver/detections.json",
        "--raster",     "bronze/ortho.tif",
        "--output",     "/tmp/gold/vra.geojson",
        "--grid_size",  "15.0",
    ]
    with patch.object(sys, "argv", mock_argv), \
         patch("agrovision.interfaces.cli.run_vra_mapping_pipeline") as mock_fn:
        from agrovision.interfaces.cli import run_vra
        run_vra()

    mock_fn.assert_called_once_with(
        "silver/detections.json",
        "bronze/ortho.tif",
        "/tmp/gold/vra.geojson",
        grid_size=15.0,
    )
