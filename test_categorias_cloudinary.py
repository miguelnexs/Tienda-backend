#!/usr/bin/env python
"""
Script para probar las categorías y verificar URLs de Cloudinary
"""

import os
import sys
import django
from pathlib import Path
import requests
import json
import uuid
from PIL import Image, ImageDraw
import io

# Configurar variables de entorno para testing
os.environ['CLOUDINARY_CLOUD_NAME'] = 'do1ntnlop'
os.environ['CLOUDINARY_API_KEY'] = '117225377115856'
os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from django.conf import settings
from categorias.models import CategoriaProducto
from categorias.serializers import CategoriaSerializer
from rest_framework.test import APIRequestFactory

def test_categoria_serializer():
    """Prueba el serializer de categorías localmente"""
    print("🔍 Probando serializer de categorías...")
    
    try:
        # Crear request factory
        factory = APIRequestFactory()
        request = factory.get('/api/categorias/')
        
        # Obtener una categoría existente
        categoria = CategoriaProducto.objects.first()
        
        if categoria:
            print(f"📋 Categoría encontrada: {categoria.nombre}")
            
            # Serializar con contexto
            serializer = CategoriaSerializer(categoria, context={'request': request})
            data = serializer.data
            
            print(f"📸 imagen_url: {data.get('imagen_url')}")
            
            # Verificar si la URL es de Cloudinary
            imagen_url = data.get('imagen_url', '')
            if imagen_url:
                if 'cloudinary.com' in imagen_url:
                    print("✅ URL de Cloudinary detectada en categoría!")
                    return True
                else:
                    print("⚠️  URL local detectada en categoría")
                    return False
            else:
                print("ℹ️  No hay imagen en la categoría")
                return True
        else:
            print("❌ No hay categorías en la base de datos")
            return False
            
    except Exception as e:
        print(f"❌ Error probando serializer: {e}")
        return False

def test_categoria_api():
    """Prueba la API de categorías en Render"""
    print("\n🚀 Probando API de categorías en Render...")
    
    # URL de la API
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
                print("✅ ¡Cloudinary está funcionando en categorías!")
                return True
            else:
                print("❌ No se detectaron URLs de Cloudinary")
                return False
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en petición API: {e}")
        return False

def test_crear_categoria_con_imagen():
    """Prueba crear una categoría con imagen en Render"""
    print("\n📝 Probando crear categoría con imagen...")
    
    # URL de la API
    api_url = "https://tienda-backend-ap-api.onrender.com/api/categorias/"
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 300), color='orange')
        draw = ImageDraw.Draw(img)
        draw.text((100, 140), "CATEGORIA TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Datos de la categoría
        unique_id = str(uuid.uuid4())[:8]
        categoria_data = {
            'nombre': f'Test Categoría Cloudinary {unique_id}',
            'descripcion': 'Categoría de prueba para verificar Cloudinary',
            'activa': True,
            'orden': 999
        }
        
        # Preparar los datos
        files = {
            'imagen': ('test_categoria.jpg', img_byte_arr, 'image/jpeg')
        }
        
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
            
            categoria = result.get('categoria', {})
            print(f"🆔 ID de la categoría: {categoria.get('id')}")
            print(f"📸 URL de imagen: {categoria.get('imagen_url')}")
            
            # Verificar si la URL es de Cloudinary
            imagen_url = categoria.get('imagen_url', '')
            if 'cloudinary.com' in imagen_url:
                print("✅ ¡URL de Cloudinary detectada!")
                print("🎉 ¡Cloudinary está funcionando correctamente en categorías!")
                return True
            else:
                print("⚠️  URL local detectada")
                print("❌ Cloudinary no está funcionando en categorías")
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
    print("🚀 Test de categorías con Cloudinary")
    print("=" * 50)
    
    # Test 1: Serializer local
    serializer_ok = test_categoria_serializer()
    
    # Test 2: API de categorías
    api_ok = test_categoria_api()
    
    # Test 3: Crear categoría con imagen
    create_ok = test_crear_categoria_con_imagen()
    
    print("\n" + "=" * 50)
    print("📊 Resumen:")
    print(f"   Serializer local: {'✅ OK' if serializer_ok else '❌ Error'}")
    print(f"   API de categorías: {'✅ OK' if api_ok else '❌ Error'}")
    print(f"   Crear categoría: {'✅ OK' if create_ok else '❌ Error'}")
    
    if serializer_ok and api_ok and create_ok:
        print("🎉 ¡Cloudinary está funcionando correctamente en categorías!")
    else:
        print("⚠️  Hay problemas con Cloudinary en categorías")

if __name__ == "__main__":
    main() 