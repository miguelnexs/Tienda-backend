#!/usr/bin/env python3
"""
Script de depuración detallado para rastrear el proceso de subida de imágenes
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

def debug_detallado_subida():
    """Depuración detallada del proceso de subida"""
    print("🔍 DEPURACIÓN DETALLADA DEL PROCESO DE SUBIDA")
    print("=" * 60)
    
    try:
        # PASO 1: Crear imagen de prueba
        print("\n📸 PASO 1: Creando imagen de prueba...")
        img = Image.new('RGB', (800, 600), color='#FF6B6B')  # Rojo
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=90)
        img_io.seek(0)
        
        print(f"✅ Imagen creada: {len(img_io.getvalue())} bytes")
        print(f"📐 Dimensiones: {img.size}")
        
        # PASO 2: Crear categoría
        print("\n📝 PASO 2: Creando categoría...")
        categoria = CategoriaProducto(
            nombre="Categoría Debug Detallado",
            descripcion="Categoría para depuración detallada",
            slug=f"categoria-debug-detallado-{os.getpid()}"
        )
        
        categoria.save()
        print(f"✅ Categoría creada: ID {categoria.id}")
        print(f"📋 Nombre: {categoria.nombre}")
        print(f"📋 Slug: {categoria.slug}")
        
        # PASO 3: Verificar configuración antes de subir
        print("\n⚙️ PASO 3: Verificando configuración...")
        print(f"📁 DEFAULT_FILE_STORAGE: {getattr(django.conf.settings, 'DEFAULT_FILE_STORAGE', 'No definido')}")
        print(f"📁 default_storage class: {type(default_storage).__name__}")
        print(f"📁 default_storage module: {type(default_storage).__module__}")
        
        # PASO 4: Crear archivo Django
        print("\n📁 PASO 4: Creando archivo Django...")
        django_file = File(img_io, name=f'categoria_debug_detallado_{os.getpid()}.jpg')
        
        print(f"📁 Nombre del archivo: {django_file.name}")
        print(f"📁 Tamaño del archivo: {len(django_file.read())} bytes")
        django_file.seek(0)  # Resetear posición
        
        # PASO 5: Verificar storage antes de subir
        print("\n🔧 PASO 5: Verificando storage antes de subir...")
        if hasattr(categoria.imagen, 'storage'):
            print(f"📁 Storage del campo imagen: {type(categoria.imagen.storage).__name__}")
        else:
            print("❌ No hay storage en el campo imagen")
        
        # PASO 6: Subir imagen (exactamente como lo hace el admin)
        print("\n📤 PASO 6: Subiendo imagen...")
        print("🔄 Llamando a: categoria.imagen.save(django_file.name, django_file, save=True)")
        
        # Capturar el proceso de subida
        try:
            categoria.imagen.save(django_file.name, django_file, save=True)
            print("✅ Imagen guardada en el modelo")
        except Exception as e:
            print(f"❌ Error guardando imagen: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # PASO 7: Verificar resultado
        print("\n📊 PASO 7: Verificando resultado...")
        print(f"📁 Nombre del archivo guardado: {categoria.imagen.name}")
        print(f"🔗 URL generada: {categoria.imagen.url}")
        
        # Verificar si la URL es de Cloudinary
        if 'cloudinary.com' in categoria.imagen.url:
            print("✅ URL es de Cloudinary")
        else:
            print("❌ URL no es de Cloudinary")
        
        # PASO 8: Verificar existencia en storage
        print("\n🔍 PASO 8: Verificando existencia en storage...")
        if hasattr(categoria.imagen, 'storage'):
            exists = categoria.imagen.storage.exists(categoria.imagen.name)
            print(f"📁 Existe en storage: {exists}")
            
            # Intentar obtener información del storage
            try:
                size = categoria.imagen.storage.size(categoria.imagen.name)
                print(f"📏 Tamaño en storage: {size} bytes")
            except Exception as e:
                print(f"⚠️ No se pudo obtener tamaño: {e}")
        else:
            print("❌ No hay storage disponible")
        
        # PASO 9: Verificar directamente en Cloudinary
        print("\n☁️ PASO 9: Verificando directamente en Cloudinary...")
        try:
            import cloudinary.api
            result = cloudinary.api.resource(categoria.imagen.name)
            print("✅ Archivo encontrado en Cloudinary")
            print(f"📊 Información de Cloudinary:")
            print(f"  🆔 Public ID: {result['public_id']}")
            print(f"  🔗 URL segura: {result.get('secure_url', 'N/A')}")
            print(f"  📏 Tamaño: {result.get('bytes', 0)} bytes")
            print(f"  🖼️ Formato: {result.get('format', 'N/A')}")
            print(f"  📐 Dimensiones: {result.get('width', 0)}x{result.get('height', 0)}")
            print(f"  🔄 Versión: {result.get('version', 'N/A')}")
            
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
                        print(f"📏 Tamaño de respuesta: {len(response.content)} bytes")
                    else:
                        print(f"❌ Error en URL segura: HTTP {response.status_code}")
                except Exception as e:
                    print(f"⚠️ Error verificando URL segura: {e}")
            
        except Exception as e:
            print(f"❌ Archivo NO encontrado en Cloudinary: {e}")
            print("🔍 Intentando con diferentes variaciones del nombre...")
            
            # Intentar con diferentes variaciones
            variations = [
                categoria.imagen.name,
                categoria.imagen.name + '.jpg',
                categoria.imagen.name.replace('.jpg', ''),
                categoria.imagen.name.replace('categorias/', '')
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
        
        # PASO 10: Probar acceso a la URL generada
        print("\n🌐 PASO 10: Probando acceso a la URL generada...")
        try:
            import requests
            response = requests.get(categoria.imagen.url, timeout=10)
            print(f"📡 Respuesta HTTP: {response.status_code}")
            if response.status_code == 200:
                print("✅ URL generada accesible")
                print(f"📏 Tamaño de respuesta: {len(response.content)} bytes")
            else:
                print(f"❌ Error en URL generada: HTTP {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error verificando URL generada: {e}")
        
        # PASO 11: Verificar configuración después de subir
        print("\n⚙️ PASO 11: Verificando configuración después de subir...")
        print(f"📁 default_storage class: {type(default_storage).__name__}")
        print(f"📁 default_storage module: {type(default_storage).__module__}")
        
        # Limpiar
        categoria.delete()
        print("\n✅ Categoría eliminada (limpieza)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en depuración detallada: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_storage_directo():
    """Depurar storage directo"""
    print("\n🔧 DEPURANDO STORAGE DIRECTO")
    print("=" * 60)
    
    try:
        from Backend.cloudinary_storage_fixed_urls import CloudinaryStorageFixedURLs
        
        # Crear imagen
        img = Image.new('RGB', (500, 500), color='#3498DB')  # Azul
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear archivo
        django_file = File(img_io, name=f'debug_storage_directo_{os.getpid()}.jpg')
        
        print(f"📁 Archivo creado: {django_file.name}")
        print(f"📏 Tamaño: {len(django_file.read())} bytes")
        django_file.seek(0)
        
        # Usar storage directamente
        storage = CloudinaryStorageFixedURLs()
        print("🔧 Storage inicializado")
        
        # Subir archivo
        print("📤 Subiendo archivo...")
        saved_name = storage.save(django_file.name, django_file)
        print(f"✅ Archivo guardado como: {saved_name}")
        
        # Obtener URL
        url = storage.url(saved_name)
        print(f"🔗 URL: {url}")
        
        # Verificar existencia
        exists = storage.exists(saved_name)
        print(f"📁 Existe: {exists}")
        
        # Verificar en Cloudinary
        try:
            import cloudinary.api
            result = cloudinary.api.resource(saved_name)
            print("✅ Archivo encontrado en Cloudinary")
            print(f"🔗 URL segura: {result.get('secure_url')}")
        except Exception as e:
            print(f"❌ Archivo NO encontrado en Cloudinary: {e}")
        
        # Limpiar
        storage.delete(saved_name)
        print("✅ Archivo eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error depurando storage directo: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO DEPURACIÓN DETALLADA")
    print("=" * 60)
    
    # Depurar proceso completo
    debug_success = debug_detallado_subida()
    
    # Depurar storage directo
    storage_success = debug_storage_directo()
    
    print("\n📊 RESULTADOS DE LA DEPURACIÓN")
    print("=" * 60)
    print(f"Proceso completo: {'✅ PASÓ' if debug_success else '❌ FALLÓ'}")
    print(f"Storage directo: {'✅ PASÓ' if storage_success else '❌ FALLÓ'}")
    
    if debug_success and storage_success:
        print("\n🎉 ¡DEPURACIÓN COMPLETA!")
        print("✅ El proceso está funcionando correctamente.")
    else:
        print("\n⚠️ Se encontraron problemas en la depuración.")
        print("❌ Revisa los logs para identificar el problema.") 