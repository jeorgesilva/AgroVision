from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path

import rasterio
from rasterio.enums import Resampling

logger = logging.getLogger(__name__)

_TIF_EXTENSIONS = {".tif", ".tiff"}

_COG_OPTIONS: dict = {
    "driver": "GTiff",
    "compress": "DEFLATE",
    "predictor": 2,
    "tiled": True,
    "blockxsize": 512,
    "blockysize": 512,
    "BIGTIFF": "IF_SAFER",
}

_OVERVIEW_LEVELS = [2, 4, 8, 16, 32]


def convert_ecw_to_cog(input_path: str, output_path: str | None = None) -> str:
    """Converts any GDAL-readable raster to a Cloud-Optimized GeoTIFF (COG).

    If the source is already a GeoTIFF, the original path is returned unchanged
    — no disk copy is made.  If the destination already exists, the conversion
    is also skipped.

    Args:
        input_path:  Path to the source raster (ECW, JP2, TIF, etc.).
        output_path: Where to write the COG.  Defaults to the source directory
                     with the file extension replaced by ".tif".

    Returns:
        Absolute path string of the resulting GeoTIFF.

    Raises:
        FileNotFoundError: if input_path does not exist.
        RuntimeError:      if the GDAL driver needed to read the source is
                           unavailable (e.g. ECW without the proprietary plugin).
    """
    src = Path(input_path)

    if not src.exists():
        raise FileNotFoundError(f"Input raster not found: {src}")

    if src.suffix.lower() in _TIF_EXTENSIONS:
        logger.info("Source is already a GeoTIFF — skipping conversion: %s", src.name)
        return str(src)

    dst = Path(output_path) if output_path else src.with_suffix(".tif")
    dst.parent.mkdir(parents=True, exist_ok=True)

    if dst.exists():
        logger.info("COG already exists — skipping conversion: %s", dst.name)
        return str(dst)

    logger.info("Converting %s → %s", src.name, dst.name)
    _write_cog(src, dst)
    logger.info("Conversion complete: %s", dst.name)

    return str(dst)


def _write_cog(src_path: Path, dst_path: Path) -> None:
    """Writes a Cloud-Optimized GeoTIFF via a two-pass, window-by-window copy.

    Pass 1 — copy bands block-by-block to a temp GeoTIFF, then build overviews
    in-place.  Block-by-block reading avoids loading the full raster into RAM,
    which is essential for ortomosaics that can exceed available memory.

    Pass 2 — rewrite with COPY_SRC_OVERVIEWS=YES so overviews are stored before
    image data, making the file a true COG (required for range-request access).

    If anything goes wrong the partial destination file is deleted so callers
    never find a corrupt output.
    """
    tmp_fd, tmp_name = tempfile.mkstemp(suffix=".tif")
    os.close(tmp_fd)
    tmp_path = Path(tmp_name)

    try:
        # ── Pass 1: write all bands window-by-window ─────────────────────────
        with rasterio.open(src_path) as src:
            _assert_readable(src, src_path)
            profile = src.profile.copy()
            profile.update(_COG_OPTIONS)

            with rasterio.open(tmp_path, "w", **profile) as tmp_dst:
                for _, window in tmp_dst.block_windows(1):
                    tmp_dst.write(src.read(window=window), window=window)

        # ── Build overviews in-place on the temp file ─────────────────────────
        with rasterio.open(tmp_path, "r+") as tmp_dst:
            tmp_dst.build_overviews(_OVERVIEW_LEVELS, Resampling.average)
            tmp_dst.update_tags(ns="rio_overview", resampling="average")

        # ── Pass 2: rewrite with COPY_SRC_OVERVIEWS → true COG ───────────────
        with rasterio.open(tmp_path) as tmp_src:
            profile = tmp_src.profile.copy()
            profile.update({**_COG_OPTIONS, "copy_src_overviews": True})

            with rasterio.open(dst_path, "w", **profile) as final_dst:
                for _, window in final_dst.block_windows(1):
                    final_dst.write(tmp_src.read(window=window), window=window)

    except Exception:
        if dst_path.exists():
            dst_path.unlink()
        raise

    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def _assert_readable(src: rasterio.DatasetReader, path: Path) -> None:
    """Raises RuntimeError with a clear message if the raster has no bands."""
    if src.count == 0:
        raise RuntimeError(
            f"Could not read any bands from '{path.name}'. "
            "If this is an ECW file, ensure the GDAL ECW/JP2 plugin is installed "
            "(gdal-ecw or libgdal-ecw-jp2-plugin depending on your OS)."
        )
