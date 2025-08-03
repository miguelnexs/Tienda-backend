#!/usr/bin/env python
"""
Script simple para probar Cloudinary
"""

import os
import sys
import django
from django.conf import settings

def test_simple_cloudinary():
    """Probar configuración simple de Cloudinary"""
    print("🔧 Probando configuración simple de Cloudinary...")
    
    # Configurar variables de entorno
    os.environ['RENDER'] = 'true'
    os.environ['CLOUDINARY_CLOUD_NAME'] = 'do1ntnlop'
    os.environ['CLOUDINARY_API_KEY'] = '117225377115856'
    os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
    django.setup()
    
    print(f"\n📋 Variables de entorno:")
    print(f"RENDER: {os.environ.get('RENDER')}")
    print(f"CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME')}")
    
    print(f"\n🔧 Configuración de Django:")
    print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No definida')}")
    print(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'No definida')}")
    
    # Verificar si CLOUDINARY está configurado
    if hasattr(settings, 'CLOUDINARY'):
        print(f"\n☁️ Configuración de Cloudinary:")
        print(f"cloud_name: {settings.CLOUDINARY.get('cloud_name')}")
        print(f"api_key: {settings.CLOUDINARY.get('api_key')}")
        print(f"api_secret: {settings.CLOUDINARY.get('api_secret')}")
    else:
        print("\n❌ CLOUDINARY no está configurado en settings")
    
    # Probar subida directa a Cloudinary
    try:
        import cloudinary
        import cloudinary.uploader
        
        print(f"\n🧪 Probando subida directa a Cloudinary...")
        
        # Crear un archivo de prueba
        test_content = b"test image content for cloudinary"
        
        # Intentar subir
        result = cloudinary.uploader.upload(
            test_content,
            public_id="test_simple_upload",
            resource_type="auto"
        )
        
        print(f"✅ Subida exitosa: {result.get('url', 'No URL')}")
        
    except Exception as e:
        print(f"❌ Error en subida directa: {e}")

if __name__ == "__main__":
    test_simple_cloudinary() 