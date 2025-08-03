#!/usr/bin/env python
"""
Script para verificar que todas las URLs han sido actualizadas correctamente
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
    
    # Directorios a verificar
    directories = [
        "Backend",
        "../Frontend",
        "../sobrio-estilo-tienda-main"
    ]
    
    total_files = 0
    correct_files = 0
    
    for directory in directories:
        dir_path = Path(directory)
        if dir_path.exists():
            print(f"\n📁 Verificando directorio: {directory}")
            
            # Buscar archivos con extensiones específicas
            extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.md']
            
            for ext in extensions:
                for file_path in dir_path.rglob(f"*{ext}"):
                    if file_path.name not in ['update_urls.py', 'verify_urls.py']:  # Excluir scripts de actualización
                        total_files += 1
                        if check_urls_in_file(file_path):
                            correct_files += 1
    
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