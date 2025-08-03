#!/usr/bin/env python
"""
Script para diagnosticar subidas a Cloudinary
"""

import requests
import json
import uuid
from PIL import Image, ImageDraw
import io

def test_cloudinary_upload_detailed():
    """Test detallado de subida a Cloudinary"""
    print("🔍 Test Detallado de Cloudinary")
    print("=" * 50)
    
    # URL de Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/categorias/"
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 200), color='green')
        draw = ImageDraw.Draw(img)
        draw.text((50, 90), "DEBUG TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Verificar que la imagen tiene contenido
        image_data = img_byte_arr.getvalue()
        print(f"📏 Tamaño de imagen: {len(image_data)} bytes")
        
        # Datos de la categoría
        unique_id = str(uuid.uuid4())[:8]
        categoria_data = {
            'nombre': f'Debug Test {unique_id}',
            'descripcion': 'Test detallado de Cloudinary',
            'activa': True,
            'orden': 999
        }
        
        # Preparar los datos
        files = {
            'imagen': ('debug_test.jpg', img_byte_arr, 'image/jpeg')
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
            print("✅ Categoría creada exitosamente!")
            result = response.json()
            
            # Imprimir toda la respuesta para debug
            print("📄 Respuesta completa:")
            print(json.dumps(result, indent=2))
            
            categoria = result.get('categoria', {})
            imagen_url = categoria.get('imagen_url', '')
            imagen_directa = categoria.get('imagen', '')
            
            print(f"\n🔗 URLs generadas:")
            print(f"   imagen_url: {imagen_url}")
            print(f"   imagen: {imagen_directa}")
            
            # Verificar si las URLs son de Cloudinary
            if imagen_url and 'cloudinary.com' in imagen_url:
                print("✅ URL de Cloudinary detectada en imagen_url")
                
                # Probar si la URL es accesible
                print("🔍 Probando acceso a la URL...")
                try:
                    img_response = requests.get(imagen_url, timeout=10)
                    print(f"   Status: {img_response.status_code}")
                    if img_response.status_code == 200:
                        print("✅ La imagen es accesible")
                    else:
                        print("❌ La imagen no es accesible")
                except Exception as e:
                    print(f"❌ Error accediendo a la imagen: {e}")
                    
            elif imagen_directa and 'cloudinary.com' in imagen_directa:
                print("✅ URL de Cloudinary detectada en imagen")
            else:
                print("⚠️  No se detectaron URLs de Cloudinary")
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_existing_images():
    """Test de imágenes existentes"""
    print("\n📋 Verificando imágenes existentes...")
    
    # URL de Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/categorias/"
    
    try:
        # Hacer petición GET
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            categorias = data.get('results', [])
            
            print(f"📋 Categorías encontradas: {len(categorias)}")
            
            for categoria in categorias:
                nombre = categoria.get('nombre', '')
                imagen_url = categoria.get('imagen_url', '')
                
                if imagen_url:
                    print(f"\n📸 {nombre}:")
                    print(f"   URL: {imagen_url}")
                    
                    if 'cloudinary.com' in imagen_url:
                        print("   ✅ URL de Cloudinary")
                        
                        # Probar acceso
                        try:
                            img_response = requests.get(imagen_url, timeout=5)
                            if img_response.status_code == 200:
                                print("   ✅ Imagen accesible")
                            else:
                                print(f"   ❌ Error {img_response.status_code}")
                        except Exception as e:
                            print(f"   ❌ Error: {e}")
                    else:
                        print("   ⚠️  URL local")
                else:
                    print(f"\n📸 {nombre}: Sin imagen")
                    
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 Diagnóstico Detallado de Cloudinary")
    print("=" * 50)
    
    # Test 1: Subida detallada
    test_cloudinary_upload_detailed()
    
    # Test 2: Imágenes existentes
    test_existing_images()

if __name__ == "__main__":
    main() 