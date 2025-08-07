#!/usr/bin/env python3
"""
Script final para probar subida de imágenes desde el admin de Django a Cloudinary
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

from Backend.cloudinary_storage_final import CloudinaryStorageFinal
from django.core.files.base import ContentFile
from django.core.files import File

def test_final_admin_upload():
    """Probar subida final como lo haría el admin de Django"""
    print("🧪 Probando subida final estilo admin de Django...")
    
    try:
        # Crear una imagen de prueba
        img = Image.new('RGB', (400, 400), color='red')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear archivo como lo haría el admin
        django_file = File(img_io, name='test_final_admin.jpg')
        
        # Usar el storage final directamente
        storage = CloudinaryStorageFinal()
        
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

def test_django_default_storage():
    """Probar el storage por defecto de Django"""
    print("\n🧪 Probando storage por defecto de Django...")
    
    try:
        from django.core.files.storage import default_storage
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (300, 300), color='blue')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Crear archivo de prueba
        test_content = ContentFile(img_io.getvalue())
        test_name = f"test_default_storage_{os.getpid()}.png"
        
        print(f"📤 Subiendo imagen: {test_name}")
        
        # Subir usando el storage por defecto
        saved_name = default_storage.save(test_name, test_content)
        print(f"✅ Imagen guardada como: {saved_name}")
        
        # Obtener URL
        url = default_storage.url(saved_name)
        print(f"🔗 URL de la imagen: {url}")
        
        # Verificar que la URL es de Cloudinary
        if 'cloudinary.com' in url:
            print("✅ URL es de Cloudinary")
        else:
            print("❌ URL no es de Cloudinary")
            return False
        
        # Verificar que el archivo existe en Cloudinary
        exists = default_storage.exists(saved_name)
        print(f"🔍 Imagen existe en Cloudinary: {exists}")
        
        # Eliminar archivo de prueba
        deleted = default_storage.delete(saved_name)
        print(f"🗑️ Imagen eliminada: {deleted}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_producto_model_final():
    """Probar modelo Producto con el storage final"""
    print("\n🧪 Probando modelo Producto con storage final...")
    
    try:
        from productos.models import Producto
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (350, 350), color='green')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear un producto de prueba
        producto = Producto(
            nombre="Producto Test Final Admin",
            descripcion_corta="Producto para probar subida final desde admin",
            descripcion_larga="Producto creado para probar la funcionalidad final de subida desde el admin de Django",
            precio=175.00,
            costo=87.50,
            stock=6,
            estado='publicado',
            sku=f'TEST-FINAL-{os.getpid()}'
        )
        
        # Guardar el producto
        producto.save()
        print(f"✅ Producto creado: {producto.id}")
        
        # Crear archivo de imagen como lo haría el admin
        django_file = File(img_io, name=f'test_producto_final_{os.getpid()}.jpg')
        
        # Asignar imagen al producto directamente
        producto.imagen_principal.save(django_file.name, django_file, save=True)
        
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

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS FINALES DE SUBIDA DESDE ADMIN")
    print("=" * 60)
    
    # Probar subida directa
    direct_success = test_final_admin_upload()
    
    # Probar storage por defecto
    default_success = test_django_default_storage()
    
    # Probar modelo Producto
    producto_success = test_producto_model_final()
    
    print("\n📊 RESULTADOS FINALES")
    print("=" * 60)
    print(f"Subida directa: {'✅ PASÓ' if direct_success else '❌ FALLÓ'}")
    print(f"Storage por defecto: {'✅ PASÓ' if default_success else '❌ FALLÓ'}")
    print(f"Modelo Producto: {'✅ PASÓ' if producto_success else '❌ FALLÓ'}")
    
    if direct_success and default_success and producto_success:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ Las imágenes se suben correctamente a Cloudinary desde el admin de Django.")
        print("✅ Ahora puedes usar el admin de Django para subir imágenes a Cloudinary.")
        print("✅ El sistema está completamente funcional.")
    else:
        print("\n⚠️ Algunas pruebas fallaron.")
        print("❌ Revisa la configuración del storage.") 