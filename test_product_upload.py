#!/usr/bin/env python
"""
Script para probar la subida de un producto con imagen específica
"""

import os
import sys
import django
from pathlib import Path
import requests
import json
from django.core.files.uploadedfile import SimpleUploadedFile

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

def test_product_upload_with_image():
    """Prueba la subida de un producto con imagen específica"""
    print("🧪 Probando subida de producto con imagen...")
    
    # Verificar configuración de Cloudinary
    try:
        config = cloudinary.config()
        print(f"✅ Cloudinary configurado: {config.cloud_name}")
    except Exception as e:
        print(f"❌ Error configurando Cloudinary: {e}")
        return
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\0fbfa4d6-958d-42c1-9db7-8c87784d28e6.jpg"
    
    # Verificar que la imagen existe
    if not os.path.exists(image_path):
        print(f"❌ La imagen no existe en: {image_path}")
        return
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    # Leer la imagen
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        print(f"✅ Imagen leída: {len(image_data)} bytes")
    except Exception as e:
        print(f"❌ Error leyendo imagen: {e}")
        return
    
    # Crear un producto de prueba
    product_data = {
        'nombre': 'Bolso de Prueba Cloudinary',
        'sku': 'BOLSO-TEST-001',
        'precio': '29.99',
        'descripcion_corta': 'Bolso de prueba para testear Cloudinary',
        'descripcion_larga': 'Este es un bolso de prueba para verificar que Cloudinary funciona correctamente con la subida de imágenes.',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 10,
        'costo': '15.00'
    }
    
    print("📦 Datos del producto:")
    for key, value in product_data.items():
        print(f"   {key}: {value}")
    
    # Simular la subida usando la API de Django
    try:
        from productos.models import Producto
        from django.core.files.base import ContentFile
        
        # Crear el producto
        producto = Producto.objects.create(
            nombre=product_data['nombre'],
            sku=product_data['sku'],
            precio=product_data['precio'],
            descripcion_corta=product_data['descripcion_corta'],
            descripcion_larga=product_data['descripcion_larga'],
            tipo=product_data['tipo'],
            estado=product_data['estado'],
            gestion_stock=product_data['gestion_stock'],
            stock=product_data['stock'],
            costo=product_data['costo']
        )
        
        print(f"✅ Producto creado: {producto.nombre} (ID: {producto.id})")
        
        # Subir la imagen
        image_name = os.path.basename(image_path)
        producto.imagen_principal.save(image_name, ContentFile(image_data), save=True)
        
        print(f"✅ Imagen subida: {producto.imagen_principal.name}")
        
        # Obtener la URL de la imagen
        if producto.imagen_principal:
            image_url = producto.imagen_principal.url
            print(f"🌐 URL de la imagen: {image_url}")
            
            # Verificar si es una URL de Cloudinary
            if 'cloudinary.com' in image_url:
                print("✅ ¡La imagen se subió a Cloudinary correctamente!")
            else:
                print("⚠️  La imagen se guardó localmente (desarrollo)")
        
        return producto
        
    except Exception as e:
        print(f"❌ Error creando producto: {e}")
        return None

def test_api_upload():
    """Prueba la subida usando la API REST"""
    print("\n🌐 Probando subida via API REST...")
    
    # URL de la API
    api_url = "http://localhost:8000/api/productos/productos/"
    
    # Datos del producto
    product_data = {
        'nombre': 'Bolso API Test',
        'sku': 'BOLSO-API-001',
        'precio': '39.99',
        'descripcion_corta': 'Bolso de prueba via API',
        'descripcion_larga': 'Este es un bolso de prueba subido via API REST.',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 5,
        'costo': '20.00'
    }
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\0fbfa4d6-958d-42c1-9db7-8c87784d28e6.jpg"
    
    try:
        # Preparar los datos
        files = {
            'imagen_principal': ('bolso_test.jpg', open(image_path, 'rb'), 'image/jpeg')
        }
        
        data = product_data
        
        # Hacer la petición POST
        response = requests.post(api_url, data=data, files=files)
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Producto creado via API exitosamente!")
            result = response.json()
            print(f"🆔 ID del producto: {result.get('id')}")
            print(f"📸 URL de imagen: {result.get('imagen_principal_url')}")
        else:
            print("❌ Error creando producto via API")
            
    except Exception as e:
        print(f"❌ Error en petición API: {e}")

if __name__ == "__main__":
    # Probar subida directa
    producto = test_product_upload_with_image()
    
    # Probar subida via API (solo si el servidor está corriendo)
    # test_api_upload() 