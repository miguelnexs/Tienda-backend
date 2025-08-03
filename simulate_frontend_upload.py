#!/usr/bin/env python
"""
Script para simular la subida de producto desde el frontend
"""

import os
import sys
import django
from pathlib import Path
import requests
import json

# Configurar variables de entorno ANTES de importar Django
os.environ['CLOUDINARY_CLOUD_NAME'] = 'do1ntnlop'
os.environ['CLOUDINARY_API_KEY'] = '117225377115856'
os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

def simulate_frontend_upload():
    """Simular la subida desde el frontend"""
    print("🎯 Simulando subida desde el frontend...")
    
    # URL de la API (como la usaría el frontend)
    api_url = "http://localhost:8000/api/productos/productos/"
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\0fbfa4d6-958d-42c1-9db7-8c87784d28e6.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ La imagen no existe en: {image_path}")
        return
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    # Datos del producto (como los enviaría el frontend)
    product_data = {
        'nombre': 'Bolso Frontend Test',
        'sku': 'BOLSO-FRONTEND-001',
        'slug': 'bolso-frontend-test',
        'precio': '49.99',
        'descripcion_corta': 'Bolso de prueba desde frontend',
        'descripcion_larga': 'Este es un bolso de prueba subido desde el frontend para verificar que Cloudinary funciona correctamente.',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 25,
        'costo': '30.00'
    }
    
    print("📦 Datos del producto:")
    for key, value in product_data.items():
        print(f"   {key}: {value}")
    
    try:
        # Preparar los datos como lo haría el frontend
        files = {
            'imagen_principal': ('bolso_frontend.jpg', open(image_path, 'rb'), 'image/jpeg')
        }
        
        data = product_data
        
        print(f"\n📡 Enviando petición POST a: {api_url}")
        print(f"📄 Datos: {data}")
        print(f"📁 Archivo: {image_path}")
        
        # Hacer la petición POST (como lo haría el frontend)
        response = requests.post(api_url, data=data, files=files)
        
        print(f"\n📡 Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        print(f"📄 Response Body: {response.text}")
        
        if response.status_code == 201:
            print("✅ Producto creado via API exitosamente!")
            result = response.json()
            print(f"🆔 ID del producto: {result.get('id')}")
            print(f"📸 URL de imagen: {result.get('imagen_principal_url')}")
            
            # Verificar si la URL es de Cloudinary
            image_url = result.get('imagen_principal_url', '')
            if 'cloudinary.com' in image_url:
                print("✅ ¡URL de Cloudinary detectada!")
                print(f"🔗 URL completa: {image_url}")
            else:
                print("⚠️  URL local detectada")
                print(f"🔗 URL: {image_url}")
                
        else:
            print("❌ Error creando producto via API")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en petición API: {e}")
        import traceback
        traceback.print_exc()

def test_existing_product():
    """Probar un producto existente"""
    print("\n🔍 Probando producto existente...")
    
    # URL para obtener productos
    api_url = "http://localhost:8000/api/productos/productos/"
    
    try:
        response = requests.get(api_url)
        
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Productos obtenidos: {len(products.get('results', []))}")
            
            # Mostrar el primer producto
            if products.get('results'):
                product = products['results'][0]
                print(f"📦 Primer producto: {product.get('nombre')}")
                print(f"📸 URL de imagen: {product.get('imagen_principal_url')}")
                
                # Verificar si la URL es de Cloudinary
                image_url = product.get('imagen_principal_url', '')
                if 'cloudinary.com' in image_url:
                    print("✅ ¡URL de Cloudinary detectada!")
                else:
                    print("⚠️  URL local detectada")
        else:
            print(f"❌ Error obteniendo productos: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error obteniendo productos: {e}")

if __name__ == "__main__":
    # Simular subida desde frontend
    simulate_frontend_upload()
    
    # Probar producto existente
    test_existing_product() 