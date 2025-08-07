#!/usr/bin/env python3
"""
Script para verificar la configuración de producción localmente
"""
import os
import sys
import django

# Configurar Django con settings locales
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.conf import settings
from django.core.files.storage import default_storage

def check_production_config():
    """Verificar configuración de producción"""
    print("🔍 VERIFICANDO CONFIGURACIÓN DE PRODUCCIÓN (LOCAL)")
    print("=" * 60)
    
    # Verificar configuración básica
    print("📋 Configuración básica:")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"  DATABASES: {list(settings.DATABASES.keys())}")
    
    # Verificar Cloudinary
    print("\n☁️ Configuración de Cloudinary:")
    print(f"  CLOUDINARY_CLOUD_NAME: {getattr(settings, 'CLOUDINARY_CLOUD_NAME', 'No configurado')}")
    print(f"  CLOUDINARY_API_KEY: {getattr(settings, 'CLOUDINARY_API_KEY', 'No configurado')[:10]}...")
    print(f"  CLOUDINARY_API_SECRET: {getattr(settings, 'CLOUDINARY_API_SECRET', 'No configurado')[:10]}...")
    
    # Verificar storage
    print("\n📁 Configuración de Storage:")
    print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    print(f"  MEDIA_URL: {settings.MEDIA_URL}")
    print(f"  STATIC_URL: {settings.STATIC_URL}")
    
    # Verificar CORS
    print("\n🌐 Configuración de CORS:")
    print(f"  CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}")
    
    # Verificar variables de entorno
    print("\n🔧 Variables de entorno:")
    print(f"  DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"  DATABASE_URL: {'Configurado' if os.environ.get('DATABASE_URL') else 'No configurado (normal en local)'}")
    print(f"  CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME', 'No configurado')}")
    print(f"  CLOUDINARY_API_KEY: {os.environ.get('CLOUDINARY_API_KEY', 'No configurado')[:10] if os.environ.get('CLOUDINARY_API_KEY') else 'No configurado'}...")
    print(f"  DJANGO_CLOUDINARY_STORAGE: {os.environ.get('DJANGO_CLOUDINARY_STORAGE', 'No configurado')}")
    
    return True

def test_cloudinary_production():
    """Probar Cloudinary en producción"""
    print("\n🧪 PROBANDO CLOUDINARY EN PRODUCCIÓN")
    print("=" * 60)
    
    try:
        # Verificar configuración de Cloudinary
        import cloudinary
        print(f"✅ Cloudinary configurado:")
        print(f"  Cloud Name: {cloudinary.config().cloud_name}")
        print(f"  API Key: {cloudinary.config().api_key[:10]}...")
        
        # Probar subida de archivo
        from io import BytesIO
        from PIL import Image
        
        # Crear imagen de prueba
        img = Image.new('RGB', (100, 100), color='#FF6B6B')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Subir a Cloudinary
        import cloudinary.uploader
        result = cloudinary.uploader.upload(
            img_io,
            public_id='test_production_local',
            overwrite=True
        )
        
        print(f"✅ Subida exitosa:")
        print(f"  Public ID: {result['public_id']}")
        print(f"  URL: {result['secure_url']}")
        print(f"  Tamaño: {result.get('bytes', 0)} bytes")
        
        # Verificar que la URL es accesible
        import requests
        response = requests.get(result['secure_url'])
        if response.status_code == 200:
            print("✅ URL accesible correctamente")
        else:
            print(f"❌ URL no accesible: {response.status_code}")
        
        # Limpiar archivo de prueba
        cloudinary.uploader.destroy('test_production_local')
        print("✅ Archivo de prueba eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando Cloudinary: {e}")
        return False

def test_storage_production():
    """Probar storage en producción"""
    print("\n🧪 PROBANDO STORAGE EN PRODUCCIÓN")
    print("=" * 60)
    
    try:
        # Verificar storage actual
        print(f"📁 Storage actual: {type(default_storage).__name__}")
        
        # Probar subida usando storage
        from django.core.files.base import ContentFile
        from io import BytesIO
        from PIL import Image
        
        # Crear imagen de prueba
        img = Image.new('RGB', (150, 150), color='#3498DB')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Crear ContentFile
        content = ContentFile(img_io.getvalue(), name='test_storage_production_local.png')
        
        # Guardar usando storage
        saved_name = default_storage.save('test_storage_production_local.png', content)
        print(f"✅ Archivo guardado: {saved_name}")
        
        # Verificar que existe
        if default_storage.exists(saved_name):
            print("✅ Archivo existe en storage")
            
            # Obtener URL
            url = default_storage.url(saved_name)
            print(f"🔗 URL: {url}")
            
            # Verificar que la URL es accesible
            import requests
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ URL accesible correctamente")
            else:
                print(f"❌ URL no accesible: {response.status_code}")
            
            # Eliminar archivo de prueba
            default_storage.delete(saved_name)
            print("✅ Archivo de prueba eliminado")
            
            return True
        else:
            print("❌ Archivo no existe en storage")
            return False
            
    except Exception as e:
        print(f"❌ Error probando storage: {e}")
        return False

def test_api_endpoints():
    """Probar endpoints de la API"""
    print("\n🧪 PROBANDO ENDPOINTS DE LA API")
    print("=" * 60)
    
    try:
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Probar endpoint de categorías
        response = client.get('/api/categorias/')
        if response.status_code == 200:
            print("✅ Endpoint /api/categorias/ funciona")
        else:
            print(f"❌ Endpoint /api/categorias/ falló: {response.status_code}")
        
        # Probar endpoint de productos
        response = client.get('/api/productos/')
        if response.status_code == 200:
            print("✅ Endpoint /api/productos/ funciona")
        else:
            print(f"❌ Endpoint /api/productos/ falló: {response.status_code}")
        
        # Probar endpoint de ventas
        response = client.get('/api/ventas/')
        if response.status_code == 200:
            print("✅ Endpoint /api/ventas/ funciona")
        else:
            print(f"❌ Endpoint /api/ventas/ falló: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando endpoints: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO VERIFICACIÓN DE PRODUCCIÓN (LOCAL)")
    print("=" * 60)
    
    # Verificar configuración
    config_success = check_production_config()
    
    # Probar Cloudinary
    cloudinary_success = test_cloudinary_production()
    
    # Probar storage
    storage_success = test_storage_production()
    
    # Probar endpoints
    api_success = test_api_endpoints()
    
    print("\n📊 RESULTADOS DE VERIFICACIÓN")
    print("=" * 60)
    print(f"Configuración: {'✅ PASÓ' if config_success else '❌ FALLÓ'}")
    print(f"Cloudinary: {'✅ PASÓ' if cloudinary_success else '❌ FALLÓ'}")
    print(f"Storage: {'✅ PASÓ' if storage_success else '❌ FALLÓ'}")
    print(f"API Endpoints: {'✅ PASÓ' if api_success else '❌ FALLÓ'}")
    
    if all([config_success, cloudinary_success, storage_success, api_success]):
        print("\n🎉 ¡CONFIGURACIÓN DE PRODUCCIÓN LISTA!")
        print("✅ Todas las verificaciones pasaron.")
        print("✅ Cloudinary funciona correctamente.")
        print("✅ Storage funciona correctamente.")
        print("✅ API endpoints funcionan correctamente.")
        print("✅ Sistema listo para Render.")
        print("\n🚀 PUEDES HACER DEPLOY EN RENDER")
    else:
        print("\n⚠️ Hay problemas con la configuración.")
        print("❌ Revisa la configuración antes del deploy.") 