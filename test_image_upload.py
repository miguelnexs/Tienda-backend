#!/usr/bin/env python
"""
Script para probar la subida de imágenes a Cloudinary
"""

import os
import sys
import django
from pathlib import Path
import cloudinary.uploader

# Configurar variables de entorno con las credenciales correctas
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

def test_cloudinary_upload():
    """Prueba la subida de imágenes a Cloudinary"""
    print("🧪 Probando subida de imágenes a Cloudinary...")
    
    # Verificar configuración
    try:
        config = cloudinary.config()
        print(f"✅ Cloudinary configurado: {config.cloud_name}")
    except Exception as e:
        print(f"❌ Error configurando Cloudinary: {e}")
        return
    
    # Crear una imagen de prueba (texto simple)
    from PIL import Image, ImageDraw, ImageFont
    import io
    
    # Crear imagen de prueba
    img = Image.new('RGB', (200, 200), color='red')
    draw = ImageDraw.Draw(img)
    draw.text((50, 90), "TEST", fill='white')
    
    # Convertir a bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    try:
        # Subir a Cloudinary
        print("📤 Subiendo imagen de prueba...")
        result = cloudinary.uploader.upload(
            img_byte_arr,
            folder="test",
            public_id="test_image",
            overwrite=True
        )
        
        print("✅ Imagen subida exitosamente!")
        print(f"   URL: {result['url']}")
        print(f"   Public ID: {result['public_id']}")
        print(f"   Secure URL: {result['secure_url']}")
        
        return result['secure_url']
        
    except Exception as e:
        print(f"❌ Error subiendo imagen: {e}")
        return None

if __name__ == "__main__":
    test_cloudinary_upload() 