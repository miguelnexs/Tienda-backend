#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión y funcionalidad de Cloudinary
"""
import os
import sys
import django
from pathlib import Path
import tempfile
import requests
from PIL import Image
import io

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

# Importar después de configurar Django
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings
from Backend.cloudinary_storage import CloudinaryStorage

def test_cloudinary_config():
    """Probar la configuración de Cloudinary"""
    print("🔧 PROBANDO CONFIGURACIÓN DE CLOUDINARY")
    print("=" * 50)
    
    # Verificar variables de entorno
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'do1ntnlop')
    api_key = os.environ.get('CLOUDINARY_API_KEY', '117225377115856')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET', 'e0YSrk3sT_70-ijM6mwdFBIWP9w')
    
    print(f"📋 Variables de entorno:")
    print(f"  CLOUDINARY_CLOUD_NAME: {cloud_name}")
    print(f"  CLOUDINARY_API_KEY: {api_key[:10]}...")
    print(f"  CLOUDINARY_API_SECRET: {api_secret[:10]}...")
    
    # Verificar configuración de Django
    print(f"\n⚙️ Configuración de Django:")
    print(f"  DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    print(f"  MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'No configurado')}")
    print(f"  MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'No configurado')}")
    
    # Verificar configuración de Cloudinary
    try:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        print(f"\n✅ Cloudinary configurado correctamente")
        print(f"  Cloud Name: {cloudinary.config().cloud_name}")
        print(f"  API Key: {cloudinary.config().api_key[:10]}...")
    except Exception as e:
        print(f"\n❌ Error configurando Cloudinary: {e}")
        return False
    
    return True

def test_cloudinary_connection():
    """Probar la conexión a Cloudinary"""
    print("\n🌐 PROBANDO CONEXIÓN A CLOUDINARY")
    print("=" * 50)
    
    try:
        # Intentar obtener información de la cuenta
        result = cloudinary.api.ping()
        print("✅ Conexión exitosa a Cloudinary")
        print(f"  Status: {result.get('status', 'OK')}")
        
        # Obtener información básica de la cuenta
        print(f"  Cloud Name: {cloudinary.config().cloud_name}")
        print(f"  API Key: {cloudinary.config().api_key[:10]}...")
        print(f"  Status: Conectado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def create_test_image():
    """Crear una imagen de prueba"""
    print("\n🖼️ CREANDO IMAGEN DE PRUEBA")
    print("=" * 50)
    
    try:
        # Crear una imagen simple con PIL
        img = Image.new('RGB', (200, 200), color='red')
        
        # Agregar texto
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        draw.text((50, 90), "TEST", fill='white')
        draw.text((30, 120), "CLOUDINARY", fill='white')
        
        # Guardar en buffer
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        print("✅ Imagen de prueba creada correctamente")
        print(f"  Tamaño: {img.size}")
        print(f"  Formato: PNG")
        print(f"  Tamaño del buffer: {len(buffer.getvalue())} bytes")
        
        return buffer
        
    except Exception as e:
        print(f"❌ Error creando imagen de prueba: {e}")
        return None

def test_upload_to_cloudinary():
    """Probar subida directa a Cloudinary"""
    print("\n📤 PROBANDO SUBIDA DIRECTA A CLOUDINARY")
    print("=" * 50)
    
    buffer = create_test_image()
    if not buffer:
        return False
    
    try:
        # Subir imagen directamente
        result = cloudinary.uploader.upload(
            buffer,
            public_id='test_upload_direct',
            overwrite=True,
            invalidate=True
        )
        
        print("✅ Subida directa exitosa")
        print(f"  Public ID: {result['public_id']}")
        print(f"  URL: {result['secure_url']}")
        print(f"  Tamaño: {result['bytes']} bytes")
        print(f"  Formato: {result['format']}")
        
        # Verificar que la imagen es accesible
        response = requests.get(result['secure_url'])
        if response.status_code == 200:
            print("✅ Imagen accesible desde URL")
        else:
            print(f"⚠️ Imagen no accesible: {response.status_code}")
        
        return result['public_id']
        
    except Exception as e:
        print(f"❌ Error en subida directa: {e}")
        return None

def test_custom_storage():
    """Probar el storage personalizado"""
    print("\n🔧 PROBANDO STORAGE PERSONALIZADO")
    print("=" * 50)
    
    buffer = create_test_image()
    if not buffer:
        return False
    
    try:
        # Crear instancia del storage personalizado
        storage = CloudinaryStorage()
        
        # Crear un archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(buffer.getvalue())
            temp_file_path = temp_file.name
        
        # Abrir el archivo como File de Django
        from django.core.files import File
        with open(temp_file_path, 'rb') as f:
            django_file = File(f, name='test_storage.png')
            
            # Guardar usando el storage personalizado
            saved_name = storage._save('test_storage_custom', django_file)
            
            print("✅ Subida con storage personalizado exitosa")
            print(f"  Nombre guardado: {saved_name}")
            
            # Obtener URL
            url = storage.url(saved_name)
            print(f"  URL: {url}")
            
            # Verificar existencia
            exists = storage.exists(saved_name)
            print(f"  Existe: {exists}")
            
            # Obtener tamaño
            size = storage.size(saved_name)
            print(f"  Tamaño: {size} bytes")
        
        # Limpiar archivo temporal
        os.unlink(temp_file_path)
        
        return saved_name
        
    except Exception as e:
        print(f"❌ Error con storage personalizado: {e}")
        return None

def test_django_model_upload():
    """Probar subida a través de un modelo Django"""
    print("\n📝 PROBANDO SUBIDA A TRAVÉS DE MODELO DJANGO")
    print("=" * 50)
    
    try:
        from productos.models import Producto, ImagenProducto
        
        # Crear un producto de prueba
        producto = Producto.objects.create(
            nombre="Producto Test Cloudinary",
            descripcion_corta="Producto para probar Cloudinary",
            descripcion_larga="Producto creado para probar la funcionalidad de Cloudinary",
            precio=100.00,
            costo=50.00,  # Campo obligatorio
            stock=10,
            estado='publicado',
            sku='TEST-CLOUD-001'
        )
        
        print(f"✅ Producto creado: {producto.id}")
        
        # Crear imagen de prueba
        buffer = create_test_image()
        if not buffer:
            return False
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(buffer.getvalue())
            temp_file_path = temp_file.name
        
        # Crear imagen del producto
        with open(temp_file_path, 'rb') as f:
            from django.core.files import File
            django_file = File(f, name='test_model.png')
            
            # Primero crear un color para el producto
            from productos.models import ColorProducto
            color = ColorProducto.objects.create(
                producto=producto,
                nombre="Test Color",
                hex_code="#FF0000",
                stock=10,
                activo=True
            )
            
            # Luego crear la imagen asociada al color
            imagen = ImagenProducto.objects.create(
                color=color,
                imagen=django_file,
                orden=1
            )
        
        print("✅ Imagen subida a través del modelo")
        print(f"  ID de imagen: {imagen.id}")
        print(f"  Nombre del archivo: {imagen.imagen.name}")
        print(f"  URL: {imagen.imagen.url}")
        
        # Verificar que la imagen existe
        if hasattr(imagen.imagen, 'storage'):
            exists = imagen.imagen.storage.exists(imagen.imagen.name)
            print(f"  Existe en storage: {exists}")
        
        # Limpiar archivo temporal
        os.unlink(temp_file_path)
        
        return imagen.id
        
    except Exception as e:
        print(f"❌ Error con modelo Django: {e}")
        return None

def test_delete_from_cloudinary():
    """Probar eliminación de archivos de Cloudinary"""
    print("\n🗑️ PROBANDO ELIMINACIÓN DE ARCHIVOS")
    print("=" * 50)
    
    # Lista de archivos a eliminar (de pruebas anteriores)
    files_to_delete = [
        'test_upload_direct',
        'test_storage_custom',
        'test_model'
    ]
    
    for file_id in files_to_delete:
        try:
            result = cloudinary.uploader.destroy(file_id)
            if result.get('result') == 'ok':
                print(f"✅ Eliminado: {file_id}")
            else:
                print(f"⚠️ No se pudo eliminar: {file_id} - {result.get('result')}")
        except Exception as e:
            print(f"❌ Error eliminando {file_id}: {e}")

def test_api_endpoints():
    """Probar endpoints de la API que manejan imágenes"""
    print("\n🌐 PROBANDO ENDPOINTS DE LA API")
    print("=" * 50)
    
    try:
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Probar endpoint de productos
        response = client.get('/api/productos/')
        if response.status_code == 200:
            print("✅ Endpoint de productos accesible")
            data = response.json()
            print(f"  Productos encontrados: {len(data.get('results', []))}")
        else:
            print(f"⚠️ Endpoint de productos: {response.status_code}")
        
        # Probar endpoint de categorías
        response = client.get('/api/categorias/')
        if response.status_code == 200:
            print("✅ Endpoint de categorías accesible")
        else:
            print(f"⚠️ Endpoint de categorías: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error probando endpoints: {e}")

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DE CLOUDINARY")
    print("=" * 60)
    
    # Ejecutar todas las pruebas
    tests = [
        ("Configuración", test_cloudinary_config),
        ("Conexión", test_cloudinary_connection),
        ("Subida directa", test_upload_to_cloudinary),
        ("Storage personalizado", test_custom_storage),
        ("Modelo Django", test_django_model_upload),
        ("Endpoints API", test_api_endpoints),
        ("Eliminación", test_delete_from_cloudinary),
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
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO FINAL: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! Cloudinary está funcionando correctamente.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración de Cloudinary.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 