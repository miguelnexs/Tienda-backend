#!/usr/bin/env python
"""
Script para probar si CORS está afectando la subida de archivos
"""

import os
import sys
import requests
import json
import uuid

def test_cors_upload():
    """Probar la subida con diferentes configuraciones de CORS"""
    print("🌐 Probando subida con configuración de CORS...")
    
    # URL de la API en Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/productos/"
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\0fbfa4d6-958d-42c1-9db7-8c87784d28e6.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ La imagen no existe en: {image_path}")
        return
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    # Crear datos únicos
    unique_id = str(uuid.uuid4())[:8]
    
    # Datos del producto
    product_data = {
        'nombre': f'Bolso CORS Test {unique_id}',
        'sku': f'BOLSO-CORS-{unique_id}',
        'slug': f'bolso-cors-test-{unique_id}',
        'precio': '79.99',
        'descripcion_corta': 'Bolso de prueba para verificar CORS',
        'descripcion_larga': 'Este es un bolso de prueba para verificar si CORS está afectando la subida de archivos.',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 40,
        'costo': '45.00'
    }
    
    print("📦 Datos del producto:")
    for key, value in product_data.items():
        print(f"   {key}: {value}")
    
    # Probar con diferentes headers de CORS
    test_cases = [
        {
            'name': 'Sin headers especiales',
            'headers': {}
        },
        {
            'name': 'Con Origin localhost',
            'headers': {
                'Origin': 'http://localhost:5173'
            }
        },
        {
            'name': 'Con Origin 127.0.0.1',
            'headers': {
                'Origin': 'http://127.0.0.1:5173'
            }
        },
        {
            'name': 'Con Content-Type multipart',
            'headers': {
                'Content-Type': 'multipart/form-data'
            }
        },
        {
            'name': 'Con headers completos',
            'headers': {
                'Origin': 'http://localhost:5173',
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        
        try:
            # Preparar los datos
            files = {
                'imagen_principal': ('bolso_cors.jpg', open(image_path, 'rb'), 'image/jpeg')
            }
            
            data = product_data.copy()
            # Cambiar SKU para cada test
            data['sku'] = f"BOLSO-CORS-{unique_id}-{i}"
            data['slug'] = f"bolso-cors-test-{unique_id}-{i}"
            
            # Hacer la petición POST
            response = requests.post(
                api_url, 
                data=data, 
                files=files, 
                headers=test_case['headers'],
                timeout=30
            )
            
            print(f"📡 Status Code: {response.status_code}")
            
            if response.status_code == 201:
                print("✅ Producto creado exitosamente!")
                result = response.json()
                print(f"🆔 ID del producto: {result.get('producto', {}).get('id')}")
                print(f"📸 URL de imagen: {result.get('producto', {}).get('imagen_principal_url')}")
                
                # Verificar si la URL es de Cloudinary
                image_url = result.get('producto', {}).get('imagen_principal_url', '')
                if 'cloudinary.com' in image_url:
                    print("✅ ¡URL de Cloudinary detectada!")
                else:
                    print("⚠️  URL local detectada")
                    
            elif response.status_code == 400:
                print("❌ Error 400 - Bad Request")
                print(f"📄 Error response: {response.text}")
                
            elif response.status_code == 403:
                print("❌ Error 403 - Forbidden (posible problema de CORS)")
                print(f"📄 Error response: {response.text}")
                
            elif response.status_code == 500:
                print("❌ Error 500 - Internal Server Error")
                print(f"📄 Error response: {response.text}")
                
            else:
                print(f"❌ Error {response.status_code}")
                print(f"📄 Error response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error en petición: {e}")
            import traceback
            traceback.print_exc()

def test_cors_preflight():
    """Probar preflight request de CORS"""
    print("\n🔍 Probando preflight request de CORS...")
    
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/productos/"
    
    try:
        # Hacer una petición OPTIONS (preflight)
        response = requests.options(
            api_url,
            headers={
                'Origin': 'http://localhost:5173',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'content-type'
            },
            timeout=10
        )
        
        print(f"📡 Preflight Status Code: {response.status_code}")
        print(f"📄 Preflight Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Preflight request exitoso")
        else:
            print("❌ Preflight request falló")
            
    except Exception as e:
        print(f"❌ Error en preflight request: {e}")

def test_simple_get():
    """Probar una petición GET simple"""
    print("\n🔍 Probando petición GET simple...")
    
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/productos/"
    
    try:
        response = requests.get(api_url, timeout=10)
        
        print(f"📡 GET Status Code: {response.status_code}")
        print(f"📄 GET Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ GET request exitoso")
        else:
            print("❌ GET request falló")
            
    except Exception as e:
        print(f"❌ Error en GET request: {e}")

if __name__ == "__main__":
    # Probar preflight request
    test_cors_preflight()
    
    # Probar GET simple
    test_simple_get()
    
    # Probar subida con diferentes configuraciones
    test_cors_upload() 