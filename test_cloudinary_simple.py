#!/usr/bin/env python
"""
Test simple de Cloudinary en Render
"""

import requests
import json
import uuid
from PIL import Image, ImageDraw
import io

def test_cloudinary_simple():
    """Test simple de Cloudinary"""
    print("🌐 Test Simple de Cloudinary en Render")
    print("=" * 50)
    
    # URL de Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/categorias/"
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 200), color='blue')
        draw = ImageDraw.Draw(img)
        draw.text((50, 90), "SIMPLE TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Datos de la categoría
        unique_id = str(uuid.uuid4())[:8]
        categoria_data = {
            'nombre': f'Test Simple {unique_id}',
            'descripcion': 'Test simple de Cloudinary',
            'activa': True,
            'orden': 999
        }
        
        # Preparar los datos
        files = {
            'imagen': ('test_simple.jpg', img_byte_arr, 'image/jpeg')
        }
        
        print("📤 Enviando imagen...")
        
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
            
            if imagen_url:
                if 'cloudinary.com' in imagen_url:
                    print("✅ ¡URL de Cloudinary detectada!")
                    print("🎉 ¡Cloudinary está funcionando!")
                    return True
                else:
                    print("⚠️  URL local detectada")
                    print(f"URL: {imagen_url}")
                    return False
            else:
                print("⚠️  No se generó URL de imagen")
                return False
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Test Simple de Cloudinary")
    print("=" * 50)
    
    success = test_cloudinary_simple()
    
    if success:
        print("🎉 ¡Cloudinary está funcionando correctamente!")
    else:
        print("⚠️  Cloudinary no está funcionando")
        print("💡 Verifica la configuración en Render")

if __name__ == "__main__":
    main() 