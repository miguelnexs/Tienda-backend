#!/usr/bin/env python3
"""
Script para diagnosticar problemas de subida en producción
"""
import os
import sys
import django
from pathlib import Path
import tempfile
from PIL import Image
import io

# Configurar Django con render_settings
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

def check_production_environment():
    """Verificar el entorno de producción"""
    print("🚀 VERIFICANDO ENTORNO DE PRODUCCIÓN")
    print("=" * 50)
    
    # Verificar variables de entorno
    print("📋 Variables de entorno:")
    render = os.environ.get('RENDER', 'No')
    debug = os.environ.get('DEBUG', 'No')
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'No configurado')
    
    print(f"  RENDER: {render}")
    print(f"  DEBUG: {debug}")
    print(f"  DJANGO_SETTINGS_MODULE: {settings_module}")
    
    # Verificar configuración de Django
    from django.conf import settings
    print(f"\n⚙️ Configuración de Django:")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"  MEDIA_URL: {settings.MEDIA_URL}")
    print(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")
    
    # Verificar Cloudinary
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
    api_key = os.environ.get('CLOUDINARY_API_KEY')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
    
    print(f"\n☁️ Configuración de Cloudinary:")
    print(f"  CLOUDINARY_CLOUD_NAME: {cloud_name}")
    print(f"  CLOUDINARY_API_KEY: {api_key[:10] if api_key else 'No configurado'}...")
    print(f"  CLOUDINARY_API_SECRET: {api_secret[:10] if api_secret else 'No configurado'}...")
    
    return True

def test_storage_in_production():
    """Probar el storage en producción"""
    print("\n🔧 PROBANDO STORAGE EN PRODUCCIÓN")
    print("=" * 50)
    
    try:
        from django.conf import settings
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        print(f"1. Storage configurado: {type(default_storage).__name__}")
        print(f"2. Clase del storage: {settings.DEFAULT_FILE_STORAGE}")
        
        # Verificar si es CloudinaryStorage
        if 'CloudinaryStorage' in str(type(default_storage)):
            print("✅ Usando CloudinaryStorage")
        else:
            print("❌ NO está usando CloudinaryStorage")
            print(f"   Storage actual: {type(default_storage).__name__}")
        
        # Probar operaciones básicas
        test_content = b"Test content for production storage"
        test_file = ContentFile(test_content)
        
        # Guardar archivo
        saved_name = default_storage.save("test_production_storage.txt", test_file)
        print(f"3. Archivo guardado como: {saved_name}")
        
        # Verificar existencia
        exists = default_storage.exists(saved_name)
        print(f"4. Archivo existe: {exists}")
        
        # Obtener URL
        url = default_storage.url(saved_name)
        print(f"5. URL del archivo: {url}")
        
        # Verificar si la URL es de Cloudinary
        if 'cloudinary.com' in url:
            print("✅ URL de Cloudinary detectada")
        else:
            print("⚠️ URL no es de Cloudinary")
        
        # Eliminar archivo
        default_storage.delete(saved_name)
        print("6. Archivo eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando storage: {e}")
        return False

def test_image_upload_simulation():
    """Simular subida de imagen como lo haría el frontend"""
    print("\n📤 SIMULANDO SUBIDA DE IMAGEN")
    print("=" * 50)
    
    try:
        from django.test import Client
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        client = Client()
        
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 200), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Crear archivo como lo haría el frontend
        image_file = SimpleUploadedFile(
            "test_upload.png",
            buffer.getvalue(),
            content_type="image/png"
        )
        
        # Simular petición POST como lo haría el frontend
        data = {
            'nombre': 'Test Color',
            'hex_code': '#FF0000',
            'stock': '10',
            'activo': 'true'
        }
        
        files = {
            'imagenes': image_file
        }
        
        print("1. Enviando petición POST simulada...")
        
        # Intentar crear un color con imagen
        response = client.post(
            '/api/productos/productos/1/colores/',
            data=data,
            files=files,
            content_type='multipart/form-data'
        )
        
        print(f"2. Status Code: {response.status_code}")
        print(f"3. Response: {response.content.decode()[:200]}...")
        
        if response.status_code in [200, 201]:
            print("✅ Subida simulada exitosa")
            return True
        else:
            print("❌ Subida simulada falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en simulación: {e}")
        return False

def test_cloudinary_direct_upload():
    """Probar subida directa a Cloudinary"""
    print("\n☁️ PROBANDO SUBIDA DIRECTA A CLOUDINARY")
    print("=" * 50)
    
    try:
        import cloudinary
        import cloudinary.uploader
        
        # Configurar Cloudinary
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET')
        )
        
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 200), color='blue')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Subir imagen directamente
        result = cloudinary.uploader.upload(
            buffer,
            public_id='test_production_direct',
            overwrite=True,
            invalidate=True
        )
        
        print("✅ Subida directa exitosa")
        print(f"  Public ID: {result['public_id']}")
        print(f"  URL: {result['secure_url']}")
        print(f"  Tamaño: {result['bytes']} bytes")
        
        # Eliminar imagen de prueba
        delete_result = cloudinary.uploader.destroy('test_production_direct')
        if delete_result.get('result') == 'ok':
            print("✅ Imagen de prueba eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en subida directa: {e}")
        return False

def test_serializer_with_image():
    """Probar serializer con imagen"""
    print("\n📝 PROBANDO SERIALIZER CON IMAGEN")
    print("=" * 50)
    
    try:
        from productos.models import Producto, ColorProducto, ImagenProducto
        from productos.serializers.color import ColorProductoCreateSerializer
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Verificar si hay productos para probar
        productos = Producto.objects.all()[:1]
        if not productos:
            print("⚠️ No hay productos para probar")
            return False
        
        producto = productos[0]
        print(f"1. Producto encontrado: {producto.nombre}")
        
        # Crear imagen de prueba
        img = Image.new('RGB', (100, 100), color='green')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        image_file = SimpleUploadedFile(
            "test_serializer.png",
            buffer.getvalue(),
            content_type="image/png"
        )
        
        # Crear datos de prueba
        test_data = {
            'nombre': 'Test Color Serializer',
            'hex_code': '#00FF00',
            'stock': 5,
            'activo': True,
            'producto': producto.id
        }
        
        # Crear serializer
        serializer = ColorProductoCreateSerializer(data=test_data)
        
        if serializer.is_valid():
            print("2. ✅ Serializer válido")
            print(f"   Datos validados: {serializer.validated_data}")
            
            # Intentar guardar
            try:
                color = serializer.save(producto=producto)
                print(f"3. ✅ Color creado: {color.id}")
                
                # Crear imagen para el color
                imagen = ImagenProducto.objects.create(
                    color=color,
                    imagen=image_file,
                    orden=1,
                    es_principal=True
                )
                print(f"4. ✅ Imagen creada: {imagen.id}")
                print(f"   URL: {imagen.imagen.url}")
                
                return True
                
            except Exception as e:
                print(f"3. ❌ Error guardando: {e}")
                return False
        else:
            print("2. ❌ Serializer inválido")
            print(f"   Errores: {serializer.errors}")
            return False
        
    except Exception as e:
        print(f"❌ Error probando serializer: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 DIAGNÓSTICO DE SUBIDA DE IMÁGENES EN PRODUCCIÓN")
    print("=" * 60)
    
    tests = [
        ("Entorno Producción", check_production_environment),
        ("Storage Producción", test_storage_in_production),
        ("Subida Simulada", test_image_upload_simulation),
        ("Cloudinary Directo", test_cloudinary_direct_upload),
        ("Serializer con Imagen", test_serializer_with_image),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results[test_name] = False
    
    # Resumen
    print("\n📊 RESUMEN DE DIAGNÓSTICO")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! El problema puede estar en el frontend.")
    elif passed >= 3:
        print("✅ La mayoría de las pruebas pasaron. Revisa los logs específicos.")
    else:
        print("⚠️ Varias pruebas fallaron. Hay problemas de configuración.")
    
    return passed >= 3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 