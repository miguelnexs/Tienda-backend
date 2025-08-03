#!/usr/bin/env python
"""
Script para forzar la configuración correcta de Cloudinary
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
import cloudinary
from cloudinary_storage.storage import MediaCloudinaryStorage

def force_cloudinary_config():
    """Fuerza la configuración correcta de Cloudinary"""
    print("🔧 Forzando configuración de Cloudinary...")
    
    # Configurar Cloudinary directamente
    cloudinary.config(
        cloud_name='do1ntnlop',
        api_key='117225377115856',
        api_secret='e0YSrk3sT_70-ijM6mwdFBIWP9w'
    )
    
    print("✅ Cloudinary configurado directamente")
    
    # Verificar configuración
    try:
        config = cloudinary.config()
        print(f"☁️  Cloudinary configurado: {config.cloud_name}")
    except Exception as e:
        print(f"❌ Error configurando Cloudinary: {e}")
        return False
    
    return True

def test_cloudinary_storage():
    """Prueba el storage de Cloudinary"""
    print("\n📁 Probando storage de Cloudinary...")
    
    try:
        # Crear storage de Cloudinary
        cloudinary_storage = MediaCloudinaryStorage()
        
        # Crear archivo de prueba
        test_content = b"test content for cloudinary storage"
        test_file = ContentFile(test_content, name="test_cloudinary_storage.txt")
        
        # Guardar archivo usando Cloudinary storage
        saved_path = cloudinary_storage.save("test_cloudinary_storage.txt", test_file)
        print(f"✅ Archivo guardado en Cloudinary: {saved_path}")
        
        # Verificar si existe
        exists = cloudinary_storage.exists(saved_path)
        print(f"Archivo existe en Cloudinary: {exists}")
        
        if exists:
            # Obtener URL
            url = cloudinary_storage.url(saved_path)
            print(f"URL del archivo: {url}")
            
            # Verificar si es URL de Cloudinary
            if 'cloudinary.com' in url:
                print("✅ URL de Cloudinary detectada!")
                return True
            else:
                print("⚠️  URL local detectada")
                return False
        
    except Exception as e:
        print(f"❌ Error en storage de Cloudinary: {e}")
        return False

def test_direct_upload():
    """Prueba la subida directa a Cloudinary"""
    print("\n🧪 Probando subida directa a Cloudinary...")
    
    try:
        # Crear imagen de prueba
        from PIL import Image, ImageDraw
        import io
        import uuid
        
        img = Image.new('RGB', (200, 200), color='red')
        draw = ImageDraw.Draw(img)
        draw.text((50, 90), "FORCE", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Subir a Cloudinary
        result = cloudinary.uploader.upload(
            img_byte_arr,
            folder="force_test",
            public_id=f"force_test_{uuid.uuid4().hex[:8]}",
            overwrite=True
        )
        
        print("✅ Imagen subida exitosamente!")
        print(f"   URL: {result['url']}")
        print(f"   Secure URL: {result['secure_url']}")
        
        return result['secure_url']
        
    except Exception as e:
        print(f"❌ Error subiendo imagen: {e}")
        return None

def main():
    """Función principal"""
    print("🚀 Forzando configuración de Cloudinary")
    print("=" * 50)
    
    # Forzar configuración
    config_ok = force_cloudinary_config()
    
    if config_ok:
        # Test 1: Storage de Cloudinary
        storage_ok = test_cloudinary_storage()
        
        # Test 2: Subida directa
        direct_ok = test_direct_upload()
        
        print("\n" + "=" * 50)
        print("📊 Resumen:")
        print(f"   Configuración: {'✅ OK' if config_ok else '❌ Error'}")
        print(f"   Storage Cloudinary: {'✅ OK' if storage_ok else '❌ Error'}")
        print(f"   Subida directa: {'✅ OK' if direct_ok else '❌ Error'}")
        
        if config_ok and storage_ok and direct_ok:
            print("🎉 ¡Cloudinary está funcionando correctamente!")
        else:
            print("⚠️  Hay problemas con Cloudinary que necesitan corrección")
    else:
        print("❌ No se pudo configurar Cloudinary")

if __name__ == "__main__":
    main() 