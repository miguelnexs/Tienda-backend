#!/usr/bin/env python
"""
Script simple para verificar que las URLs importantes han sido actualizadas
"""

import os
import re
from pathlib import Path

def check_urls_in_file(file_path):
    """Verifica las URLs en un archivo específico"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar URLs antiguas
        old_url_pattern = r'tienda-backend-api\.onrender\.com'
        old_urls = re.findall(old_url_pattern, content)
        
        # Buscar URLs nuevas
        new_url_pattern = r'tienda-backend-ap-api\.onrender\.com'
        new_urls = re.findall(new_url_pattern, content)
        
        if old_urls:
            print(f"❌ {file_path}: {len(old_urls)} URLs antiguas encontradas")
            return False
        elif new_urls:
            print(f"✅ {file_path}: {len(new_urls)} URLs nuevas encontradas")
            return True
        else:
            print(f"ℹ️  {file_path}: No se encontraron URLs del backend")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando {file_path}: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 Verificando URLs actualizadas...")
    
    # Lista específica de archivos importantes a verificar
    important_files = [
        # Backend
        "test_cloudinary_complete.py",
        "test_render_upload.py",
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
        "CLOUDINARY_FIXES.md",
        "Backend/settings.py",
        
        # Frontend
        "../Frontend/src/renderer/src/api/apiConfig.js",
        "../Frontend/src/main/handlers/apiErrorHandler.js",
        "../Frontend/src/main/handlers/clienteHandlers.js",
        "../Frontend/src/main/handlers/pedidoHandlers.js",
        "../Frontend/src/main/handlers/ventaHandlers.js",
        "../Frontend/src/renderer/src/components/productos/ProductForm.jsx",
        
        # Vercel Frontend
        "../sobrio-estilo-tienda-main/src/services/ventaService.ts",
        "../sobrio-estilo-tienda-main/src/pages/CategoriaPage.tsx",
        "../sobrio-estilo-tienda-main/src/pages/ProductoDetalle.tsx",
        "../sobrio-estilo-tienda-main/src/hooks/useProductos.ts",
        "../sobrio-estilo-tienda-main/src/hooks/useCategorias.ts"
    ]
    
    total_files = 0
    correct_files = 0
    
    for file_path_str in important_files:
        file_path = Path(file_path_str)
        if file_path.exists():
            total_files += 1
            if check_urls_in_file(file_path):
                correct_files += 1
        else:
            print(f"⚠️  Archivo no encontrado: {file_path_str}")
    
    print(f"\n📊 Resumen:")
    print(f"   Total de archivos verificados: {total_files}")
    print(f"   Archivos correctos: {correct_files}")
    print(f"   Archivos con problemas: {total_files - correct_files}")
    
    if total_files == correct_files:
        print("✅ ¡Todas las URLs han sido actualizadas correctamente!")
    else:
        print("⚠️  Algunos archivos aún contienen URLs antiguas")

if __name__ == "__main__":
    main() 