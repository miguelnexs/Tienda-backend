#!/usr/bin/env python
"""
Test final de Cloudinary con imagen real
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

def test_cloudinary_with_image():
    """Prueba Cloudinary con una imagen real"""
    print("🔍 Probando Cloudinary con imagen real...")
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 200), color='blue')
        draw = ImageDraw.Draw(img)
        draw.text((50, 90), "FINAL TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Crear archivo de Django
        test_file = ContentFile(img_byte_arr.getvalue(), name="test_final.jpg")
        
        # Guardar usando Django storage
        saved_path = default_storage.save("test_final_cloudinary.jpg", test_file)
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

def test_api_with_image():
    """Prueba la API con imagen"""
    print("\n🚀 Probando API con imagen...")
    
    # URL local
    api_url = "http://127.0.0.1:8000/api/categorias/"
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 300), color='green')
        draw = ImageDraw.Draw(img)
        draw.text((100, 140), "API FINAL TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Datos de la categoría
        unique_id = str(uuid.uuid4())[:8]
        categoria_data = {
            'nombre': f'Test Final Cloudinary {unique_id}',
            'descripcion': 'Categoría de prueba final',
            'activa': True,
            'orden': 999
        }
        
        # Preparar los datos
        files = {
            'imagen': ('test_final_api.jpg', img_byte_arr, 'image/jpeg')
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

def test_render_api():
    """Prueba la API de Render"""
    print("\n🌐 Probando API de Render...")
    
    # URL de Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/categorias/"
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 300), color='purple')
        draw = ImageDraw.Draw(img)
        draw.text((100, 140), "RENDER FINAL TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Datos de la categoría
        unique_id = str(uuid.uuid4())[:8]
        categoria_data = {
            'nombre': f'Test Render Final {unique_id}',
            'descripcion': 'Categoría de prueba en Render',
            'activa': True,
            'orden': 999
        }
        
        # Preparar los datos
        files = {
            'imagen': ('test_render_final.jpg', img_byte_arr, 'image/jpeg')
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
            print("✅ Categoría creada exitosamente en Render!")
            result = response.json()
            
            categoria = result.get('categoria', {})
            print(f"🆔 ID de la categoría: {categoria.get('id')}")
            print(f"📸 URL de imagen: {categoria.get('imagen_url')}")
            
            # Verificar si la URL es de Cloudinary
            imagen_url = categoria.get('imagen_url', '')
            if 'cloudinary.com' in imagen_url:
                print("✅ ¡URL de Cloudinary detectada en Render!")
                return True
            else:
                print("⚠️  URL local detectada en Render")
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
    print("🚀 Test Final de Cloudinary")
    print("=" * 50)
    
    # Test 1: Cloudinary local con imagen
    local_ok = test_cloudinary_with_image()
    
    # Test 2: API local con imagen
    api_local_ok = test_api_with_image()
    
    # Test 3: API de Render
    render_ok = test_render_api()
    
    print("\n" + "=" * 50)
    print("📊 Resumen:")
    print(f"   Cloudinary local: {'✅ OK' if local_ok else '❌ Error'}")
    print(f"   API local: {'✅ OK' if api_local_ok else '❌ Error'}")
    print(f"   API Render: {'✅ OK' if render_ok else '❌ Error'}")
    
    if local_ok and api_local_ok and render_ok:
        print("🎉 ¡Cloudinary está funcionando correctamente en todos los entornos!")
    else:
        print("⚠️  Hay problemas que necesitan corrección")

if __name__ == "__main__":
    main() 