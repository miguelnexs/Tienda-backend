#!/usr/bin/env python
"""
Script para verificar variables de entorno en Render
"""

import requests
import json
import uuid

def check_render_environment_vars():
    """Verificar si las variables de entorno están activas en Render"""
    print("🔍 Verificando variables de entorno en Render...")
    
    # URL de la API en Render
    api_url = "https://tienda-backend-api.onrender.com/api/productos/productos/"
    
    try:
        # Hacer una petición simple para verificar el estado
        response = requests.get(api_url, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API funcionando correctamente")
            
            # Verificar headers específicos de Render
            headers = dict(response.headers)
            print(f"🆔 Render ID: {headers.get('rndr-id', 'No disponible')}")
            print(f"🖥️  Server: {headers.get('x-render-origin-server', 'No disponible')}")
            
            # Verificar si hay headers específicos de Cloudinary
            cloudinary_headers = [k for k in headers.keys() if 'cloudinary' in k.lower()]
            if cloudinary_headers:
                print(f"☁️ Headers de Cloudinary encontrados: {cloudinary_headers}")
            else:
                print("⚠️  No se encontraron headers específicos de Cloudinary")
                
        else:
            print(f"❌ API no responde correctamente: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error al verificar Render: {e}")

def test_cloudinary_after_redeploy():
    """Probar Cloudinary después del redespliegue"""
    print("\n☁️ Probando Cloudinary después del redespliegue...")
    
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
    
    # Datos del producto
    product_data = {
        'nombre': f'Test Post Redeploy {unique_id}',
        'sku': f'TEST-REDEPLOY-{unique_id}',
        'slug': f'test-post-redeploy-{unique_id}',
        'precio': '99.99',
        'descripcion_corta': 'Test después del redespliegue',
        'descripcion_larga': 'Este es un test para verificar si Cloudinary funciona después del redespliegue manual en Render.',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 10,
        'costo': '50.00'
    }
    
    print("📦 Datos del producto:")
    for key, value in product_data.items():
        print(f"   {key}: {value}")
    
    try:
        # Preparar los datos
        files = {
            'imagen_principal': ('test_redeploy.jpg', open(image_path, 'rb'), 'image/jpeg')
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
            print("✅ Producto creado exitosamente en Render!")
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
                print("🎯 ¡El redespliegue funcionó!")
            else:
                print("⚠️  URL local detectada")
                print("🔧 Cloudinary no está funcionando")
                print("❌ Las variables de entorno no están siendo reconocidas")
                print("💡 Posibles soluciones:")
                print("   1. Verificar que las variables estén configuradas en Render")
                print("   2. Hacer otro redespliegue manual")
                print("   3. Verificar que el código esté actualizado")
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en petición: {e}")

if __name__ == "__main__":
    import os
    
    # Verificar variables de entorno
    check_render_environment_vars()
    
    # Probar Cloudinary después del redespliegue
    test_cloudinary_after_redeploy() 