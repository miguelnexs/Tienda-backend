#!/usr/bin/env python
"""
Script para probar Cloudinary localmente
"""

import os
import sys
import django
from pathlib import Path
import requests
import json
import uuid
from PIL import Image, ImageDraw
import io

# Configurar variables de entorno para testing local
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

def test_local_cloudinary():
    """Prueba Cloudinary localmente"""
    print("🔍 Probando Cloudinary localmente...")
    
    try:
        # Verificar configuración
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 200), color='blue')
        draw = ImageDraw.Draw(img)
        draw.text((50, 90), "LOCAL TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Crear archivo de Django
        test_file = ContentFile(img_byte_arr.getvalue(), name="test_local.jpg")
        
        # Guardar usando Django storage
        saved_path = default_storage.save("test_local_cloudinary.jpg", test_file)
        print(f"✅ Archivo guardado: {saved_path}")
        
        # Obtener URL
        url = default_storage.url(saved_path)
        print(f"📸 URL generada: {url}")
        
        # Verificar si es URL de Cloudinary
        if 'cloudinary.com' in url:
            print("✅ ¡URL de Cloudinary detectada!")
            return True
        else:
            print("⚠️  URL local detectada")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_local_api():
    """Prueba la API local"""
    print("\n🚀 Probando API local...")
    
    # URL local
    api_url = "http://127.0.0.1:8000/api/categorias/"
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 300), color='green')
        draw = ImageDraw.Draw(img)
        draw.text((100, 140), "LOCAL API TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Datos de la categoría
        unique_id = str(uuid.uuid4())[:8]
        categoria_data = {
            'nombre': f'Test Local Cloudinary {unique_id}',
            'descripcion': 'Categoría de prueba local',
            'activa': True,
            'orden': 999
        }
        
        # Preparar los datos
        files = {
            'imagen': ('test_local_api.jpg', img_byte_arr, 'image/jpeg')
        }
        
        # Hacer la petición POST
        response = requests.post(
            api_url, 
            data=categoria_data, 
            files=files, 
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Categoría creada exitosamente!")
            result = response.json()
            
            categoria = result.get('categoria', {})
            print(f"🆔 ID de la categoría: {categoria.get('id')}")
            print(f"📸 URL de imagen: {categoria.get('imagen_url')}")
            
            # Verificar si la URL es de Cloudinary
            imagen_url = categoria.get('imagen_url', '')
            if 'cloudinary.com' in imagen_url:
                print("✅ ¡URL de Cloudinary detectada!")
                return True
            else:
                print("⚠️  URL local detectada")
                return False
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en petición API: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Test de Cloudinary Local")
    print("=" * 50)
    
    # Test 1: Storage local
    storage_ok = test_local_cloudinary()
    
    # Test 2: API local
    api_ok = test_local_api()
    
    print("\n" + "=" * 50)
    print("📊 Resumen:")
    print(f"   Storage local: {'✅ OK' if storage_ok else '❌ Error'}")
    print(f"   API local: {'✅ OK' if api_ok else '❌ Error'}")
    
    if storage_ok and api_ok:
        print("🎉 ¡Cloudinary está funcionando correctamente localmente!")
        print("💡 Ahora puedes usar la aplicación local con Cloudinary")
    else:
        print("⚠️  Hay problemas con Cloudinary localmente")

if __name__ == "__main__":
    main() 