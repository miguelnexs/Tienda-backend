#!/usr/bin/env python
"""
Script para verificar las variables de entorno de Cloudinary en Render
"""

import os
import requests
import json

def check_render_environment():
    """Verifica las variables de entorno en Render"""
    print("🔍 Verificando variables de entorno en Render...")
    
    # URL de la API de Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/debug/environment/"
    
    try:
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API de Render responde correctamente")
            
            # Verificar variables de Cloudinary
            cloudinary_vars = {
                'CLOUDINARY_CLOUD_NAME': data.get('CLOUDINARY_CLOUD_NAME'),
                'CLOUDINARY_API_KEY': data.get('CLOUDINARY_API_KEY'),
                'CLOUDINARY_API_SECRET': data.get('CLOUDINARY_API_SECRET'),
            }
            
            print("\n📋 Variables de Cloudinary en Render:")
            for var_name, var_value in cloudinary_vars.items():
                if var_value:
                    print(f"   ✅ {var_name}: {var_value[:10]}...")
                else:
                    print(f"   ❌ {var_name}: No configurada")
            
            # Verificar si todas están configuradas
            all_configured = all(cloudinary_vars.values())
            
            if all_configured:
                print("\n✅ Todas las variables de Cloudinary están configuradas en Render")
                return True
            else:
                print("\n❌ Faltan variables de Cloudinary en Render")
                print("💡 Necesitas configurar las siguientes variables en Render:")
                print("   - CLOUDINARY_CLOUD_NAME")
                print("   - CLOUDINARY_API_KEY")
                print("   - CLOUDINARY_API_SECRET")
                return False
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando a Render: {e}")
        return False

def test_render_upload():
    """Prueba la subida de imagen a Render"""
    print("\n🚀 Probando subida de imagen a Render...")
    
    # URL de la API
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/productos/"
    
    try:
        # Crear imagen de prueba
        from PIL import Image, ImageDraw
        import io
        import uuid
        
        img = Image.new('RGB', (300, 300), color='purple')
        draw = ImageDraw.Draw(img)
        draw.text((100, 140), "RENDER TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Datos del producto
        unique_id = str(uuid.uuid4())[:8]
        product_data = {
            'nombre': f'Test Render Cloudinary {unique_id}',
            'sku': f'TEST-RENDER-{unique_id}',
            'slug': f'test-render-cloudinary-{unique_id}',
            'precio': '99.99',
            'descripcion_corta': 'Test de Cloudinary en Render',
            'descripcion_larga': 'Este es un producto de prueba para verificar que Cloudinary funciona correctamente en Render.',
            'tipo': 'fisico',
            'estado': 'publicado',
            'gestion_stock': True,
            'stock': 10,
            'costo': '50.00'
        }
        
        # Preparar los datos
        files = {
            'imagen_principal': ('test_render.jpg', img_byte_arr, 'image/jpeg')
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
                print("🎉 ¡Cloudinary está funcionando correctamente en Render!")
                return True
            else:
                print("⚠️  URL local detectada")
                print("❌ Cloudinary no está funcionando en Render")
                return False
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en petición API: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 Verificación de Cloudinary en Render")
    print("=" * 50)
    
    # Verificar variables de entorno
    env_ok = check_render_environment()
    
    if env_ok:
        # Probar subida
        upload_ok = test_render_upload()
        
        print("\n" + "=" * 50)
        print("📊 Resumen:")
        print(f"   Variables de entorno: {'✅ OK' if env_ok else '❌ Error'}")
        print(f"   Subida de imagen: {'✅ OK' if upload_ok else '❌ Error'}")
        
        if env_ok and upload_ok:
            print("🎉 ¡Cloudinary está funcionando correctamente en Render!")
        else:
            print("⚠️  Hay problemas con Cloudinary en Render")
    else:
        print("\n❌ No se pueden verificar las variables de entorno")

if __name__ == "__main__":
    main() 