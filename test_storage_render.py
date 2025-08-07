#!/usr/bin/env python3
"""
Script para verificar la configuración de storage en Render
"""
import os
import sys
import django

# Configurar variables de entorno para prueba
os.environ['DATABASE_URL'] = 'postgresql://test:test@localhost:5432/testdb'
os.environ['DJANGO_SETTINGS_MODULE'] = 'Backend.render_settings'

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
    print("✅ Django configurado correctamente")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

from django.conf import settings
from django.core.files.storage import default_storage
from Backend.cloudinary_storage_fixed_urls import CloudinaryStorageFixedURLs

def test_storage_config():
    """Verificar configuración de storage"""
    print("\n🧪 VERIFICANDO CONFIGURACIÓN DE STORAGE")
    print("=" * 60)
    
    # 1. Verificar DEFAULT_FILE_STORAGE
    print("\n📋 Configuración en settings:")
    print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    
    # 2. Verificar tipo de default_storage
    print("\n📋 Storage actual:")
    print(f"  Tipo: {type(default_storage).__name__}")
    print(f"  Módulo: {type(default_storage).__module__}")
    
    # 3. Verificar que sea CloudinaryStorageFixedURLs
    if isinstance(default_storage, CloudinaryStorageFixedURLs):
        print("\n✅ Storage configurado correctamente")
        print("  Es una instancia de CloudinaryStorageFixedURLs")
    else:
        print("\n❌ Storage NO configurado correctamente")
        print(f"  Es una instancia de {type(default_storage).__name__}")
        
        # Intentar forzar el storage
        print("\n🔧 Intentando forzar el storage correcto...")
        try:
            cloudinary_storage = CloudinaryStorageFixedURLs()
            import django.core.files.storage
            django.core.files.storage.default_storage = cloudinary_storage
            
            # Verificar de nuevo
            if isinstance(default_storage, CloudinaryStorageFixedURLs):
                print("✅ Storage forzado correctamente")
            else:
                print("❌ No se pudo forzar el storage")
                
        except Exception as e:
            print(f"❌ Error forzando storage: {e}")

def test_cloudinary_config():
    """Verificar configuración de Cloudinary"""
    print("\n🧪 VERIFICANDO CONFIGURACIÓN DE CLOUDINARY")
    print("=" * 60)
    
    import cloudinary
    
    # 1. Verificar credenciales
    print("\n📋 Credenciales configuradas:")
    print(f"  Cloud Name: {cloudinary.config().cloud_name}")
    print(f"  API Key: {cloudinary.config().api_key[:10]}...")
    
    # 2. Verificar variables de entorno
    print("\n📋 Variables de entorno:")
    print(f"  CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME', 'No configurado')}")
    print(f"  CLOUDINARY_API_KEY: {os.environ.get('CLOUDINARY_API_KEY', 'No configurado')[:10]}...")
    print(f"  DJANGO_CLOUDINARY_STORAGE: {os.environ.get('DJANGO_CLOUDINARY_STORAGE', 'No configurado')}")
    
    # 3. Verificar configuración en settings
    print("\n📋 Configuración en settings:")
    print(f"  CLOUDINARY_CLOUD_NAME: {getattr(settings, 'CLOUDINARY_CLOUD_NAME', 'No configurado')}")
    print(f"  CLOUDINARY_API_KEY: {getattr(settings, 'CLOUDINARY_API_KEY', 'No configurado')[:10]}...")

def test_upload():
    """Intentar subir un archivo de prueba"""
    print("\n🧪 PROBANDO SUBIDA DE ARCHIVO")
    print("=" * 60)
    
    from django.core.files.base import ContentFile
    
    try:
        # Crear un archivo de prueba
        content = ContentFile(b"test content", name="test.txt")
        
        # Intentar guardar
        path = default_storage.save("test/test.txt", content)
        print(f"\n✅ Archivo guardado en: {path}")
        
        # Intentar obtener URL
        url = default_storage.url(path)
        print(f"✅ URL generada: {url}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error subiendo archivo: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE STORAGE PARA RENDER")
    print("=" * 60)
    
    # Probar configuración
    test_storage_config()
    test_cloudinary_config()
    upload_success = test_upload()
    
    print("\n📊 RESULTADOS DE PRUEBA")
    print("=" * 60)
    print(f"Storage: {'✅ PASÓ' if isinstance(default_storage, CloudinaryStorageFixedURLs) else '❌ FALLÓ'}")
    print(f"Cloudinary: {'✅ PASÓ' if hasattr(settings, 'CLOUDINARY_CLOUD_NAME') else '❌ FALLÓ'}")
    print(f"Upload: {'✅ PASÓ' if upload_success else '❌ FALLÓ'}")
    
    if all([
        isinstance(default_storage, CloudinaryStorageFixedURLs),
        hasattr(settings, 'CLOUDINARY_CLOUD_NAME'),
        upload_success
    ]):
        print("\n🎉 ¡STORAGE LISTO PARA RENDER!")
        print("✅ Storage configurado correctamente")
        print("✅ Cloudinary configurado")
        print("✅ Prueba de subida exitosa")
        print("\n🚀 PUEDES HACER DEPLOY EN RENDER")
    else:
        print("\n⚠️ Hay problemas con el storage")
        print("❌ Revisa la configuración antes del deploy") 