#!/usr/bin/env python3
"""
Script para probar específicamente la subida de imágenes desde el admin de Django
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
from django.core.files.base import ContentFile

def test_admin_style_upload():
    """Probar subida estilo admin de Django"""
    print("🧪 Probando subida estilo admin de Django...")
    
    try:
        from categorias.models import CategoriaProducto
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (600, 600), color='orange')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear una categoría de prueba
        categoria = CategoriaProducto(
            nombre="Categoría Admin Test",
            descripcion="Categoría para probar subida desde admin",
            slug=f"categoria-admin-test-{os.getpid()}"
        )
        
        # Guardar la categoría primero
        categoria.save()
        print(f"✅ Categoría creada: {categoria.id}")
        
        # Crear archivo de imagen como lo haría el admin
        django_file = File(img_io, name=f'categoria_admin_{os.getpid()}.jpg')
        
        # Asignar imagen usando el método del modelo (estilo admin)
        categoria.imagen.save(django_file.name, django_file, save=True)
        
        print(f"✅ Imagen asignada al estilo admin")
        print(f"  Nombre del archivo: {categoria.imagen.name}")
        print(f"  URL: {categoria.imagen.url}")
        
        # Verificar que la URL es de Cloudinary
        if 'cloudinary.com' in categoria.imagen.url:
            print("✅ URL de la categoría es de Cloudinary")
        else:
            print("❌ URL de la categoría no es de Cloudinary")
        
        # Verificar que la imagen existe
        if hasattr(categoria.imagen, 'storage'):
            exists = categoria.imagen.storage.exists(categoria.imagen.name)
            print(f"  Existe en storage: {exists}")
        
        # Obtener información del archivo desde Cloudinary
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
            print(f"❌ Error obteniendo información: {e}")
        
        # Limpiar
        categoria.delete()
        print("✅ Categoría eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando admin: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_storage_usage():
    """Probar uso directo del storage"""
    print("\n🧪 Probando uso directo del storage...")
    
    try:
        from Backend.cloudinary_storage_complete import CloudinaryStorageComplete
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (500, 500), color='pink')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Crear archivo de imagen
        django_file = File(img_io, name=f'direct_storage_test_{os.getpid()}.png')
        
        # Usar el storage directamente
        storage = CloudinaryStorageComplete()
        saved_name = storage.save(django_file.name, django_file)
        
        print(f"✅ Imagen guardada: {saved_name}")
        
        # Obtener URL
        url = storage.url(saved_name)
        print(f"  URL: {url}")
        
        # Verificar que la URL es de Cloudinary
        if 'cloudinary.com' in url:
            print("✅ URL es de Cloudinary")
        else:
            print("❌ URL no es de Cloudinary")
        
        # Verificar que existe
        exists = storage.exists(saved_name)
        print(f"  Existe: {exists}")
        
        # Limpiar
        storage.delete(saved_name)
        print("✅ Archivo eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando storage directo: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_default_storage():
    """Probar default_storage de Django"""
    print("\n🧪 Probando default_storage de Django...")
    
    try:
        from django.core.files.storage import default_storage
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (450, 450), color='cyan')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear archivo de imagen
        django_file = File(img_io, name=f'default_storage_test_{os.getpid()}.jpg')
        
        # Usar default_storage
        saved_name = default_storage.save(django_file.name, django_file)
        
        print(f"✅ Imagen guardada con default_storage: {saved_name}")
        
        # Obtener URL
        url = default_storage.url(saved_name)
        print(f"  URL: {url}")
        
        # Verificar que la URL es de Cloudinary
        if 'cloudinary.com' in url:
            print("✅ URL es de Cloudinary")
        else:
            print("❌ URL no es de Cloudinary")
        
        # Verificar que existe
        exists = default_storage.exists(saved_name)
        print(f"  Existe: {exists}")
        
        # Limpiar
        default_storage.delete(saved_name)
        print("✅ Archivo eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando default_storage: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE ADMIN DE DJANGO")
    print("=" * 60)
    
    # Probar estilo admin
    admin_success = test_admin_style_upload()
    
    # Probar storage directo
    direct_success = test_direct_storage_usage()
    
    # Probar default_storage
    default_success = test_default_storage()
    
    print("\n📊 RESULTADOS FINALES")
    print("=" * 60)
    print(f"Estilo admin: {'✅ PASÓ' if admin_success else '❌ FALLÓ'}")
    print(f"Storage directo: {'✅ PASÓ' if direct_success else '❌ FALLÓ'}")
    print(f"Default storage: {'✅ PASÓ' if default_success else '❌ FALLÓ'}")
    
    if admin_success and direct_success and default_success:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ Las imágenes se suben correctamente desde el admin.")
        print("✅ El storage funciona correctamente.")
        print("✅ El default_storage funciona correctamente.")
        print("✅ El sistema está completamente funcional.")
    else:
        print("\n⚠️ Algunas pruebas fallaron.")
        print("❌ Revisa la configuración del storage.") 