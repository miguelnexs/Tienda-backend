#!/usr/bin/env python
"""
Script para probar Cloudinary en Render después de configurar las variables de entorno
"""

import os
import sys
import requests
import json
import uuid

def test_cloudinary_render():
    """Probar la subida de imagen a Render con Cloudinary configurado"""
    print("☁️ Probando Cloudinary en Render después de configurar variables...")
    
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
        'nombre': f'Bolso Cloudinary Test {unique_id}',
        'sku': f'BOLSO-CLOUD-{unique_id}',
        'slug': f'bolso-cloudinary-test-{unique_id}',
        'precio': '89.99',
        'descripcion_corta': 'Bolso de prueba para verificar Cloudinary en Render',
        'descripcion_larga': 'Este es un bolso de prueba para verificar si Cloudinary está funcionando correctamente en Render después de configurar las variables de entorno.',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 50,
        'costo': '55.00'
    }
    
    print("📦 Datos del producto:")
    for key, value in product_data.items():
        print(f"   {key}: {value}")
    
    try:
        # Preparar los datos
        files = {
            'imagen_principal': ('bolso_cloudinary.jpg', open(image_path, 'rb'), 'image/jpeg')
        }
        
        print("🚀 Enviando petición POST a Render...")
        
        # Hacer la petición POST
        response = requests.post(
            api_url, 
            data=product_data, 
            files=files, 
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            print("✅ Producto creado exitosamente en Render!")
            result = response.json()
            
            # Extraer información del producto
            producto = result.get('producto', {})
            print(f"🆔 ID del producto: {producto.get('id')}")
            print(f"📸 URL de imagen: {producto.get('imagen_principal_url')}")
            print(f"🌐 URL completa: {producto.get('imagen_url')}")
            
            # Verificar si la URL es de Cloudinary
            image_url = producto.get('imagen_principal_url', '')
            if 'cloudinary.com' in image_url:
                print("✅ ¡URL de Cloudinary detectada! Cloudinary está funcionando correctamente.")
                print("🎉 ¡Las variables de entorno están configuradas correctamente!")
            else:
                print("⚠️  URL local detectada - Cloudinary no está funcionando")
                print("🔧 Verifica que las variables de entorno estén configuradas en Render")
                
        elif response.status_code == 400:
            print("❌ Error 400 - Bad Request")
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

def test_existing_products():
    """Verificar productos existentes en Render"""
    print("\n🔍 Verificando productos existentes en Render...")
    
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/productos/"
    
    try:
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            productos = data.get('results', [])
            
            print(f"📊 Total de productos: {len(productos)}")
            
            for i, producto in enumerate(productos[:3]):  # Solo los primeros 3
                print(f"\n📦 Producto {i+1}:")
                print(f"   Nombre: {producto.get('nombre')}")
                print(f"   SKU: {producto.get('sku')}")
                print(f"   URL imagen: {producto.get('imagen_principal_url')}")
                
                # Verificar si es URL de Cloudinary
                image_url = producto.get('imagen_principal_url', '')
                if 'cloudinary.com' in image_url:
                    print("   ✅ URL de Cloudinary")
                else:
                    print("   ⚠️  URL local")
        else:
            print(f"❌ Error al obtener productos: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error al verificar productos: {e}")

if __name__ == "__main__":
    # Verificar productos existentes
    test_existing_products()
    
    # Probar subida nueva
    test_cloudinary_render() 