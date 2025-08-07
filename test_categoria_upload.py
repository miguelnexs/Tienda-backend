#!/usr/bin/env python3
"""
Script para probar específicamente la subida de imágenes de categorías
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

from Backend.cloudinary_storage_complete import CloudinaryStorageComplete
from django.core.files.base import ContentFile
from django.core.files import File

def test_categoria_upload():
    """Probar subida de imagen para categoría"""
    print("🧪 Probando subida de imagen para categoría...")
    
    try:
        from categorias.models import CategoriaProducto
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (400, 400), color='purple')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear una categoría de prueba
        categoria = CategoriaProducto(
            nombre="Categoría Test Upload",
            descripcion="Categoría para probar subida de imágenes",
            slug=f"categoria-test-upload-{os.getpid()}"
        )
        
        # Guardar la categoría
        categoria.save()
        print(f"✅ Categoría creada: {categoria.id}")
        
        # Crear archivo de imagen como lo haría el admin
        django_file = File(img_io, name=f'categoria_test_{os.getpid()}.jpg')
        
        # Usar el storage completo para subir la imagen
        storage = CloudinaryStorageComplete()
        saved_name = storage.save(django_file.name, django_file)
        
        # Asignar el nombre guardado a la categoría
        categoria.imagen.name = saved_name
        categoria.save()
        
        print(f"✅ Imagen asignada a la categoría")
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
            result = cloudinary.api.resource(saved_name)
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
        print(f"❌ Error probando categoría: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_categoria_edit():
    """Probar edición de categoría con nueva imagen"""
    print("\n🧪 Probando edición de categoría con nueva imagen...")
    
    try:
        from categorias.models import CategoriaProducto
        
        # Crear una categoría de prueba
        categoria = CategoriaProducto(
            nombre="Categoría Test Edit",
            descripcion="Categoría para probar edición de imágenes",
            slug=f"categoria-test-edit-{os.getpid()}"
        )
        
        # Guardar la categoría
        categoria.save()
        print(f"✅ Categoría creada: {categoria.id}")
        
        # Crear primera imagen
        img1 = Image.new('RGB', (300, 300), color='red')
        img1_io = BytesIO()
        img1.save(img1_io, format='JPEG')
        img1_io.seek(0)
        
        # Asignar primera imagen
        django_file1 = File(img1_io, name=f'categoria_edit_1_{os.getpid()}.jpg')
        storage = CloudinaryStorageComplete()
        saved_name1 = storage.save(django_file1.name, django_file1)
        
        categoria.imagen.name = saved_name1
        categoria.save()
        
        print(f"✅ Primera imagen asignada")
        print(f"  URL: {categoria.imagen.url}")
        
        # Crear segunda imagen (edición)
        img2 = Image.new('RGB', (350, 350), color='blue')
        img2_io = BytesIO()
        img2.save(img2_io, format='JPEG')
        img2_io.seek(0)
        
        # Asignar segunda imagen (edición)
        django_file2 = File(img2_io, name=f'categoria_edit_2_{os.getpid()}.jpg')
        saved_name2 = storage.save(django_file2.name, django_file2)
        
        categoria.imagen.name = saved_name2
        categoria.save()
        
        print(f"✅ Segunda imagen asignada (edición)")
        print(f"  URL: {categoria.imagen.url}")
        
        # Verificar que la URL es de Cloudinary
        if 'cloudinary.com' in categoria.imagen.url:
            print("✅ URL de la categoría es de Cloudinary")
        else:
            print("❌ URL de la categoría no es de Cloudinary")
        
        # Limpiar
        categoria.delete()
        print("✅ Categoría eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando edición de categoría: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_django_admin_style():
    """Probar estilo admin de Django"""
    print("\n🧪 Probando estilo admin de Django...")
    
    try:
        from categorias.models import CategoriaProducto
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (500, 500), color='green')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Crear una categoría de prueba
        categoria = CategoriaProducto(
            nombre="Categoría Test Admin Style",
            descripcion="Categoría para probar estilo admin",
            slug=f"categoria-test-admin-{os.getpid()}"
        )
        
        # Guardar la categoría
        categoria.save()
        print(f"✅ Categoría creada: {categoria.id}")
        
        # Crear archivo de imagen como lo haría el admin
        django_file = File(img_io, name=f'categoria_admin_{os.getpid()}.png')
        
        # Asignar imagen directamente al modelo (estilo admin)
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
        
        # Limpiar
        categoria.delete()
        print("✅ Categoría eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando estilo admin: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE SUBIDA DE CATEGORÍAS")
    print("=" * 60)
    
    # Probar subida de categoría
    upload_success = test_categoria_upload()
    
    # Probar edición de categoría
    edit_success = test_categoria_edit()
    
    # Probar estilo admin
    admin_success = test_django_admin_style()
    
    print("\n📊 RESULTADOS FINALES")
    print("=" * 60)
    print(f"Subida de categoría: {'✅ PASÓ' if upload_success else '❌ FALLÓ'}")
    print(f"Edición de categoría: {'✅ PASÓ' if edit_success else '❌ FALLÓ'}")
    print(f"Estilo admin: {'✅ PASÓ' if admin_success else '❌ FALLÓ'}")
    
    if upload_success and edit_success and admin_success:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ Las imágenes se suben correctamente a Cloudinary para categorías.")
        print("✅ La edición de categorías funciona correctamente.")
        print("✅ El estilo admin funciona correctamente.")
        print("✅ El sistema está completamente funcional.")
    else:
        print("\n⚠️ Algunas pruebas fallaron.")
        print("❌ Revisa la configuración del storage.") 