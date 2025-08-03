#!/usr/bin/env python
"""
Script para probar la subida de producto a la API de Render en la nube
"""

import os
import sys
import requests
import json
import uuid

def test_render_upload():
    """Probar la subida a la API de Render"""
    print("🌐 Probando subida a la API de Render...")
    
    # URL de la API en Render
    api_url = "https://tienda-backend-api.onrender.com/api/productos/productos/"
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\0fbfa4d6-958d-42c1-9db7-8c87784d28e6.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ La imagen no existe en: {image_path}")
        return
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    # Crear datos únicos
    unique_id = str(uuid.uuid4())[:8]
    
    # Datos del producto (como los enviaría el frontend)
    product_data = {
        'nombre': f'Bolso Render Test {unique_id}',
        'sku': f'BOLSO-RENDER-{unique_id}',
        'slug': f'bolso-render-test-{unique_id}',
        'precio': '69.99',
        'descripcion_corta': 'Bolso de prueba en Render con Cloudinary',
        'descripcion_larga': 'Este es un bolso de prueba subido a la API de Render para verificar que Cloudinary funciona correctamente en producción.',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 35,
        'costo': '40.00'
    }
    
    print("📦 Datos del producto:")
    for key, value in product_data.items():
        print(f"   {key}: {value}")
    
    try:
        # Preparar los datos como lo haría el frontend
        files = {
            'imagen_principal': ('bolso_render.jpg', open(image_path, 'rb'), 'image/jpeg')
        }
        
        data = product_data
        
        print(f"\n📡 Enviando petición POST a: {api_url}")
        print(f"📄 Datos: {data}")
        print(f"📁 Archivo: {image_path}")
        
        # Hacer la petición POST (como lo haría el frontend)
        response = requests.post(api_url, data=data, files=files, timeout=30)
        
        print(f"\n📡 Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        print(f"📄 Response Body: {response.text}")
        
        if response.status_code == 201:
            print("✅ Producto creado via API de Render exitosamente!")
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
            print("❌ Error creando producto via API de Render")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en petición API: {e}")
        import traceback
        traceback.print_exc()

def test_render_products():
    """Probar productos existentes en Render"""
    print("\n🔍 Probando productos existentes en Render...")
    
    # URL para obtener productos
    api_url = "https://tienda-backend-api.onrender.com/api/productos/productos/"
    
    try:
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Productos obtenidos: {len(products.get('results', []))}")
            
            # Mostrar los primeros productos
            if products.get('results'):
                for i, product in enumerate(products['results'][:3]):
                    print(f"\n📦 Producto {i+1}: {product.get('nombre')}")
                    print(f"   ID: {product.get('id')}")
                    print(f"   SKU: {product.get('sku')}")
                    print(f"   Precio: {product.get('precio')}")
                    print(f"   URL de imagen: {product.get('imagen_principal_url')}")
                    
                    # Verificar si la URL es de Cloudinary
                    image_url = product.get('imagen_principal_url', '')
                    if 'cloudinary.com' in image_url:
                        print("   ✅ ¡URL de Cloudinary detectada!")
                    else:
                        print("   ⚠️  URL local detectada")
            else:
                print("❌ No hay productos disponibles")
        else:
            print(f"❌ Error obteniendo productos: {response.status_code}")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error obteniendo productos: {e}")
        import traceback
        traceback.print_exc()

def test_render_health():
    """Probar el estado de salud de la API"""
    print("\n🏥 Probando estado de salud de la API...")
    
    try:
        # Probar endpoint de salud (si existe)
        health_url = "https://tienda-backend-api.onrender.com/"
        response = requests.get(health_url, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ API de Render está funcionando correctamente")
        else:
            print("⚠️  API de Render responde pero con status diferente")
            
    except Exception as e:
        print(f"❌ Error conectando a la API: {e}")

if __name__ == "__main__":
    # Probar estado de salud
    test_render_health()
    
    # Probar productos existentes
    test_render_products()
    
    # Simular subida desde frontend
    test_render_upload() 