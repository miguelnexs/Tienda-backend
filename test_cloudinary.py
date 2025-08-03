#!/usr/bin/env python
"""
Script de prueba para verificar la configuración de Cloudinary
Ejecutar: python test_cloudinary.py
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from django.conf import settings
import cloudinary

def test_cloudinary_config():
    """Prueba la configuración de Cloudinary"""
    print("🔍 Verificando configuración de Cloudinary...")
    
    # Verificar variables de entorno
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
    api_key = os.environ.get('CLOUDINARY_API_KEY')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
    
    print(f"📋 Variables de entorno:")
    print(f"   Cloud Name: {'✅ Configurado' if cloud_name else '❌ No configurado'}")
    print(f"   API Key: {'✅ Configurado' if api_key else '❌ No configurado'}")
    print(f"   API Secret: {'✅ Configurado' if api_secret else '❌ No configurado'}")
    
    # Verificar configuración de Django
    if 'RENDER' in os.environ:
        print(f"🌐 Entorno: Producción (Render)")
        if hasattr(settings, 'CLOUDINARY'):
            print(f"   ✅ CLOUDINARY configurado en settings")
        else:
            print(f"   ❌ CLOUDINARY no configurado en settings")
            
        if hasattr(settings, 'DEFAULT_FILE_STORAGE'):
            print(f"   ✅ DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        else:
            print(f"   ❌ DEFAULT_FILE_STORAGE no configurado")
    else:
        print(f"💻 Entorno: Desarrollo (Local)")
        print(f"   📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
        print(f"   🌐 MEDIA_URL: {settings.MEDIA_URL}")
    
    # Verificar configuración de Cloudinary
    try:
        config = cloudinary.config()
        print(f"☁️  Cloudinary configurado correctamente")
        print(f"   Cloud Name: {config.cloud_name}")
        print(f"   API Key: {config.api_key[:10]}...")
    except Exception as e:
        print(f"❌ Error configurando Cloudinary: {e}")
    
    print("\n" + "="*50)
    print("📝 Próximos pasos:")
    if not all([cloud_name, api_key, api_secret]):
        print("1. Configura las variables de entorno en Render")
        print("2. Redespliega tu aplicación")
    else:
        print("✅ Configuración lista para usar!")

if __name__ == "__main__":
    test_cloudinary_config() 