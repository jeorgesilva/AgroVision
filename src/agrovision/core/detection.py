import os
import numpy as np
from pathlib import Path
from agrovision.models.yolo import WeedDetector as YoloWeedDetector
from agrovision.data.loaders import list_images
from agrovision.data.tilling import gerar_fatias_raster 

def run_batch_detection(model_path: str, input_path: str):
    detector = YoloWeedDetector(model_path)
    results = []
    
    caminho = Path(input_path)
    
    # SE FOR UM RASTER GIGANTE (.tif / .tiff)
    if caminho.is_file() and caminho.suffix.lower() in ['.tif', '.tiff']:
        print(f"🗺️ A processar ortomosaico gigante: {caminho.name}")
        
        # Fatiar com tamanho de 1024 e sobreposição de 15% (overlap)
        for img_pil, meta in gerar_fatias_raster(str(caminho), tamanho_fatia=512, sobreposicao=0.15):
            # Cria um ID para sabermos de onde veio esta fatia
            meta["tile_id"] = f"{caminho.stem}_x{meta['x_offset']}_y{meta['y_offset']}"
            
            # Para JSON serializar o Transform, convertemos para uma lista de 6 elementos [a, b, c, d, e, f]
            t = meta["transform_fatia"]
            meta["transform_matrix"] = [t.a, t.b, t.c, t.d, t.e, t.f]
            del meta["transform_fatia"] # Remove o objeto não-serializável
            
            pred = detector.detect(img_pil, metadata=meta)
            
            # Opcional: Só guardar no JSON se encontrou alguma daninha (poupa muito espaço!)
            if pred["detections"]:
                results.append((meta["tile_id"], pred))
                
    # SE FOR UMA PASTA DE IMAGENS NORMAIS
    elif caminho.is_dir():
        print(f"📂 A processar diretório de imagens: {caminho.name}")
        images = list_images(input_path)
        for img in images:
            pred = detector.detect(str(img))
            results.append((img, pred))
            
    return results