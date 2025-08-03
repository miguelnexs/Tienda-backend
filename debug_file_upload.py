#!/usr/bin/env python
"""
Script para diagnosticar el procesamiento de archivos
"""

import requests
import json
import uuid
from PIL import Image, ImageDraw
import io

def test_file_upload_detailed():
    """Test detallado de subida de archivos"""
    print("🔍 Test Detallado de Subida de Archivos")
    print("=" * 50)
    
    # URL de Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/categorias/"
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 200), color='purple')
        draw = ImageDraw.Draw(img)
        draw.text((50, 90), "FILE TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Verificar que la imagen tiene contenido
        image_data = img_byte_arr.getvalue()
        print(f"📏 Tamaño de imagen: {len(image_data)} bytes")
        print(f"📏 Primeros bytes: {image_data[:20]}")
        
        # Datos de la categoría
        unique_id = str(uuid.uuid4())[:8]
        categoria_data = {
            'nombre': f'File Test {unique_id}',
            'descripcion': 'Test detallado de archivos',
            'activa': True,
            'orden': 999
        }
        
        # Preparar los datos
        files = {
            'imagen': ('file_test.jpg', img_byte_arr, 'image/jpeg')
        }
        
        print("📤 Enviando imagen a Render...")
        print(f"📤 Nombre del archivo: file_test.jpg")
        print(f"📤 Tipo de contenido: image/jpeg")
        print(f"📤 Tamaño del archivo: {len(image_data)} bytes")
        
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
            
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_simple_upload():
    """Test simple sin imagen"""
    print("\n🧪 Test Simple sin imagen")
    print("=" * 50)
    
    # URL de Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/categorias/"
    
    try:
        # Datos de la categoría sin imagen
        unique_id = str(uuid.uuid4())[:8]
        categoria_data = {
            'nombre': f'Simple Test {unique_id}',
            'descripcion': 'Test simple sin imagen',
            'activa': True,
            'orden': 999
        }
        
        print("📤 Enviando categoría sin imagen...")
        
        # Hacer la petición POST sin archivos
        response = requests.post(
            api_url, 
            data=categoria_data, 
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Categoría creada exitosamente!")
            result = response.json()
            print("📄 Respuesta:")
            print(json.dumps(result, indent=2))
            
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_different_file_format():
    """Test con formato de archivo diferente"""
    print("\n🧪 Test con formato diferente")
    print("=" * 50)
    
    # URL de Render
    api_url = "https://tienda-backend-ap-api.onrender.com/api/categorias/"
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (100, 100), color='orange')
        draw = ImageDraw.Draw(img)
        draw.text((20, 40), "PNG TEST", fill='white')
        
        # Convertir a bytes como PNG
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Verificar que la imagen tiene contenido
        image_data = img_byte_arr.getvalue()
        print(f"📏 Tamaño de imagen PNG: {len(image_data)} bytes")
        
        # Datos de la categoría
        unique_id = str(uuid.uuid4())[:8]
        categoria_data = {
            'nombre': f'PNG Test {unique_id}',
            'descripcion': 'Test con formato PNG',
            'activa': True,
            'orden': 999
        }
        
        # Preparar los datos
        files = {
            'imagen': ('file_test.png', img_byte_arr, 'image/png')
        }
        
        print("📤 Enviando imagen PNG...")
        
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
            print("📄 Respuesta:")
            print(json.dumps(result, indent=2))
            
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 Diagnóstico de Subida de Archivos")
    print("=" * 50)
    
    # Test 1: Subida detallada
    test_file_upload_detailed()
    
    # Test 2: Sin imagen
    test_simple_upload()
    
    # Test 3: Formato diferente
    test_different_file_format()

if __name__ == "__main__":
    main() 