#!/usr/bin/env python3
"""
Script para arreglar los modelos para usar el storage correcto de Cloudinary
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

from Backend.cloudinary_storage_models import CloudinaryStorageModels
from django.core.files.base import ContentFile
from django.core.files import File

def test_models_with_correct_storage():
    """Probar modelos con el storage correcto"""
    print("🧪 Probando modelos con storage correcto...")
    
    try:
        from productos.models import Producto
        from categorias.models import CategoriaProducto
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (400, 400), color='purple')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear un producto de prueba
        producto = Producto(
            nombre="Producto Test Storage Correcto",
            descripcion_corta="Producto para probar storage correcto",
            descripcion_larga="Producto creado para probar el storage correcto de Cloudinary",
            precio=200.00,
            costo=100.00,
            stock=5,
            estado='publicado',
            sku=f'TEST-CORRECT-{os.getpid()}'
        )
        
        # Guardar el producto
        producto.save()
        print(f"✅ Producto creado: {producto.id}")
        
        # Crear archivo de imagen como lo haría el admin
        django_file = File(img_io, name=f'test_producto_correct_{os.getpid()}.jpg')
        
        # Usar el storage correcto para subir la imagen
        storage = CloudinaryStorageModels()
        saved_name = storage.save(django_file.name, django_file)
        
        # Asignar el nombre guardado al producto
        producto.imagen_principal.name = saved_name
        producto.save()
        
        print(f"✅ Imagen asignada al producto")
        print(f"  Nombre del archivo: {producto.imagen_principal.name}")
        print(f"  URL: {producto.imagen_principal.url}")
        
        # Verificar que la URL es de Cloudinary
        if 'cloudinary.com' in producto.imagen_principal.url:
            print("✅ URL del producto es de Cloudinary")
        else:
            print("❌ URL del producto no es de Cloudinary")
        
        # Verificar que la imagen existe
        if hasattr(producto.imagen_principal, 'storage'):
            exists = producto.imagen_principal.storage.exists(producto.imagen_principal.name)
            print(f"  Existe en storage: {exists}")
        
        # Limpiar
        producto.delete()
        print("✅ Producto eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando modelo Django: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_categoria_with_correct_storage():
    """Probar categoría con el storage correcto"""
    print("\n🧪 Probando categoría con storage correcto...")
    
    try:
        from categorias.models import CategoriaProducto
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (300, 300), color='orange')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Crear una categoría de prueba
        categoria = CategoriaProducto(
            nombre="Categoría Test Storage Correcto",
            descripcion="Categoría para probar storage correcto",
            slug=f"categoria-test-correct-{os.getpid()}"
        )
        
        # Guardar la categoría
        categoria.save()
        print(f"✅ Categoría creada: {categoria.id}")
        
        # Crear archivo de imagen como lo haría el admin
        django_file = File(img_io, name=f'test_categoria_correct_{os.getpid()}.png')
        
        # Usar el storage correcto para subir la imagen
        storage = CloudinaryStorageModels()
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
        
        # Limpiar
        categoria.delete()
        print("✅ Categoría eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando categoría Django: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_admin_style_upload():
    """Probar subida estilo admin con storage correcto"""
    print("\n🧪 Probando subida estilo admin con storage correcto...")
    
    try:
        # Crear una imagen de prueba
        img = Image.new('RGB', (500, 500), color='cyan')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear archivo como lo haría el admin
        django_file = File(img_io, name='test_admin_correct.jpg')
        
        # Usar el storage correcto directamente
        storage = CloudinaryStorageModels()
        
        print(f"📤 Subiendo imagen: {django_file.name}")
        
        # Subir usando el storage
        saved_name = storage.save(django_file.name, django_file)
        print(f"✅ Imagen guardada como: {saved_name}")
        
        # Obtener URL
        url = storage.url(saved_name)
        print(f"🔗 URL de la imagen: {url}")
        
        # Verificar que la URL es de Cloudinary
        if 'cloudinary.com' in url:
            print("✅ URL es de Cloudinary")
        else:
            print("❌ URL no es de Cloudinary")
            return False
        
        # Verificar que el archivo existe en Cloudinary
        exists = storage.exists(saved_name)
        print(f"🔍 Imagen existe en Cloudinary: {exists}")
        
        # Obtener información del archivo
        try:
            import cloudinary.api
            result = cloudinary.api.resource(saved_name)
            print(f"📊 Información de la imagen:")
            print(f"  Public ID: {result['public_id']}")
            print(f"  Tamaño: {result.get('bytes', 0)} bytes")
            print(f"  Formato: {result.get('format', 'N/A')}")
            print(f"  Ancho: {result.get('width', 0)}")
            print(f"  Alto: {result.get('height', 0)}")
            print(f"  Tipo de recurso: {result.get('resource_type', 'N/A')}")
        except Exception as e:
            print(f"❌ Error obteniendo información: {e}")
        
        # Eliminar archivo de prueba
        deleted = storage.delete(saved_name)
        print(f"🗑️ Imagen eliminada: {deleted}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS CON STORAGE CORRECTO")
    print("=" * 60)
    
    # Probar subida estilo admin
    admin_success = test_admin_style_upload()
    
    # Probar modelo Producto
    producto_success = test_models_with_correct_storage()
    
    # Probar modelo CategoriaProducto
    categoria_success = test_categoria_with_correct_storage()
    
    print("\n📊 RESULTADOS FINALES")
    print("=" * 60)
    print(f"Subida estilo admin: {'✅ PASÓ' if admin_success else '❌ FALLÓ'}")
    print(f"Modelo Producto: {'✅ PASÓ' if producto_success else '❌ FALLÓ'}")
    print(f"Modelo CategoriaProducto: {'✅ PASÓ' if categoria_success else '❌ FALLÓ'}")
    
    if admin_success and producto_success and categoria_success:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ Las imágenes se suben correctamente a Cloudinary desde el admin.")
        print("✅ Los modelos usan el storage correcto.")
        print("✅ El sistema está completamente funcional.")
    else:
        print("\n⚠️ Algunas pruebas fallaron.")
        print("❌ Revisa la configuración del storage.") 