#!/usr/bin/env python3
"""
Script para diagnosticar el problema de URLs de Cloudinary
"""
import os
import sys
import django
import requests
from io import BytesIO
from PIL import Image

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from Backend.cloudinary_storage_models import CloudinaryStorageModels
from django.core.files.base import ContentFile
from django.core.files import File

def test_cloudinary_upload_and_url():
    """Probar subida a Cloudinary y verificar URL"""
    print("🧪 Probando subida a Cloudinary y verificación de URL...")
    
    try:
        # Crear una imagen de prueba
        img = Image.new('RGB', (300, 300), color='red')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear archivo de prueba
        test_name = f"test_url_debug_{os.getpid()}.jpg"
        django_file = File(img_io, name=test_name)
        
        # Usar el storage
        storage = CloudinaryStorageModels()
        
        print(f"📤 Subiendo imagen: {test_name}")
        
        # Subir usando el storage
        saved_name = storage.save(test_name, django_file)
        print(f"✅ Imagen guardada como: {saved_name}")
        
        # Obtener URL
        url = storage.url(saved_name)
        print(f"🔗 URL generada: {url}")
        
        # Verificar que la URL es de Cloudinary
        if 'cloudinary.com' in url:
            print("✅ URL es de Cloudinary")
        else:
            print("❌ URL no es de Cloudinary")
            return False
        
        # Verificar que el archivo existe en Cloudinary
        exists = storage.exists(saved_name)
        print(f"🔍 Imagen existe en Cloudinary: {exists}")
        
        # Intentar acceder a la URL
        try:
            response = requests.get(url, timeout=10)
            print(f"📡 Respuesta HTTP: {response.status_code}")
            if response.status_code == 200:
                print("✅ URL accesible")
                print(f"📏 Tamaño de respuesta: {len(response.content)} bytes")
            else:
                print(f"❌ Error accediendo a URL: {response.status_code}")
        except Exception as e:
            print(f"❌ Error verificando URL: {e}")
        
        # Obtener información del archivo desde Cloudinary
        try:
            import cloudinary.api
            result = cloudinary.api.resource(saved_name)
            print(f"📊 Información de Cloudinary:")
            print(f"  Public ID: {result['public_id']}")
            print(f"  URL segura: {result.get('secure_url', 'N/A')}")
            print(f"  URL: {result.get('url', 'N/A')}")
            print(f"  Tamaño: {result.get('bytes', 0)} bytes")
            print(f"  Formato: {result.get('format', 'N/A')}")
            print(f"  Ancho: {result.get('width', 0)}")
            print(f"  Alto: {result.get('height', 0)}")
            print(f"  Tipo de recurso: {result.get('resource_type', 'N/A')}")
            
            # Probar la URL segura
            secure_url = result.get('secure_url')
            if secure_url:
                print(f"🔗 URL segura: {secure_url}")
                try:
                    response = requests.get(secure_url, timeout=10)
                    print(f"📡 Respuesta URL segura: {response.status_code}")
                    if response.status_code == 200:
                        print("✅ URL segura accesible")
                    else:
                        print(f"❌ Error en URL segura: {response.status_code}")
                except Exception as e:
                    print(f"❌ Error verificando URL segura: {e}")
            
        except Exception as e:
            print(f"❌ Error obteniendo información de Cloudinary: {e}")
        
        # Eliminar archivo de prueba
        deleted = storage.delete(saved_name)
        print(f"🗑️ Imagen eliminada: {deleted}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specific_url_format():
    """Probar formato específico de URL"""
    print("\n🧪 Probando formato específico de URL...")
    
    try:
        # Crear una imagen de prueba
        img = Image.new('RGB', (200, 200), color='blue')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear archivo con nombre específico
        test_name = "categorias/test_specific_url.jpg"
        django_file = File(img_io, name=test_name)
        
        # Usar el storage
        storage = CloudinaryStorageModels()
        
        print(f"📤 Subiendo imagen: {test_name}")
        
        # Subir usando el storage
        saved_name = storage.save(test_name, django_file)
        print(f"✅ Imagen guardada como: {saved_name}")
        
        # Obtener URL
        url = storage.url(saved_name)
        print(f"🔗 URL generada: {url}")
        
        # Verificar que la URL es de Cloudinary
        if 'cloudinary.com' in url:
            print("✅ URL es de Cloudinary")
        else:
            print("❌ URL no es de Cloudinary")
            return False
        
        # Verificar que el archivo existe en Cloudinary
        exists = storage.exists(saved_name)
        print(f"🔍 Imagen existe en Cloudinary: {exists}")
        
        # Intentar acceder a la URL
        try:
            response = requests.get(url, timeout=10)
            print(f"📡 Respuesta HTTP: {response.status_code}")
            if response.status_code == 200:
                print("✅ URL accesible")
                print(f"📏 Tamaño de respuesta: {len(response.content)} bytes")
            else:
                print(f"❌ Error accediendo a URL: {response.status_code}")
        except Exception as e:
            print(f"❌ Error verificando URL: {e}")
        
        # Eliminar archivo de prueba
        deleted = storage.delete(saved_name)
        print(f"🗑️ Imagen eliminada: {deleted}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_cloudinary_configuration():
    """Verificar configuración de Cloudinary"""
    print("\n🔍 Verificando configuración de Cloudinary...")
    
    try:
        import cloudinary
        import cloudinary.api
        
        # Verificar configuración
        print(f"📁 Cloud Name: {cloudinary.config().cloud_name}")
        print(f"📁 API Key: {cloudinary.config().api_key}")
        print(f"📁 API Secret: {cloudinary.config().api_secret[:10]}...")
        
        # Probar conexión
        try:
            # Intentar obtener información de la cuenta
            result = cloudinary.api.ping()
            print("✅ Conexión a Cloudinary exitosa")
        except Exception as e:
            print(f"❌ Error conectando a Cloudinary: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO DIAGNÓSTICO DE URL")
    print("=" * 60)
    
    # Verificar configuración
    config_success = check_cloudinary_configuration()
    
    # Probar subida y URL
    upload_success = test_cloudinary_upload_and_url()
    
    # Probar formato específico
    format_success = test_specific_url_format()
    
    print("\n📊 RESULTADOS DEL DIAGNÓSTICO")
    print("=" * 60)
    print(f"Configuración: {'✅ PASÓ' if config_success else '❌ FALLÓ'}")
    print(f"Subida y URL: {'✅ PASÓ' if upload_success else '❌ FALLÓ'}")
    print(f"Formato específico: {'✅ PASÓ' if format_success else '❌ FALLÓ'}")
    
    if config_success and upload_success and format_success:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ Las URLs de Cloudinary funcionan correctamente.")
    else:
        print("\n⚠️ Algunas pruebas fallaron.")
        print("❌ Revisa la configuración de Cloudinary.") 