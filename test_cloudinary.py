#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración de Cloudinary
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

def test_cloudinary_storage():
    """Probar el storage de Cloudinary"""
    print("🧪 Probando configuración de Cloudinary...")
    
    try:
        # Crear una imagen de prueba
        img = Image.new('RGB', (100, 100), color='red')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear un archivo de prueba
        test_content = ContentFile(img_io.getvalue())
        test_name = "test_image.jpg"
        
        print(f"📤 Intentando subir archivo de prueba: {test_name}")
        
        # Intentar guardar
        saved_name = default_storage.save(test_name, test_content)
        print(f"✅ Archivo guardado como: {saved_name}")
        
        # Verificar si existe
        exists = default_storage.exists(saved_name)
        print(f"🔍 Archivo existe: {exists}")
        
        # Obtener URL
        url = default_storage.url(saved_name)
        print(f"🔗 URL del archivo: {url}")
        
        # Obtener tamaño
        size = default_storage.size(saved_name)
        print(f"📏 Tamaño del archivo: {size} bytes")
        
        # Eliminar archivo de prueba
        deleted = default_storage.delete(saved_name)
        print(f"🗑️ Archivo eliminado: {deleted}")
        
        print("✅ Prueba completada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

if __name__ == "__main__":
    success = test_cloudinary_storage()
    if success:
        print("\n🎉 ¡Cloudinary configurado correctamente!")
    else:
        print("\n💥 Error en la configuración de Cloudinary")
        sys.exit(1) 