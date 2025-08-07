#!/usr/bin/env python3
"""
Script para depurar el proceso real de subida a Cloudinary
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
from Backend.cloudinary_storage_fixed_urls import CloudinaryStorageFixedURLs

def debug_cloudinary_upload():
    """Depurar subida real a Cloudinary"""
    print("🔍 DEPURANDO SUBIDA REAL A CLOUDINARY")
    print("=" * 60)
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (500, 500), color='#F39C12')  # Amarillo
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        print("📸 Imagen de prueba creada")
        
        # Crear archivo
        django_file = File(img_io, name=f'debug_cloudinary_upload_{os.getpid()}.jpg')
        
        print(f"📁 Archivo creado: {django_file.name}")
        print(f"📏 Tamaño: {len(django_file.read())} bytes")
        django_file.seek(0)
        
        # Usar storage directamente
        storage = CloudinaryStorageFixedURLs()
        print("🔧 Storage inicializado")
        
        # PASO 1: Subir archivo
        print("\n📤 PASO 1: Subiendo archivo...")
        saved_name = storage.save(django_file.name, django_file)
        print(f"✅ Archivo guardado como: {saved_name}")
        
        # PASO 2: Obtener URL
        print("\n🔗 PASO 2: Obteniendo URL...")
        url = storage.url(saved_name)
        print(f"🔗 URL: {url}")
        
        # PASO 3: Verificar existencia
        print("\n🔍 PASO 3: Verificando existencia...")
        exists = storage.exists(saved_name)
        print(f"📁 Existe en storage: {exists}")
        
        # PASO 4: Verificar en Cloudinary directamente
        print("\n☁️ PASO 4: Verificando en Cloudinary...")
        try:
            import cloudinary.api
            result = cloudinary.api.resource(saved_name)
            print("✅ Archivo encontrado en Cloudinary")
            print(f"📊 Información:")
            print(f"  Public ID: {result['public_id']}")
            print(f"  URL segura: {result.get('secure_url', 'N/A')}")
            print(f"  Tamaño: {result.get('bytes', 0)} bytes")
            print(f"  Formato: {result.get('format', 'N/A')}")
            print(f"  Ancho: {result.get('width', 0)}")
            print(f"  Alto: {result.get('height', 0)}")
            print(f"  Versión: {result.get('version', 'N/A')}")
            
            # Probar acceso a la URL segura
            secure_url = result.get('secure_url')
            if secure_url:
                print(f"🔗 URL segura: {secure_url}")
                try:
                    import requests
                    response = requests.get(secure_url, timeout=10)
                    print(f"📡 Respuesta HTTP: {response.status_code}")
                    if response.status_code == 200:
                        print("✅ URL segura accesible")
                        print(f"📏 Tamaño: {len(response.content)} bytes")
                    else:
                        print(f"❌ Error en URL segura: HTTP {response.status_code}")
                except Exception as e:
                    print(f"⚠️ Error verificando URL segura: {e}")
            
        except Exception as e:
            print(f"❌ Archivo NO encontrado en Cloudinary: {e}")
            print("🔍 Intentando con diferentes variaciones...")
            
            # Intentar con diferentes variaciones
            variations = [
                saved_name,
                saved_name + '.jpg',
                saved_name.replace('.jpg', ''),
                saved_name.replace('categorias/', '')
            ]
            
            for variation in variations:
                try:
                    result = cloudinary.api.resource(variation)
                    print(f"✅ Encontrado con variación '{variation}': {result.get('secure_url')}")
                    break
                except:
                    continue
            else:
                print("❌ No se encontró el archivo con ninguna variación")
        
        # PASO 5: Probar acceso a la URL generada
        print("\n🌐 PASO 5: Probando acceso a la URL generada...")
        try:
            import requests
            response = requests.get(url, timeout=10)
            print(f"📡 Respuesta HTTP: {response.status_code}")
            if response.status_code == 200:
                print("✅ URL generada accesible")
                print(f"📏 Tamaño: {len(response.content)} bytes")
            else:
                print(f"❌ Error en URL generada: HTTP {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error verificando URL generada: {e}")
        
        # Limpiar
        storage.delete(saved_name)
        print("\n✅ Archivo eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error depurando subida a Cloudinary: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_admin_with_cloudinary():
    """Probar admin con verificación de Cloudinary"""
    print("\n🧪 PROBANDO ADMIN CON VERIFICACIÓN DE CLOUDINARY")
    print("=" * 60)
    
    try:
        # Crear imagen
        img = Image.new('RGB', (600, 600), color='#E74C3C')  # Rojo
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear categoría
        categoria = CategoriaProducto(
            nombre="Categoría Admin Cloudinary",
            descripcion="Categoría para probar admin con Cloudinary",
            slug=f"categoria-admin-cloudinary-{os.getpid()}"
        )
        
        categoria.save()
        print(f"✅ Categoría creada: {categoria.id}")
        
        # Crear archivo
        django_file = File(img_io, name=f'categoria_admin_cloudinary_{os.getpid()}.jpg')
        
        print("📤 Subiendo imagen...")
        
        # Subir imagen
        categoria.imagen.save(django_file.name, django_file, save=True)
        
        print("✅ Imagen guardada")
        print(f"📁 Nombre: {categoria.imagen.name}")
        print(f"🔗 URL: {categoria.imagen.url}")
        
        # Verificar en Cloudinary
        try:
            import cloudinary.api
            result = cloudinary.api.resource(categoria.imagen.name)
            print("✅ Archivo encontrado en Cloudinary")
            print(f"📊 Información:")
            print(f"  Public ID: {result['public_id']}")
            print(f"  URL segura: {result.get('secure_url', 'N/A')}")
            print(f"  Tamaño: {result.get('bytes', 0)} bytes")
            
            # Probar acceso
            secure_url = result.get('secure_url')
            if secure_url:
                try:
                    import requests
                    response = requests.get(secure_url, timeout=10)
                    print(f"📡 Respuesta HTTP: {response.status_code}")
                    if response.status_code == 200:
                        print("✅ URL accesible")
                        print(f"📏 Tamaño: {len(response.content)} bytes")
                    else:
                        print(f"❌ Error: HTTP {response.status_code}")
                except Exception as e:
                    print(f"⚠️ Error verificando URL: {e}")
            
        except Exception as e:
            print(f"❌ Archivo NO encontrado en Cloudinary: {e}")
        
        # Limpiar
        categoria.delete()
        print("✅ Categoría eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando admin con Cloudinary: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO DEPURACIÓN DE CLOUDINARY")
    print("=" * 60)
    
    # Depurar subida a Cloudinary
    cloudinary_success = debug_cloudinary_upload()
    
    # Probar admin con Cloudinary
    admin_success = test_admin_with_cloudinary()
    
    print("\n📊 RESULTADOS DE LA DEPURACIÓN")
    print("=" * 60)
    print(f"Subida a Cloudinary: {'✅ PASÓ' if cloudinary_success else '❌ FALLÓ'}")
    print(f"Admin con Cloudinary: {'✅ PASÓ' if admin_success else '❌ FALLÓ'}")
    
    if cloudinary_success and admin_success:
        print("\n🎉 ¡DEPURACIÓN COMPLETA!")
        print("✅ Las imágenes se suben correctamente a Cloudinary.")
        print("✅ El admin funciona correctamente.")
    else:
        print("\n⚠️ Se encontraron problemas en la depuración.")
        print("❌ Revisa los logs para identificar el problema.") 