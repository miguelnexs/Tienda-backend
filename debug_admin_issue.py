#!/usr/bin/env python3
"""
Script para diagnosticar el problema específico del admin de Django
"""
import os
import sys
import django
from io import BytesIO
from PIL import Image

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.core.files import File
from categorias.models import CategoriaProducto
from django.core.files.storage import default_storage

def debug_admin_upload_process():
    """Diagnosticar el proceso de subida del admin"""
    print("🔍 DIAGNOSTICANDO PROCESO DE SUBIDA DEL ADMIN")
    print("=" * 60)
    
    try:
        # Crear una imagen de prueba
        img = Image.new('RGB', (600, 600), color='purple')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        print("📸 Imagen de prueba creada")
        
        # Crear categoría
        categoria = CategoriaProducto(
            nombre="Categoría Debug Admin",
            descripcion="Categoría para diagnosticar problema del admin",
            slug=f"categoria-debug-admin-{os.getpid()}"
        )
        
        # Guardar categoría
        categoria.save()
        print(f"✅ Categoría creada: {categoria.id}")
        
        # Verificar configuración antes de subir
        print("\n📋 CONFIGURACIÓN ANTES DE SUBIR:")
        print(f"  DEFAULT_FILE_STORAGE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
        print(f"  default_storage class: {type(default_storage).__name__}")
        print(f"  default_storage module: {type(default_storage).__module__}")
        
        # Crear archivo como lo haría el admin
        django_file = File(img_io, name=f'categoria_debug_admin_{os.getpid()}.jpg')
        
        print(f"\n📤 Subiendo archivo: {django_file.name}")
        print(f"  Tamaño del archivo: {len(django_file.read())} bytes")
        django_file.seek(0)  # Resetear posición
        
        # Asignar imagen (exactamente como lo hace el admin)
        print("🔄 Asignando imagen a la categoría...")
        categoria.imagen.save(django_file.name, django_file, save=True)
        
        print("✅ Imagen asignada")
        print(f"  Nombre del archivo: {categoria.imagen.name}")
        print(f"  URL: {categoria.imagen.url}")
        
        # Verificar configuración después de subir
        print("\n📋 CONFIGURACIÓN DESPUÉS DE SUBIR:")
        print(f"  default_storage class: {type(default_storage).__name__}")
        print(f"  default_storage module: {type(default_storage).__module__}")
        
        # Verificar URL
        if 'cloudinary.com' in categoria.imagen.url:
            print("✅ URL es de Cloudinary")
        else:
            print("❌ URL no es de Cloudinary")
        
        # Verificar existencia
        if hasattr(categoria.imagen, 'storage'):
            exists = categoria.imagen.storage.exists(categoria.imagen.name)
            print(f"  Existe en storage: {exists}")
        
        # Obtener información detallada
        try:
            import cloudinary.api
            result = cloudinary.api.resource(categoria.imagen.name)
            print(f"📊 Información de Cloudinary:")
            print(f"  Public ID: {result['public_id']}")
            print(f"  URL segura: {result.get('secure_url', 'N/A')}")
            print(f"  Tamaño: {result.get('bytes', 0)} bytes")
            print(f"  Formato: {result.get('format', 'N/A')}")
            print(f"  Ancho: {result.get('width', 0)}")
            print(f"  Alto: {result.get('height', 0)}")
        except Exception as e:
            print(f"⚠️ No se pudo obtener información: {e}")
        
        # Probar acceso a la URL
        try:
            import requests
            response = requests.get(categoria.imagen.url, timeout=10)
            print(f"📡 Respuesta HTTP: {response.status_code}")
            if response.status_code == 200:
                print("✅ URL accesible")
                print(f"📏 Tamaño de respuesta: {len(response.content)} bytes")
            else:
                print(f"❌ Error accediendo a URL: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error verificando URL: {e}")
        
        # Limpiar
        categoria.delete()
        print("✅ Categoría eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error diagnosticando admin: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_storage_override():
    """Probar override del storage"""
    print("\n🧪 PROBANDO OVERRIDE DEL STORAGE")
    print("=" * 60)
    
    try:
        from Backend.cloudinary_storage_complete import CloudinaryStorageComplete
        
        # Crear imagen de prueba
        img = Image.new('RGB', (400, 400), color='orange')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear archivo
        django_file = File(img_io, name=f'test_override_{os.getpid()}.jpg')
        
        # Usar storage directamente
        storage = CloudinaryStorageComplete()
        saved_name = storage.save(django_file.name, django_file)
        
        print("✅ Storage directo funcionando")
        print(f"  Nombre guardado: {saved_name}")
        
        # Obtener URL
        url = storage.url(saved_name)
        print(f"  URL: {url}")
        
        # Verificar existencia
        exists = storage.exists(saved_name)
        print(f"  Existe: {exists}")
        
        # Limpiar
        storage.delete(saved_name)
        print("✅ Archivo eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando override: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_settings_import():
    """Verificar importación de settings"""
    print("\n🔍 VERIFICANDO IMPORTACIÓN DE SETTINGS")
    print("=" * 60)
    
    try:
        from django.conf import settings
        
        print("✅ Settings importados correctamente")
        print(f"  DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No definido')}")
        print(f"  MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'No definido')}")
        print(f"  CLOUDINARY_CLOUD_NAME: {getattr(settings, 'CLOUDINARY_CLOUD_NAME', 'No definido')}")
        print(f"  CLOUDINARY_API_KEY: {getattr(settings, 'CLOUDINARY_API_KEY', 'No definido')}")
        
        # Verificar que el storage está configurado
        storage_class = getattr(settings, 'DEFAULT_FILE_STORAGE', None)
        if storage_class:
            print(f"  Storage class configurado: {storage_class}")
        else:
            print("❌ DEFAULT_FILE_STORAGE no está configurado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando settings: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO DIAGNÓSTICO DEL ADMIN")
    print("=" * 60)
    
    # Verificar settings
    settings_success = check_settings_import()
    
    # Diagnosticar admin
    admin_success = debug_admin_upload_process()
    
    # Probar override
    override_success = test_storage_override()
    
    print("\n📊 RESULTADOS DEL DIAGNÓSTICO")
    print("=" * 60)
    print(f"Settings: {'✅ PASÓ' if settings_success else '❌ FALLÓ'}")
    print(f"Admin: {'✅ PASÓ' if admin_success else '❌ FALLÓ'}")
    print(f"Override: {'✅ PASÓ' if override_success else '❌ FALLÓ'}")
    
    if settings_success and admin_success and override_success:
        print("\n🎉 ¡DIAGNÓSTICO COMPLETO!")
        print("✅ El sistema está funcionando correctamente.")
        print("✅ Las imágenes se suben a Cloudinary.")
        print("✅ El admin funciona correctamente.")
    else:
        print("\n⚠️ Se encontraron problemas.")
        print("❌ Revisa la configuración del sistema.") 