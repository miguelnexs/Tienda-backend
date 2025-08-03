#!/usr/bin/env python
"""
Script para debuggear la configuración de Cloudinary en Render
"""

import os
import sys
import django
from django.conf import settings

def debug_cloudinary_settings():
    """Debuggear la configuración de Cloudinary"""
    print("🔍 Debuggeando configuración de Cloudinary...")
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
    django.setup()
    
    print("\n📋 Variables de entorno:")
    print(f"RENDER: {os.environ.get('RENDER', 'No definida')}")
    print(f"CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME', 'No definida')}")
    print(f"CLOUDINARY_API_KEY: {os.environ.get('CLOUDINARY_API_KEY', 'No definida')}")
    print(f"CLOUDINARY_API_SECRET: {os.environ.get('CLOUDINARY_API_SECRET', 'No definida')}")
    
    print("\n🔧 Configuración de Django:")
    print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No definida')}")
    print(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'No definida')}")
    print(f"MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'No definida')}")
    
    # Verificar si CLOUDINARY está configurado
    if hasattr(settings, 'CLOUDINARY'):
        print(f"\n☁️ Configuración de Cloudinary:")
        print(f"cloud_name: {settings.CLOUDINARY.get('cloud_name', 'No definida')}")
        print(f"api_key: {settings.CLOUDINARY.get('api_key', 'No definida')}")
        print(f"api_secret: {settings.CLOUDINARY.get('api_secret', 'No definida')}")
    else:
        print("\n❌ CLOUDINARY no está configurado en settings")
    
    # Verificar la condición de activación
    render_in_env = 'RENDER' in os.environ
    cloudinary_name_in_env = bool(os.environ.get('CLOUDINARY_CLOUD_NAME'))
    
    print(f"\n🎯 Condiciones de activación:")
    print(f"'RENDER' in os.environ: {render_in_env}")
    print(f"os.environ.get('CLOUDINARY_CLOUD_NAME'): {cloudinary_name_in_env}")
    print(f"Condición total: {render_in_env or cloudinary_name_in_env}")
    
    if render_in_env or cloudinary_name_in_env:
        print("✅ Cloudinary debería estar activo")
    else:
        print("❌ Cloudinary no debería estar activo")

def test_cloudinary_upload():
    """Probar subida directa a Cloudinary"""
    print("\n🧪 Probando subida directa a Cloudinary...")
    
    try:
        import cloudinary
        import cloudinary.uploader
        
        # Verificar configuración
        print(f"Cloudinary configurado: {cloudinary.config()}")
        
        # Crear un archivo de prueba
        test_content = b"test image content"
        
        # Intentar subir
        result = cloudinary.uploader.upload(
            test_content,
            public_id="test_upload",
            resource_type="auto"
        )
        
        print(f"✅ Subida exitosa: {result.get('url', 'No URL')}")
        
    except Exception as e:
        print(f"❌ Error en subida directa: {e}")

def test_django_storage():
    """Probar el storage de Django"""
    print("\n📁 Probando storage de Django...")
    
    try:
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        print(f"Storage actual: {default_storage}")
        print(f"Clase del storage: {type(default_storage)}")
        
        # Intentar guardar un archivo de prueba
        test_file = ContentFile(b"test content", name="test.txt")
        saved_path = default_storage.save("test_upload.txt", test_file)
        
        print(f"✅ Archivo guardado en: {saved_path}")
        
        # Verificar si existe
        exists = default_storage.exists(saved_path)
        print(f"Archivo existe: {exists}")
        
        if exists:
            # Obtener URL
            url = default_storage.url(saved_path)
            print(f"URL del archivo: {url}")
        
    except Exception as e:
        print(f"❌ Error en storage de Django: {e}")

if __name__ == "__main__":
    debug_cloudinary_settings()
    test_cloudinary_upload()
    test_django_storage() 