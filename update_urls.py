#!/usr/bin/env python
"""
Script para actualizar todas las URLs del backend de tienda-backend-api.onrender.com 
a tienda-backend-ap-api.onrender.com
"""

import os
import re
from pathlib import Path

def update_urls_in_file(file_path):
    """Actualiza las URLs en un archivo específico"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar la URL antigua por la nueva
        old_url = "tienda-backend-api.onrender.com"
        new_url = "tienda-backend-ap-api.onrender.com"
        
        if old_url in content:
            new_content = content.replace(old_url, new_url)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Actualizado: {file_path}")
            return True
        else:
            print(f"ℹ️  No se encontraron URLs para actualizar en: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error actualizando {file_path}: {e}")
        return False

def main():
    """Función principal"""
    print("🔄 Actualizando URLs del backend...")
    
    # Lista de archivos a actualizar
    files_to_update = [
        "test_render_env_vars.py",
        "test_render_cloudinary_direct.py",
        "test_debug_endpoint.py",
        "test_cors_upload.py",
        "test_cloudinary_render.py",
        "debug_render_cloudinary.py",
        "check_render_vars.py",
        "check_render_deployment.py",
        "setup_cloudinary.md",
        "RENDER_DEPLOYMENT.md",
        "CLOUDINARY_FIXES.md"
    ]
    
    updated_count = 0
    
    for filename in files_to_update:
        file_path = Path(filename)
        if file_path.exists():
            if update_urls_in_file(file_path):
                updated_count += 1
        else:
            print(f"⚠️  Archivo no encontrado: {filename}")
    
    print(f"\n✅ Actualización completada: {updated_count} archivos actualizados")

if __name__ == "__main__":
    main() 