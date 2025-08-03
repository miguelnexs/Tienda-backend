#!/usr/bin/env python
"""
Script para probar directamente Cloudinary en Render
"""

import requests
import json
import uuid

def test_cloudinary_direct():
    """Probar Cloudinary directamente en Render"""
    print("☁️ Probando Cloudinary directamente en Render...")
    
    # URL de la API en Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/productos/"
    
    # Crear datos únicos
    unique_id = str(uuid.uuid4())[:8]
    
    # Datos del producto (sin imagen por ahora)
    product_data = {
        'nombre': f'Test Cloudinary Direct {unique_id}',
        'sku': f'TEST-CLOUD-{unique_id}',
        'slug': f'test-cloudinary-direct-{unique_id}',
        'precio': '99.99',
        'descripcion_corta': 'Test directo de Cloudinary',
        'descripcion_larga': 'Test directo para verificar configuración de Cloudinary',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 10,
        'costo': '60.00'
    }
    
    print("📦 Datos del producto:")
    for key, value in product_data.items():
        print(f"   {key}: {value}")
    
    try:
        print("🚀 Enviando petición POST sin imagen...")
        
        # Hacer la petición POST sin imagen
        response = requests.post(
            api_url, 
            data=product_data, 
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Producto creado exitosamente!")
            result = response.json()
            
            producto = result.get('producto', {})
            print(f"🆔 ID del producto: {producto.get('id')}")
            print(f"📸 URL de imagen: {producto.get('imagen_principal_url')}")
            print(f"🌐 URL completa: {producto.get('imagen_url')}")
            
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en petición: {e}")

def test_cloudinary_with_image():
    """Probar Cloudinary con imagen"""
    print("\n📸 Probando Cloudinary con imagen...")
    
    # URL de la API en Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/productos/"
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\0fbfa4d6-958d-42c1-9db7-8c87784d28e6.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ La imagen no existe en: {image_path}")
        return
    
    # Crear datos únicos
    unique_id = str(uuid.uuid4())[:8]
    
    # Datos del producto
    product_data = {
        'nombre': f'Test Cloudinary Image {unique_id}',
        'sku': f'TEST-IMG-{unique_id}',
        'slug': f'test-cloudinary-image-{unique_id}',
        'precio': '129.99',
        'descripcion_corta': 'Test de Cloudinary con imagen',
        'descripcion_larga': 'Test para verificar si Cloudinary funciona con imágenes',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 15,
        'costo': '80.00'
    }
    
    try:
        # Preparar los datos
        files = {
            'imagen_principal': ('test_cloudinary.jpg', open(image_path, 'rb'), 'image/jpeg')
        }
        
        print("🚀 Enviando petición POST con imagen...")
        
        # Hacer la petición POST
        response = requests.post(
            api_url, 
            data=product_data, 
            files=files, 
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Producto con imagen creado exitosamente!")
            result = response.json()
            
            producto = result.get('producto', {})
            print(f"🆔 ID del producto: {producto.get('id')}")
            print(f"📸 URL de imagen: {producto.get('imagen_principal_url')}")
            print(f"🌐 URL completa: {producto.get('imagen_url')}")
            
            # Verificar si la URL es de Cloudinary
            image_url = producto.get('imagen_principal_url', '')
            if 'cloudinary.com' in image_url:
                print("✅ ¡URL de Cloudinary detectada!")
                print("🎉 ¡Cloudinary está funcionando correctamente!")
            else:
                print("⚠️  URL local detectada")
                print("🔧 Cloudinary no está funcionando")
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en petición: {e}")

def check_latest_products():
    """Verificar los productos más recientes"""
    print("\n🔍 Verificando productos más recientes...")
    
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/productos/"
    
    try:
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            productos = data.get('results', [])
            
            print(f"📊 Total de productos: {len(productos)}")
            
            # Mostrar solo los últimos 3 productos
            for i, producto in enumerate(productos[:3]):
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
    import os
    
    # Verificar productos existentes
    check_latest_products()
    
    # Probar sin imagen
    test_cloudinary_direct()
    
    # Probar con imagen
    test_cloudinary_with_image() 