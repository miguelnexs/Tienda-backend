#!/usr/bin/env python3
"""
Script para verificar la URL correcta de la imagen subida
"""

import requests

def test_image_urls():
    """Probar diferentes URLs para la imagen"""
    print("🔍 VERIFICACIÓN DE URLS DE LA IMAGEN")
    print("="*40)
    
    # URLs posibles
    urls_to_test = [
        "https://ik.imagekit.io/jjuadt4gux/productos/cartera-casual-para-mujer-23064.jpg",
        "https://ik.imagekit.io/jjuadt4gux/productos/productos_cartera-casual-para-mujer-23064.jpg",
        "https://ik.imagekit.io/jjuadt4gux/cartera-casual-para-mujer-23064.jpg"
    ]
    
    for i, url in enumerate(urls_to_test, 1):
        print(f"\n{i}. Probando: {url}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ ACCESIBLE - Status: {response.status_code}")
                print(f"📊 Tamaño: {len(response.content)} bytes")
                print(f"📋 Content-Type: {response.headers.get('content-type', 'No especificado')}")
                return url
            else:
                print(f"❌ No accesible - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return None

def list_imagekit_files():
    """Listar archivos en ImageKit para ver la estructura"""
    print("\n📁 LISTANDO ARCHIVOS EN IMAGEKIT")
    print("="*40)
    
    try:
        import os
        import sys
        import django
        from pathlib import Path
        from dotenv import load_dotenv
        
        # Cargar variables de entorno
        load_dotenv()
        
        # Configurar Django
        BASE_DIR = Path(__file__).resolve().parent
        sys.path.append(str(BASE_DIR))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
        django.setup()
        
        from Backend.imagekit_storage import ImageKitStorage
        
        storage = ImageKitStorage()
        result = storage._imagekit.list_files()
        
        print(f"📊 Total de archivos: {len(result.list)}")
        for file in result.list:
            print(f"📄 {file.name} - ID: {file.file_id}")
            print(f"   URL: {file.url}")
            print(f"   Tamaño: {file.size} bytes")
            print()
            
    except Exception as e:
        print(f"❌ Error listando archivos: {e}")

if __name__ == "__main__":
    # Probar URLs
    working_url = test_image_urls()
    
    if working_url:
        print(f"\n🎉 ¡URL FUNCIONANDO: {working_url}")
    else:
        print("\n❌ Ninguna URL funcionó")
    
    # Listar archivos para ver la estructura
    list_imagekit_files() 