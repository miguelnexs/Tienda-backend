#!/usr/bin/env python
"""
Script para diagnosticar URLs de Cloudinary
"""

import os
import sys
import django
from pathlib import Path

# Configurar variables de entorno
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
from cloudinary_storage.storage import MediaCloudinaryStorage
import cloudinary

def debug_cloudinary_config():
    """Diagnostica la configuración de Cloudinary"""
    print("🔍 Diagnóstico de Cloudinary")
    print("=" * 50)
    
    # Verificar variables de entorno
    print("📋 Variables de entorno:")
    print(f"   CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME')}")
    print(f"   CLOUDINARY_API_KEY: {os.environ.get('CLOUDINARY_API_KEY')}")
    print(f"   CLOUDINARY_API_SECRET: {os.environ.get('CLOUDINARY_API_SECRET')}")
    
    # Verificar configuración de Django
    print("\n📋 Configuración de Django:")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    
    if hasattr(settings, 'CLOUDINARY'):
        print(f"   CLOUDINARY configurado: {settings.CLOUDINARY}")
    else:
        print("   ❌ CLOUDINARY no configurado en settings")
    
    if hasattr(settings, 'CLOUDINARY_STORAGE'):
        print(f"   CLOUDINARY_STORAGE configurado: {settings.CLOUDINARY_STORAGE}")
    else:
        print("   ❌ CLOUDINARY_STORAGE no configurado")
    
    # Verificar configuración de Cloudinary
    print("\n📋 Configuración de Cloudinary:")
    try:
        config = cloudinary.config()
        print(f"   Cloud Name: {config.cloud_name}")
        print(f"   API Key: {config.api_key}")
        print(f"   API Secret: {config.api_secret[:10]}...")
    except Exception as e:
        print(f"   ❌ Error configurando Cloudinary: {e}")
    
    # Verificar storage actual
    print("\n📋 Storage actual:")
    print(f"   Tipo: {type(default_storage)}")
    print(f"   Clase: {default_storage.__class__.__name__}")
    
    if isinstance(default_storage, MediaCloudinaryStorage):
        print("   ✅ Es MediaCloudinaryStorage")
    else:
        print("   ❌ No es MediaCloudinaryStorage")

def test_url_generation():
    """Prueba la generación de URLs"""
    print("\n🧪 Probando generación de URLs")
    print("=" * 50)
    
    try:
        # Crear archivo de prueba
        test_content = b"test content for cloudinary"
        test_file = ContentFile(test_content, name="test_debug.txt")
        
        # Guardar archivo
        saved_path = default_storage.save("test_debug.txt", test_file)
        print(f"✅ Archivo guardado: {saved_path}")
        
        # Obtener URL
        url = default_storage.url(saved_path)
        print(f"📸 URL generada: {url}")
        
        # Verificar tipo de URL
        if 'cloudinary.com' in url:
            print("✅ URL de Cloudinary detectada!")
            return True
        elif url.startswith('/media/'):
            print("⚠️  URL local detectada")
            print("💡 Esto indica que Cloudinary no está configurado correctamente")
            return False
        else:
            print(f"❓ URL desconocida: {url}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_cloudinary_storage_directly():
    """Prueba el storage de Cloudinary directamente"""
    print("\n🔧 Probando MediaCloudinaryStorage directamente")
    print("=" * 50)
    
    try:
        # Crear storage de Cloudinary
        cloudinary_storage = MediaCloudinaryStorage()
        
        # Crear archivo de prueba
        test_content = b"test content for direct cloudinary"
        test_file = ContentFile(test_content, name="test_direct.txt")
        
        # Guardar archivo
        saved_path = cloudinary_storage.save("test_direct.txt", test_file)
        print(f"✅ Archivo guardado: {saved_path}")
        
        # Obtener URL
        url = cloudinary_storage.url(saved_path)
        print(f"📸 URL generada: {url}")
        
        # Verificar tipo de URL
        if 'cloudinary.com' in url:
            print("✅ URL de Cloudinary detectada!")
            return True
        else:
            print("⚠️  URL local detectada")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Diagnóstico de URLs de Cloudinary")
    print("=" * 50)
    
    # Diagnóstico de configuración
    debug_cloudinary_config()
    
    # Test 1: Generación de URLs
    url_ok = test_url_generation()
    
    # Test 2: Storage directo
    direct_ok = test_cloudinary_storage_directly()
    
    print("\n" + "=" * 50)
    print("📊 Resumen:")
    print(f"   Generación de URLs: {'✅ OK' if url_ok else '❌ Error'}")
    print(f"   Storage directo: {'✅ OK' if direct_ok else '❌ Error'}")
    
    if url_ok and direct_ok:
        print("🎉 ¡Cloudinary está funcionando correctamente!")
    else:
        print("⚠️  Hay problemas con la configuración de Cloudinary")

if __name__ == "__main__":
    main() 