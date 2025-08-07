#!/usr/bin/env python3
"""
Script para probar subida de imágenes a Cloudinary
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

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def test_image_upload():
    """Probar subida de imagen a Cloudinary"""
    print("🧪 Probando subida de imagen a Cloudinary...")
    
    try:
        # Crear una imagen de prueba
        img = Image.new('RGB', (300, 300), color='red')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear archivo de prueba
        test_content = ContentFile(img_io.getvalue())
        test_name = f"test_image_{os.getpid()}.jpg"
        
        print(f"📤 Subiendo imagen: {test_name}")
        
        # Subir usando el storage de Django
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
        deleted = default_storage.delete(saved_name)
        print(f"🗑️ Imagen eliminada: {deleted}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def test_django_model_image():
    """Probar subida de imagen a través de un modelo Django"""
    print("\n🧪 Probando subida de imagen a través de modelo Django...")
    
    try:
        from productos.models import Producto
        from django.core.files import File
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (400, 400), color='blue')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Crear un producto de prueba
        producto = Producto(
            nombre="Producto Test Imagen Cloudinary",
            descripcion_corta="Producto para probar imágenes en Cloudinary",
            descripcion_larga="Producto creado para probar la funcionalidad de imágenes en Cloudinary",
            precio=200.00,
            costo=100.00,
            stock=5,
            estado='publicado',
            sku=f'TEST-IMG-{os.getpid()}'
        )
        
        # Guardar el producto
        producto.save()
        print(f"✅ Producto creado: {producto.id}")
        
        # Crear archivo de imagen
        django_file = File(img_io, name=f'test_producto_imagen_{os.getpid()}.png')
        
        # Asignar imagen al producto
        producto.imagen_principal.save(f'test_producto_imagen_{os.getpid()}.png', django_file, save=True)
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
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE SUBIDA DE IMÁGENES")
    print("=" * 60)
    
    # Probar subida directa
    direct_success = test_image_upload()
    
    # Probar subida a través de modelo
    model_success = test_django_model_image()
    
    print("\n📊 RESULTADOS")
    print("=" * 60)
    print(f"Subida directa: {'✅ PASÓ' if direct_success else '❌ FALLÓ'}")
    print(f"Subida por modelo: {'✅ PASÓ' if model_success else '❌ FALLÓ'}")
    
    if direct_success and model_success:
        print("\n🎉 ¡Todas las pruebas pasaron! Las imágenes se suben correctamente a Cloudinary.")
    else:
        print("\n⚠️ Algunas pruebas fallaron.") 