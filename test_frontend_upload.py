#!/usr/bin/env python3
"""
Script para probar la subida de imágenes desde el frontend
"""
import os
import sys
import django
from pathlib import Path
import tempfile
import requests
import json
from PIL import Image
import io

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

# Importar después de configurar Django
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

def create_test_image_file():
    """Crear un archivo de imagen para pruebas"""
    # Crear imagen de prueba
    img = Image.new('RGB', (300, 200), color='blue')
    
    # Agregar texto
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.text((100, 80), "FRONTEND", fill='white')
    draw.text((80, 120), "UPLOAD TEST", fill='white')
    
    # Guardar en buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer.getvalue()

def test_product_creation_with_image():
    """Probar creación de producto con imagen"""
    print("📝 PROBANDO CREACIÓN DE PRODUCTO CON IMAGEN")
    print("=" * 50)
    
    client = Client()
    
    # Crear imagen de prueba
    image_data = create_test_image_file()
    image_file = SimpleUploadedFile(
        "test_product.png",
        image_data,
        content_type="image/png"
    )
    
    # Datos del producto
    product_data = {
        'nombre': 'Producto Test Frontend',
        'descripcion': 'Producto creado desde frontend test',
        'precio': '150.00',
        'stock': '20',
        'activo': 'true',
        'categoria': '1',  # Asumiendo que existe una categoría con ID 1
    }
    
    # Crear archivo multipart
    files = {
        'imagenes': image_file
    }
    
    try:
        # Hacer petición POST
        response = client.post(
            '/api/productos/',
            data=product_data,
            files=files,
            content_type='multipart/form-data'
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.content.decode()}")
        
        if response.status_code in [200, 201]:
            print("✅ Producto creado exitosamente")
            data = response.json()
            print(f"  ID del producto: {data.get('id')}")
            return data.get('id')
        else:
            print("❌ Error creando producto")
            return None
            
    except Exception as e:
        print(f"❌ Error en la petición: {e}")
        return None

def test_image_upload_endpoint():
    """Probar endpoint específico de subida de imágenes"""
    print("\n📤 PROBANDO ENDPOINT DE SUBIDA DE IMÁGENES")
    print("=" * 50)
    
    client = Client()
    
    # Crear imagen de prueba
    image_data = create_test_image_file()
    image_file = SimpleUploadedFile(
        "test_upload.png",
        image_data,
        content_type="image/png"
    )
    
    try:
        # Intentar subir imagen directamente
        files = {
            'imagen': image_file
        }
        
        response = client.post(
            '/api/productos/upload-image/',
            files=files,
            content_type='multipart/form-data'
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.content.decode()}")
        
        if response.status_code in [200, 201]:
            print("✅ Imagen subida exitosamente")
            return True
        else:
            print("❌ Error subiendo imagen")
            return False
            
    except Exception as e:
        print(f"❌ Error en la petición: {e}")
        return False

def test_api_with_real_http():
    """Probar la API con peticiones HTTP reales"""
    print("\n🌐 PROBANDO API CON PETICIONES HTTP REALES")
    print("=" * 50)
    
    # URL base (ajustar según tu configuración)
    base_url = "http://localhost:8000"
    
    # Crear imagen de prueba
    image_data = create_test_image_file()
    
    try:
        # Probar endpoint de productos
        response = requests.get(f"{base_url}/api/productos/")
        print(f"GET /api/productos/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Productos encontrados: {len(data.get('results', []))}")
        
        # Probar endpoint de categorías
        response = requests.get(f"{base_url}/api/categorias/")
        print(f"GET /api/categorias/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Categorías encontradas: {len(data.get('results', []))}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor. Asegúrate de que esté ejecutándose.")
        return False
    except Exception as e:
        print(f"❌ Error en peticiones HTTP: {e}")
        return False

def test_cloudinary_urls():
    """Probar URLs de Cloudinary"""
    print("\n🔗 PROBANDO URLs DE CLOUDINARY")
    print("=" * 50)
    
    try:
        from productos.models import Producto, ImagenProducto
        
        # Obtener algunos productos con imágenes
        productos = Producto.objects.filter(imagenes__isnull=False).distinct()[:5]
        
        if productos:
            print(f"Encontrados {len(productos)} productos con imágenes:")
            
            for producto in productos:
                print(f"\n📦 Producto: {producto.nombre}")
                
                # Obtener imágenes del producto
                imagenes = producto.imagenes.all()
                
                for imagen in imagenes:
                    print(f"  🖼️ Imagen: {imagen.imagen.name}")
                    print(f"     URL: {imagen.imagen.url}")
                    
                    # Verificar si la URL es accesible
                    try:
                        response = requests.get(imagen.imagen.url, timeout=10)
                        if response.status_code == 200:
                            print(f"     ✅ Accesible ({response.headers.get('content-length', 'N/A')} bytes)")
                        else:
                            print(f"     ❌ No accesible (Status: {response.status_code})")
                    except Exception as e:
                        print(f"     ⚠️ Error verificando URL: {e}")
        else:
            print("No se encontraron productos con imágenes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando URLs: {e}")
        return False

def test_storage_configuration():
    """Probar la configuración del storage"""
    print("\n⚙️ PROBANDO CONFIGURACIÓN DEL STORAGE")
    print("=" * 50)
    
    try:
        from django.conf import settings
        from django.core.files.storage import default_storage
        
        print(f"Storage configurado: {type(default_storage).__name__}")
        print(f"Clase del storage: {settings.DEFAULT_FILE_STORAGE}")
        
        # Probar operaciones básicas del storage
        test_file = SimpleUploadedFile(
            "test_storage.txt",
            b"Test content",
            content_type="text/plain"
        )
        
        # Guardar archivo
        saved_name = default_storage.save("test_storage.txt", test_file)
        print(f"Archivo guardado como: {saved_name}")
        
        # Verificar existencia
        exists = default_storage.exists(saved_name)
        print(f"Archivo existe: {exists}")
        
        # Obtener URL
        url = default_storage.url(saved_name)
        print(f"URL del archivo: {url}")
        
        # Eliminar archivo
        default_storage.delete(saved_name)
        print("Archivo eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando storage: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DE FRONTEND UPLOAD")
    print("=" * 60)
    
    tests = [
        ("Configuración Storage", test_storage_configuration),
        ("Creación Producto", test_product_creation_with_image),
        ("Subida Imagen", test_image_upload_endpoint),
        ("URLs Cloudinary", test_cloudinary_urls),
        ("HTTP Real", test_api_with_real_http),
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
    print("\n📊 RESUMEN DE PRUEBAS FRONTEND")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! El frontend puede subir imágenes correctamente.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 