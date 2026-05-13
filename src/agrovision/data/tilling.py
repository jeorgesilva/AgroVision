from __future__ import annotations

import math
from collections.abc import Generator

import numpy as np
import rasterio
from PIL import Image
from rasterio.transform import Affine
from rasterio.windows import Window


def gerar_fatias_raster(
    raster_path: str,
    tamanho_fatia: int = 512,
    sobreposicao: float = 0.15,
) -> Generator[tuple[Image.Image, dict], None, None]:
    """Slices a large GeoTIFF into overlapping square tiles.

    Yields (PIL.Image RGB uint8, metadata dict) for each tile.

    Metadata keys:
        x_offset       — left column in global raster pixel space
        y_offset       — top row in global raster pixel space
        tile_width     — actual tile width in pixels (may be < tamanho_fatia at edges)
        tile_height    — actual tile height in pixels (may be < tamanho_fatia at edges)
        transform_fatia — rasterio.Affine mapping tile pixel (0,0) → real-world coords
        crs            — CRS string of the source raster
    """
    if not 0.0 <= sobreposicao < 1.0:
        raise ValueError(f"sobreposicao must be in [0, 1), got {sobreposicao}")

    passo = max(1, math.floor(tamanho_fatia * (1.0 - sobreposicao)))

    with rasterio.open(raster_path) as src:
        raster_width = src.width
        raster_height = src.height
        global_transform = src.transform
        crs_str = str(src.crs) if src.crs else None

        for y_offset in range(0, raster_height, passo):
            for x_offset in range(0, raster_width, passo):
                tile_w = min(tamanho_fatia, raster_width - x_offset)
                tile_h = min(tamanho_fatia, raster_height - y_offset)

                window = Window(x_offset, y_offset, tile_w, tile_h)
                data = src.read(window=window)

                img_pil = Image.fromarray(_to_rgb_uint8(data))

                # Affine that maps tile pixel (0, 0) to the real-world coordinate
                # of global pixel (x_offset, y_offset).
                tile_transform = global_transform * Affine.translation(x_offset, y_offset)

                meta = {
                    "x_offset": x_offset,
                    "y_offset": y_offset,
                    "tile_width": tile_w,
                    "tile_height": tile_h,
                    "transform_fatia": tile_transform,
                    "crs": crs_str,
                }

                yield img_pil, meta


def _to_rgb_uint8(data: np.ndarray) -> np.ndarray:
    """Converts a (bands, H, W) rasterio array to an (H, W, 3) uint8 RGB array."""
    n_bands = data.shape[0]

    if n_bands >= 3:
        rgb = data[:3, :, :]
    else:
        # Grayscale → replicate to 3 channels
        rgb = np.repeat(data[:1, :, :], 3, axis=0)

    if rgb.dtype == np.uint8:
        return rgb.transpose(1, 2, 0)

    if rgb.dtype == np.uint16:
        # Bit-shift preserves relative values without float conversion overhead
        return (rgb >> 8).astype(np.uint8).transpose(1, 2, 0)

    # Float or other integer types: min-max stretch to full 8-bit range
    rgb = rgb.astype(np.float64)
    min_val = np.nanmin(rgb)
    max_val = np.nanmax(rgb)

    if max_val > min_val:
        rgb = (rgb - min_val) / (max_val - min_val) * 255.0
    else:
        rgb = np.zeros_like(rgb)

    return rgb.astype(np.uint8).transpose(1, 2, 0)
