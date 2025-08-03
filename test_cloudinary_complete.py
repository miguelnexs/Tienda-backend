#!/usr/bin/env python
"""
Script completo para probar Cloudinary en producción
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
    else:
        print(f"💻 Entorno: Desarrollo (Local)")
        
    if hasattr(settings, 'CLOUDINARY'):
        print(f"   ✅ CLOUDINARY configurado en settings")
    else:
        print(f"   ❌ CLOUDINARY no configurado en settings")
        
    if hasattr(settings, 'DEFAULT_FILE_STORAGE'):
        print(f"   ✅ DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    else:
        print(f"   ❌ DEFAULT_FILE_STORAGE no configurado")
    
    # Verificar configuración de Cloudinary
    try:
        config = cloudinary.config()
        print(f"☁️  Cloudinary configurado correctamente")
        print(f"   Cloud Name: {config.cloud_name}")
        print(f"   API Key: {config.api_key[:10]}...")
    except Exception as e:
        print(f"❌ Error configurando Cloudinary: {e}")

def test_cloudinary_upload():
    """Prueba la subida directa a Cloudinary"""
    print("\n🧪 Probando subida directa a Cloudinary...")
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 200), color='blue')
        draw = ImageDraw.Draw(img)
        draw.text((50, 90), "TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Subir a Cloudinary
        result = cloudinary.uploader.upload(
            img_byte_arr,
            folder="test",
            public_id=f"test_image_{uuid.uuid4().hex[:8]}",
            overwrite=True
        )
        
        print("✅ Imagen subida exitosamente!")
        print(f"   URL: {result['url']}")
        print(f"   Secure URL: {result['secure_url']}")
        
        return result['secure_url']
        
    except Exception as e:
        print(f"❌ Error subiendo imagen: {e}")
        return None

def test_django_storage():
    """Prueba el storage de Django"""
    print("\n📁 Probando storage de Django...")
    
    try:
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        print(f"Storage actual: {default_storage}")
        print(f"Clase del storage: {type(default_storage)}")
        
        # Crear archivo de prueba
        test_content = b"test content for cloudinary"
        test_file = ContentFile(test_content, name="test_cloudinary.txt")
        
        # Guardar archivo
        saved_path = default_storage.save("test_upload.txt", test_file)
        print(f"✅ Archivo guardado en: {saved_path}")
        
        # Verificar si existe
        exists = default_storage.exists(saved_path)
        print(f"Archivo existe: {exists}")
        
        if exists:
            # Obtener URL
            url = default_storage.url(saved_path)
            print(f"URL del archivo: {url}")
            
            # Verificar si es URL de Cloudinary
            if 'cloudinary.com' in url:
                print("✅ URL de Cloudinary detectada!")
            else:
                print("⚠️  URL local detectada")
        
    except Exception as e:
        print(f"❌ Error en storage de Django: {e}")

def test_api_upload():
    """Prueba la subida a través de la API"""
    print("\n🚀 Probando subida a través de la API...")
    
    # URL de la API
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/productos/"
    
    # Crear imagen de prueba
    img = Image.new('RGB', (300, 300), color='green')
    draw = ImageDraw.Draw(img)
    draw.text((100, 140), "API TEST", fill='white')
    
    # Convertir a bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    # Datos del producto
    unique_id = str(uuid.uuid4())[:8]
    product_data = {
        'nombre': f'Test Cloudinary API {unique_id}',
        'sku': f'TEST-{unique_id}',
        'slug': f'test-cloudinary-api-{unique_id}',
        'precio': '99.99',
        'descripcion_corta': 'Test de Cloudinary API',
        'descripcion_larga': 'Este es un producto de prueba para verificar que Cloudinary funciona correctamente a través de la API.',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 10,
        'costo': '50.00'
    }
    
    try:
        # Preparar los datos
        files = {
            'imagen_principal': ('test_api.jpg', img_byte_arr, 'image/jpeg')
        }
        
        # Hacer la petición POST
        response = requests.post(
            api_url, 
            data=product_data, 
            files=files, 
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Producto creado exitosamente!")
            result = response.json()
            
            producto = result.get('producto', {})
            print(f"🆔 ID del producto: {producto.get('id')}")
            print(f"📸 URL de imagen: {producto.get('imagen_principal_url')}")
            
            # Verificar si la URL es de Cloudinary
            image_url = producto.get('imagen_principal_url', '')
            if 'cloudinary.com' in image_url:
                print("✅ ¡URL de Cloudinary detectada!")
                print("🎉 ¡Cloudinary está funcionando correctamente!")
            else:
                print("⚠️  URL local detectada")
                print("❌ Cloudinary no está funcionando")
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en petición API: {e}")

def main():
    """Función principal"""
    print("🚀 Test completo de Cloudinary")
    print("=" * 50)
    
    # Test 1: Configuración
    test_cloudinary_config()
    
    # Test 2: Subida directa
    test_cloudinary_upload()
    
    # Test 3: Storage de Django
    test_django_storage()
    
    # Test 4: API
    test_api_upload()
    
    print("\n" + "=" * 50)
    print("✅ Test completado!")

if __name__ == "__main__":
    main() 