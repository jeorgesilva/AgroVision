import matplotlib.pyplot as plt
import geopandas as gpd
import os
import rasterio
from rasterio.plot import show as raster_show
import numpy as np

def generate_report_material(grid_gdf, ortho_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # IMPORTANTE: Forçar o backend 'Agg' para evitar erros de interface no servidor
    import matplotlib
    matplotlib.use('Agg')
    
    plt.style.use('ggplot')

    # 1. Cálculos de área
    total_area = grid_gdf.area.sum()
    sprayed_gdf = grid_gdf[grid_gdf['spray_action'] == 1]
    sprayed_area = sprayed_gdf.area.sum()
    economy = (1 - (sprayed_area / total_area)) * 100 if total_area > 0 else 0

    # --- 2. Gráfico de Pizza (Economia) ---
    try:
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        ax1.pie([sprayed_area, max(0, total_area - sprayed_area)], 
                labels=['Pulverizado', 'Economizado'], 
                autopct='%1.1f%%', colors=['#ff4d4d', '#2ecc71'])
        ax1.set_title("Economia de Insumos")
        fig1.savefig(os.path.join(output_dir, "grafico_economia.png"))
        plt.close(fig1)
    except Exception as e:
        print(f"⚠️ Erro no gráfico de pizza: {e}")

    # --- 3. MAPA ESTÁTICO (Onde o erro costuma ocorrer) ---
    try:
        # Definimos um tamanho fixo e forçamos o aspect ratio
        fig2, ax2 = plt.subplots(figsize=(12, 12))
        
        with rasterio.open(ortho_path) as src:
            # Usamos o 'extent' do próprio rasterio para garantir que o aspect seja finito
            extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]
            
            # Mostramos o raster com um limite de resolução para o relatório (não trava a RAM)
            raster_show(src, ax=ax2, alpha=0.8, adjust=True)
            
            if not sprayed_gdf.empty:
                # Reprojetar a grelha para o mesmo sistema do mapa
                grid_vis = sprayed_gdf.to_crs(src.crs)
                grid_vis.plot(ax=ax2, color='red', alpha=0.4, edgecolor='darkred', linewidth=0.5)
        
        # O segredo para evitar o erro de 'aspect':
        ax2.set_aspect('equal', adjustable='datalim')
        plt.axis('off')
        
        fig2.savefig(os.path.join(output_dir, "mapa_estatico_prescricao.png"), dpi=150, bbox_inches='tight')
        plt.close(fig2)
    except Exception as e:
        print(f"⚠️ Erro ao gerar mapa estático: {e}")
        # Se falhar, criamos uma imagem vazia para não quebrar o PDF
        fig_err, ax_err = plt.subplots()
        ax_err.text(0.5, 0.5, "Mapa indisponível para arquivos gigantes", ha='center')
        fig_err.savefig(os.path.join(output_dir, "mapa_estatico_prescricao.png"))
        plt.close(fig_err)

    return {
        "total_ha": total_area / 10000, 
        "sprayed_ha": sprayed_area / 10000, 
        "economy_pct": economy
    }