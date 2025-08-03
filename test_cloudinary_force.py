#!/usr/bin/env python
"""
Script para forzar el uso de Cloudinary en desarrollo
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
import cloudinary

def test_cloudinary_force():
    """Prueba forzar Cloudinary en desarrollo"""
    print("🔧 Forzando Cloudinary en desarrollo...")
    
    # Verificar variables de entorno
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
    api_key = os.environ.get('CLOUDINARY_API_KEY')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
    
    print(f"📋 Variables de entorno:")
    print(f"   Cloud Name: {cloud_name}")
    print(f"   API Key: {api_key}")
    print(f"   API Secret: {api_secret[:10]}...")
    
    # Verificar configuración de Django
    print(f"\n🔧 Configuración de Django:")
    print(f"   DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    print(f"   MEDIA_URL: {settings.MEDIA_URL}")
    print(f"   MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'No configurado')}")
    
    # Verificar configuración de Cloudinary
    try:
        config = cloudinary.config()
        print(f"\n☁️  Cloudinary configurado:")
        print(f"   Cloud Name: {config.cloud_name}")
        print(f"   API Key: {config.api_key[:10]}...")
    except Exception as e:
        print(f"❌ Error configurando Cloudinary: {e}")
    
    # Verificar si CLOUDINARY está en settings
    if hasattr(settings, 'CLOUDINARY'):
        print(f"\n✅ CLOUDINARY configurado en settings:")
        print(f"   {settings.CLOUDINARY}")
    else:
        print(f"\n❌ CLOUDINARY no configurado en settings")
    
    # Verificar la condición
    condition = 'RENDER' in os.environ or os.environ.get('CLOUDINARY_CLOUD_NAME')
    print(f"\n🔍 Condición de configuración:")
    print(f"   'RENDER' in os.environ: {'RENDER' in os.environ}")
    print(f"   os.environ.get('CLOUDINARY_CLOUD_NAME'): {os.environ.get('CLOUDINARY_CLOUD_NAME')}")
    print(f"   Condición resultante: {condition}")

if __name__ == "__main__":
    test_cloudinary_force() 