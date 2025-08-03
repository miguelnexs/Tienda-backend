#!/usr/bin/env python
"""
Script para debuggear Cloudinary en Render
"""

import requests
import json
import uuid

def test_cloudinary_debug():
    """Probar Cloudinary con debug detallado"""
    print("🔍 Debuggeando Cloudinary en Render...")
    
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
    
    # Datos del producto con descripción larga
    product_data = {
        'nombre': f'Debug Cloudinary {unique_id}',
        'sku': f'DEBUG-{unique_id}',
        'slug': f'debug-cloudinary-{unique_id}',
        'precio': '99.99',
        'descripcion_corta': 'Debug de Cloudinary en Render',
        'descripcion_larga': 'Este es un producto de debug para verificar si Cloudinary está funcionando correctamente en Render después del redespliegue.',
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
            'imagen_principal': ('debug_cloudinary.jpg', open(image_path, 'rb'), 'image/jpeg')
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
        print(f"📄 Response Headers: {dict(response.headers)}")
        
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
                print("🎯 ¡Las variables de entorno están configuradas correctamente!")
            else:
                print("⚠️  URL local detectada")
                print("🔧 Cloudinary no está funcionando")
                print("❌ Las variables de entorno no están siendo reconocidas")
                
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

def check_render_logs():
    """Verificar si hay logs específicos de Cloudinary en Render"""
    print("\n📋 Verificando logs de Render...")
    
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

if __name__ == "__main__":
    import os
    
    # Verificar logs de Render
    check_render_logs()
    
    # Probar Cloudinary con debug
    test_cloudinary_debug() 