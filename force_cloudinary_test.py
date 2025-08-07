#!/usr/bin/env python3
"""
Script para forzar el uso de CloudinaryStorage y probarlo directamente
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

from Backend.cloudinary_storage import CloudinaryStorage
from django.core.files.base import ContentFile

def test_forced_cloudinary():
    """Probar CloudinaryStorage directamente"""
    print("🧪 Probando CloudinaryStorage directamente...")
    
    try:
        # Crear instancia del storage
        storage = CloudinaryStorage()
        print("✅ CloudinaryStorage creado")
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (250, 250), color='green')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear archivo de prueba
        test_content = ContentFile(img_io.getvalue())
        test_name = f"test_forced_{os.getpid()}.jpg"
        
        print(f"📤 Subiendo imagen: {test_name}")
        
        # Subir usando el storage directamente
        saved_name = storage.save(test_name, test_content)
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

def test_django_model_with_forced_storage():
    """Probar modelo Django con storage forzado"""
    print("\n🧪 Probando modelo Django con storage forzado...")
    
    try:
        from productos.models import Producto
        from django.core.files import File
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (350, 350), color='purple')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Crear un producto de prueba
        producto = Producto(
            nombre="Producto Test Storage Forzado",
            descripcion_corta="Producto para probar storage forzado",
            descripcion_larga="Producto creado para probar el storage forzado",
            precio=300.00,
            costo=150.00,
            stock=3,
            estado='publicado',
            sku=f'TEST-FORCED-{os.getpid()}'
        )
        
        # Guardar el producto
        producto.save()
        print(f"✅ Producto creado: {producto.id}")
        
        # Crear archivo de imagen
        django_file = File(img_io, name=f'test_producto_forced_{os.getpid()}.png')
        
        # Asignar imagen al producto usando el storage forzado
        storage = CloudinaryStorage()
        saved_name = storage.save(f'test_producto_forced_{os.getpid()}.png', django_file)
        
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
        
        # Limpiar
        producto.delete()
        print("✅ Producto eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando modelo Django: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS CON STORAGE FORZADO")
    print("=" * 60)
    
    # Probar storage directo
    direct_success = test_forced_cloudinary()
    
    # Probar modelo con storage forzado
    model_success = test_django_model_with_forced_storage()
    
    print("\n📊 RESULTADOS")
    print("=" * 60)
    print(f"Storage directo: {'✅ PASÓ' if direct_success else '❌ FALLÓ'}")
    print(f"Modelo con storage forzado: {'✅ PASÓ' if model_success else '❌ FALLÓ'}")
    
    if direct_success and model_success:
        print("\n🎉 ¡Todas las pruebas pasaron! CloudinaryStorage funciona correctamente.")
    else:
        print("\n⚠️ Algunas pruebas fallaron.") 