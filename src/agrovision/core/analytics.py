import logging

import matplotlib

matplotlib.use("Agg")  # must be set before pyplot is imported

import os

import geopandas as gpd
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show as raster_show

logger = logging.getLogger(__name__)

plt.style.use("ggplot")

_M2_PER_HECTARE = 10_000.0


def _compute_areas_m2(grid_gdf: gpd.GeoDataFrame) -> tuple[float, float]:
    """Returns (total_area_m2, sprayed_area_m2) in square metres.

    GeoDataFrames coming from create_vra_grid() are in WGS84 (EPSG:4326).
    Calling .area on geographic coordinates yields degrees², not m², which
    makes any hectare conversion nonsensical.  This function reprojects to a
    local UTM zone before computing area so the result is always in m².

    If the GDF is already in a projected metric CRS it is used as-is, so the
    function is safe to call regardless of the upstream CRS.
    """
    if grid_gdf.crs is None:
        raise ValueError(
            "GeoDataFrame has no CRS set — cannot compute area. "
            "Ensure create_vra_grid() preserves the source CRS."
        )

    if grid_gdf.empty:
        return 0.0, 0.0

    if grid_gdf.crs.is_geographic:
        grid_metric = grid_gdf.to_crs(grid_gdf.estimate_utm_crs())
    else:
        grid_metric = grid_gdf

    total_m2 = float(grid_metric.area.sum())
    sprayed_m2 = float(grid_metric[grid_metric["spray_action"] == 1].area.sum())

    return total_m2, sprayed_m2


def generate_report_material(grid_gdf: gpd.GeoDataFrame, ortho_path: str, output_dir: str) -> dict:
    os.makedirs(output_dir, exist_ok=True)

    # 1. Área em m² com CRS métrico — corrige o bug de cálculo em graus²
    total_m2, sprayed_m2 = _compute_areas_m2(grid_gdf)
    economy_pct = (1.0 - sprayed_m2 / total_m2) * 100.0 if total_m2 > 0 else 0.0

    sprayed_gdf = grid_gdf[grid_gdf["spray_action"] == 1]
    saved_m2 = max(0.0, total_m2 - sprayed_m2)

    # --- 2. Gráfico de Pizza (Economia) ---
    try:
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        ax1.pie(
            [sprayed_m2, saved_m2],
            labels=["Pulverizado", "Economizado"],
            autopct="%1.1f%%",
            colors=["#ff4d4d", "#2ecc71"],
        )
        ax1.set_title("Economia de Insumos")
        fig1.savefig(os.path.join(output_dir, "grafico_economia.png"))
        plt.close(fig1)
    except Exception as e:
        logger.warning("Failed to generate pie chart: %s", e)

    # --- 3. Mapa estático de prescrição ---
    try:
        fig2, ax2 = plt.subplots(figsize=(12, 12))

        with rasterio.open(ortho_path) as src:
            raster_show(src, ax=ax2, alpha=0.8, adjust=True)

            if not sprayed_gdf.empty:
                sprayed_gdf.to_crs(src.crs).plot(
                    ax=ax2, color="red", alpha=0.4, edgecolor="darkred", linewidth=0.5
                )

        ax2.set_aspect("equal", adjustable="datalim")
        plt.axis("off")
        fig2.savefig(
            os.path.join(output_dir, "mapa_estatico_prescricao.png"),
            dpi=150,
            bbox_inches="tight",
        )
        plt.close(fig2)
    except Exception as e:
        logger.warning("Failed to generate static map: %s", e)
        fig_err, ax_err = plt.subplots()
        ax_err.text(0.5, 0.5, "Mapa indisponível para arquivos gigantes", ha="center")
        fig_err.savefig(os.path.join(output_dir, "mapa_estatico_prescricao.png"))
        plt.close(fig_err)

    return {
        "total_ha": total_m2 / _M2_PER_HECTARE,
        "sprayed_ha": sprayed_m2 / _M2_PER_HECTARE,
        "economy_pct": economy_pct,
    }
