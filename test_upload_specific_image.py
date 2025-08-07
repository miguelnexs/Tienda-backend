#!/usr/bin/env python3
"""
Script para subir una imagen específica a ImageKit.io
"""

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

from django.core.files.base import ContentFile
from Backend.imagekit_storage import ImageKitStorage

def upload_specific_image():
    """Subir imagen específica a ImageKit"""
    print("🚀 SUBIDA DE IMAGEN ESPECÍFICA A IMAGEKIT")
    print("="*50)
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\cartera-casual-para-mujer-23064.jpg"
    
    try:
        # Verificar que el archivo existe
        if not os.path.exists(image_path):
            print(f"❌ Error: El archivo no existe en {image_path}")
            return False
        
        print(f"📁 Archivo encontrado: {image_path}")
        
        # Leer el archivo
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        print(f"📊 Tamaño del archivo: {len(image_data)} bytes ({len(image_data)/1024:.1f} KB)")
        
        # Crear instancia de ImageKitStorage
        storage = ImageKitStorage()
        print("✅ ImageKitStorage inicializado")
        
        # Crear ContentFile
        content = ContentFile(image_data)
        content.name = 'cartera-casual-para-mujer-23064.jpg'
        
        # Subir a ImageKit
        print("📤 Subiendo imagen a ImageKit...")
        file_path = storage.save('productos/cartera-casual-para-mujer-23064.jpg', content)
        
        print(f"✅ Archivo subido exitosamente")
        print(f"📁 Ruta del archivo: {file_path}")
        
        # Obtener URL
        file_url = storage.url(file_path)
        print(f"🔗 URL del archivo: {file_url}")
        
        # Verificar que existe
        if storage.exists(file_path):
            print("✅ Archivo verificado en ImageKit")
        else:
            print("❌ Archivo no encontrado en ImageKit")
        
        # Obtener información del archivo
        file_size = storage.size(file_path)
        print(f"📊 Tamaño en ImageKit: {file_size} bytes")
        
        print("\n🎉 ¡IMAGEN SUBIDA EXITOSAMENTE!")
        print(f"🔗 URL completa: {file_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error subiendo imagen: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_access():
    """Probar acceso a la imagen subida"""
    print("\n🔍 PRUEBA DE ACCESO A LA IMAGEN")
    print("="*30)
    
    try:
        import requests
        
        # URL de la imagen (asumiendo que se subió correctamente)
        image_url = "https://ik.imagekit.io/jjuadt4gux/productos/cartera-casual-para-mujer-23064.jpg"
        
        print(f"🔗 Probando acceso a: {image_url}")
        
        # Hacer request a la imagen
        response = requests.get(image_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Imagen accesible correctamente")
            print(f"📊 Tamaño de respuesta: {len(response.content)} bytes")
            print(f"📋 Content-Type: {response.headers.get('content-type', 'No especificado')}")
        else:
            print(f"❌ Error accediendo a la imagen: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en prueba de acceso: {e}")

if __name__ == "__main__":
    print("🔧 CONFIGURACIÓN DE IMAGEKIT")
    print(f"Public Key: {os.environ.get('IMAGEKIT_PUBLIC_KEY', 'No configurada')[:20]}...")
    print(f"URL Endpoint: {os.environ.get('IMAGEKIT_URL_ENDPOINT', 'No configurada')}")
    print()
    
    # Subir imagen
    success = upload_specific_image()
    
    if success:
        # Probar acceso
        test_image_access()
        
        print("\n🎉 ¡PRUEBA COMPLETADA EXITOSAMENTE!")
        print("La imagen se subió correctamente a ImageKit.io")
    else:
        print("\n❌ PRUEBA FALLÓ")
        print("Revisa los errores y la configuración") 