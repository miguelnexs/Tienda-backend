#!/usr/bin/env python
"""
Script para debuggear el problema del storage
"""

import os
import sys
import django
from pathlib import Path

# Forzar variables de entorno de Cloudinary
os.environ['CLOUDINARY_CLOUD_NAME'] = 'do1ntnlop'
os.environ['CLOUDINARY_API_KEY'] = '117225377115856'
os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import cloudinary

def debug_storage():
    """Debuggear el problema del storage"""
    print("🔍 Debuggeando configuración de storage...")
    
    # Verificar configuración
    print(f"🔧 DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    print(f"🔧 default_storage: {default_storage}")
    print(f"🔧 default_storage.__class__: {default_storage.__class__}")
    
    # Verificar si es Cloudinary
    if 'cloudinary' in str(default_storage.__class__).lower():
        print("✅ default_storage es Cloudinary")
    else:
        print("❌ default_storage NO es Cloudinary")
    
    # Probar subida directa
    print("\n🧪 Probando subida directa...")
    test_content = b"test content"
    test_file = ContentFile(test_content)
    
    try:
        # Intentar subir un archivo de prueba
        file_path = default_storage.save('test.txt', test_file)
        print(f"✅ Archivo subido: {file_path}")
        
        # Verificar URL
        file_url = default_storage.url(file_path)
        print(f"🌐 URL del archivo: {file_url}")
        
        # Verificar si es Cloudinary
        if 'cloudinary.com' in file_url:
            print("✅ ¡URL de Cloudinary detectada!")
        else:
            print("⚠️  URL local detectada")
            
        # Limpiar archivo de prueba
        default_storage.delete(file_path)
        print("🗑️  Archivo de prueba eliminado")
        
    except Exception as e:
        print(f"❌ Error en subida: {e}")
        import traceback
        traceback.print_exc()

def test_image_upload():
    """Probar subida de imagen específica"""
    print("\n🖼️  Probando subida de imagen...")
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\0fbfa4d6-958d-42c1-9db7-8c87784d28e6.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ La imagen no existe en: {image_path}")
        return
    
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # Crear archivo de prueba
        test_file = ContentFile(image_data)
        file_path = default_storage.save('test_image.jpg', test_file)
        
        print(f"✅ Imagen subida: {file_path}")
        
        # Obtener URL
        file_url = default_storage.url(file_path)
        print(f"🌐 URL de la imagen: {file_url}")
        
        # Verificar si es Cloudinary
        if 'cloudinary.com' in file_url:
            print("✅ ¡Imagen subida a Cloudinary!")
        else:
            print("⚠️  Imagen guardada localmente")
            
        # Limpiar
        default_storage.delete(file_path)
        print("🗑️  Imagen de prueba eliminada")
        
    except Exception as e:
        print(f"❌ Error subiendo imagen: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_storage()
    test_image_upload() 