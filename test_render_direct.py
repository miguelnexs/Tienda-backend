#!/usr/bin/env python
"""
Test directo de Cloudinary en Render
"""

import requests
import json
import uuid
from PIL import Image, ImageDraw
import io

def test_render_cloudinary_direct():
    """Prueba Cloudinary directamente en Render"""
    print("🌐 Test directo de Cloudinary en Render")
    print("=" * 50)
    
    # URL de Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/categorias/"
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 300), color='red')
        draw = ImageDraw.Draw(img)
        draw.text((100, 140), "RENDER DIRECT TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Datos de la categoría
        unique_id = str(uuid.uuid4())[:8]
        categoria_data = {
            'nombre': f'Test Render Direct {unique_id}',
            'descripcion': 'Test directo de Cloudinary en Render',
            'activa': True,
            'orden': 999
        }
        
        # Preparar los datos
        files = {
            'imagen': ('test_render_direct.jpg', img_byte_arr, 'image/jpeg')
        }
        
        print("📤 Enviando imagen a Render...")
        
        # Hacer la petición POST
        response = requests.post(
            api_url, 
            data=categoria_data, 
            files=files, 
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Categoría creada exitosamente en Render!")
            result = response.json()
            
            categoria = result.get('categoria', {})
            print(f"🆔 ID de la categoría: {categoria.get('id')}")
            print(f"📸 URL de imagen: {categoria.get('imagen_url')}")
            
            # Verificar si la URL es de Cloudinary
            imagen_url = categoria.get('imagen_url', '')
            if imagen_url:
                if 'cloudinary.com' in imagen_url:
                    print("✅ ¡URL de Cloudinary detectada en Render!")
                    print("🎉 ¡Cloudinary está funcionando correctamente en producción!")
                    return True
                else:
                    print("⚠️  URL local detectada en Render")
                    print("❌ Cloudinary no está funcionando en producción")
                    return False
            else:
                print("⚠️  No se generó URL de imagen")
                return False
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en petición API: {e}")
        return False

def test_render_existing_categories():
    """Verifica las categorías existentes en Render"""
    print("\n📋 Verificando categorías existentes en Render...")
    
    # URL de Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/categorias/"
    
    try:
        # Hacer petición GET
        response = requests.get(api_url, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            categorias = data.get('results', [])
            
            print(f"📋 Categorías encontradas: {len(categorias)}")
            
            # Verificar URLs de imágenes
            cloudinary_urls = 0
            local_urls = 0
            
            for categoria in categorias:
                imagen_url = categoria.get('imagen_url', '')
                if imagen_url:
                    if 'cloudinary.com' in imagen_url:
                        cloudinary_urls += 1
                        print(f"✅ {categoria.get('nombre')}: URL de Cloudinary")
                    else:
                        local_urls += 1
                        print(f"⚠️  {categoria.get('nombre')}: URL local")
            
            print(f"\n📊 Resumen:")
            print(f"   URLs de Cloudinary: {cloudinary_urls}")
            print(f"   URLs locales: {local_urls}")
            
            if cloudinary_urls > 0:
                print("✅ ¡Cloudinary está funcionando en Render!")
                return True
            else:
                print("❌ No se detectaron URLs de Cloudinary")
                return False
                
        else:
            print(f"❌ Error {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en petición API: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Test Directo de Cloudinary en Render")
    print("=" * 50)
    
    # Test 1: Verificar categorías existentes
    existing_ok = test_render_existing_categories()
    
    # Test 2: Crear nueva categoría
    create_ok = test_render_cloudinary_direct()
    
    print("\n" + "=" * 50)
    print("📊 Resumen:")
    print(f"   Categorías existentes: {'✅ OK' if existing_ok else '❌ Error'}")
    print(f"   Crear nueva categoría: {'✅ OK' if create_ok else '❌ Error'}")
    
    if existing_ok or create_ok:
        print("🎉 ¡Cloudinary está funcionando en Render!")
    else:
        print("⚠️  Cloudinary no está funcionando en Render")
        print("💡 Necesitas redesplegar la aplicación después de configurar las variables")

if __name__ == "__main__":
    main() 