#!/usr/bin/env python3
"""
Script de prueba para verificar que las imágenes se suben realmente a Cloudinary
"""
import os
import sys
import django
from io import BytesIO
from PIL import Image
import requests

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import cloudinary
import cloudinary.api

def test_real_cloudinary_upload():
    """Probar subida real a Cloudinary"""
    print("🧪 Probando subida real a Cloudinary...")
    
    try:
        # Crear una imagen de prueba
        img = Image.new('RGB', (300, 300), color='red')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear archivo de prueba
        test_content = ContentFile(img_io.getvalue())
        test_name = f"test_real_upload_{os.getpid()}.jpg"
        
        print(f"📤 Subiendo archivo: {test_name}")
        
        # Subir usando el storage de Django
        saved_name = default_storage.save(test_name, test_content)
        print(f"✅ Archivo guardado como: {saved_name}")
        
        # Obtener URL
        url = default_storage.url(saved_name)
        print(f"🔗 URL del archivo: {url}")
        
        # Verificar que la URL es de Cloudinary
        if 'cloudinary.com' in url:
            print("✅ URL es de Cloudinary")
        else:
            print("❌ URL no es de Cloudinary")
            return False
        
        # Verificar que el archivo existe en Cloudinary
        exists = default_storage.exists(saved_name)
        print(f"🔍 Archivo existe en Cloudinary: {exists}")
        
        # Intentar acceder a la URL
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("✅ Imagen accesible desde URL de Cloudinary")
                print(f"📏 Tamaño de respuesta: {len(response.content)} bytes")
            else:
                print(f"❌ Error accediendo a la imagen: {response.status_code}")
        except Exception as e:
            print(f"❌ Error verificando URL: {e}")
        
        # Obtener información del archivo desde Cloudinary
        try:
            result = cloudinary.api.resource(saved_name)
            print(f"📊 Información de Cloudinary:")
            print(f"  Public ID: {result['public_id']}")
            print(f"  Tamaño: {result.get('bytes', 0)} bytes")
            print(f"  Formato: {result.get('format', 'N/A')}")
            print(f"  Ancho: {result.get('width', 0)}")
            print(f"  Alto: {result.get('height', 0)}")
        except Exception as e:
            print(f"❌ Error obteniendo información de Cloudinary: {e}")
        
        # Eliminar archivo de prueba
        deleted = default_storage.delete(saved_name)
        print(f"🗑️ Archivo eliminado: {deleted}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def test_django_model_upload():
    """Probar subida a través de un modelo Django"""
    print("\n🧪 Probando subida a través de modelo Django...")
    
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
            nombre="Producto Test Cloudinary Real",
            descripcion_corta="Producto para probar Cloudinary real",
            descripcion_larga="Producto creado para probar la funcionalidad real de Cloudinary",
            precio=150.00,
            costo=75.00,
            stock=5,
            estado='publicado',
            sku=f'TEST-REAL-{os.getpid()}'
        )
        
        # Guardar el producto
        producto.save()
        print(f"✅ Producto creado: {producto.id}")
        
        # Crear archivo de imagen
        django_file = File(img_io, name=f'test_producto_real_{os.getpid()}.png')
        
        # Asignar imagen al producto
        producto.imagen_principal.save(f'test_producto_real_{os.getpid()}.png', django_file, save=True)
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

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DE CLOUDINARY REAL")
    print("=" * 60)
    
    tests = [
        ("Subida directa a Cloudinary", test_real_cloudinary_upload),
        ("Subida a través de modelo Django", test_django_model_upload),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results[test_name] = False
    
    # Resumen de resultados
    print("\n📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:35} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO FINAL: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! Las imágenes se suben realmente a Cloudinary.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración de Cloudinary.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 