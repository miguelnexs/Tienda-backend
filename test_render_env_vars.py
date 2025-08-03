#!/usr/bin/env python
"""
Script para verificar variables de entorno en Render
"""

import requests
import json

def test_render_environment():
    """Verificar variables de entorno en Render"""
    print("🔍 Verificando variables de entorno en Render...")
    
    # URL de la API en Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/productos/"
    
    try:
        # Hacer una petición simple para verificar el estado
        response = requests.get(api_url, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API funcionando correctamente")
            
            # Verificar headers específicos de Render
            headers = dict(response.headers)
            if 'rndr-id' in headers:
                print(f"🆔 Render ID: {headers['rndr-id']}")
            if 'x-render-origin-server' in headers:
                print(f"🖥️  Server: {headers['x-render-origin-server']}")
                
            print("\n📋 Headers de respuesta:")
            for key, value in headers.items():
                if key.lower() in ['server', 'cf-ray', 'rndr-id', 'x-render-origin-server']:
                    print(f"   {key}: {value}")
                    
        else:
            print(f"❌ API no responde correctamente: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error al verificar Render: {e}")

def test_simple_product_creation():
    """Probar creación de producto simple para verificar configuración"""
    print("\n📦 Probando creación de producto simple...")
    
    # URL de la API en Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/productos/"
    
    # Datos del producto simple
    product_data = {
        'nombre': 'Test Env Vars',
        'sku': 'TEST-ENV-001',
        'slug': 'test-env-vars',
        'precio': '99.99',
        'descripcion_corta': 'Test para verificar variables de entorno',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 10,
        'costo': '50.00'
    }
    
    try:
        # Hacer la petición POST
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
            
            # Verificar si la URL es de Cloudinary
            image_url = producto.get('imagen_principal_url', '')
            if image_url and 'cloudinary.com' in image_url:
                print("✅ ¡URL de Cloudinary detectada!")
                print("🎉 ¡Cloudinary está funcionando correctamente!")
            elif image_url:
                print("⚠️  URL local detectada")
                print("🔧 Cloudinary no está funcionando")
            else:
                print("ℹ️  No hay imagen en este producto")
                
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
                if image_url and 'cloudinary.com' in image_url:
                    print("   ✅ URL de Cloudinary")
                elif image_url:
                    print("   ⚠️  URL local")
                else:
                    print("   ℹ️  Sin imagen")
        else:
            print(f"❌ Error al obtener productos: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error al verificar productos: {e}")

if __name__ == "__main__":
    # Verificar estado de Render
    test_render_environment()
    
    # Verificar productos existentes
    check_latest_products()
    
    # Probar creación de producto simple
    test_simple_product_creation() 