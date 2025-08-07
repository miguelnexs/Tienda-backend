#!/usr/bin/env python3
"""
Script para probar la subida desde el frontend en producción
"""
import os
import sys
import django
from pathlib import Path
import tempfile
import requests
from PIL import Image
import io
import json

# Configurar Django con render_settings
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

def test_api_endpoints():
    """Probar endpoints de la API"""
    print("🌐 PROBANDO ENDPOINTS DE LA API")
    print("=" * 50)
    
    try:
        from django.test import Client
        
        client = Client()
        
        # Probar endpoint de productos
        response = client.get('/api/productos/')
        print(f"1. GET /api/productos/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Productos encontrados: {len(data.get('results', []))}")
            
            if data.get('results'):
                producto = data['results'][0]
                print(f"   Primer producto: {producto.get('nombre')}")
                return producto.get('id')
        else:
            print(f"   Error: {response.content.decode()[:200]}")
        
        return None
        
    except Exception as e:
        print(f"❌ Error probando endpoints: {e}")
        return None

def test_color_creation_with_image():
    """Probar creación de color con imagen"""
    print("\n📝 PROBANDO CREACIÓN DE COLOR CON IMAGEN")
    print("=" * 50)
    
    try:
        from django.test import Client
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        client = Client()
        
        # Obtener un producto para probar
        producto_id = test_api_endpoints()
        if not producto_id:
            print("❌ No se pudo obtener un producto para probar")
            return False
        
        print(f"2. Usando producto ID: {producto_id}")
        
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 200), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Crear archivo como lo haría el frontend
        image_file = SimpleUploadedFile(
            "test_frontend_upload.png",
            buffer.getvalue(),
            content_type="image/png"
        )
        
        # Datos del color
        data = {
            'nombre': 'Test Color Frontend',
            'hex_code': '#FF0000',
            'stock': '10',
            'activo': 'true'
        }
        
        # Crear archivo multipart
        files = {
            'imagenes': image_file
        }
        
        print("3. Enviando petición POST...")
        
        # Hacer petición POST
        response = client.post(
            f'/api/productos/productos/{producto_id}/colores/',
            data=data,
            files=files,
            content_type='multipart/form-data'
        )
        
        print(f"4. Status Code: {response.status_code}")
        print(f"5. Response: {response.content.decode()[:300]}...")
        
        if response.status_code in [200, 201]:
            print("✅ Color creado exitosamente")
            response_data = response.json()
            print(f"   ID del color: {response_data.get('id')}")
            return True
        else:
            print("❌ Error creando color")
            return False
            
    except Exception as e:
        print(f"❌ Error en la petición: {e}")
        return False

def test_direct_image_upload():
    """Probar subida directa de imagen"""
    print("\n📤 PROBANDO SUBIDA DIRECTA DE IMAGEN")
    print("=" * 50)
    
    try:
        from django.test import Client
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        client = Client()
        
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 200), color='blue')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Crear archivo
        image_file = SimpleUploadedFile(
            "test_direct_upload.png",
            buffer.getvalue(),
            content_type="image/png"
        )
        
        # Obtener un color para probar
        from productos.models import ColorProducto
        color = ColorProducto.objects.first()
        
        if not color:
            print("❌ No hay colores para probar")
            return False
        
        print(f"1. Usando color: {color.nombre}")
        
        # Datos de la imagen
        data = {
            'orden': '1',
            'es_principal': 'true'
        }
        
        files = {
            'imagen': image_file
        }
        
        print("2. Enviando petición POST...")
        
        # Hacer petición POST
        response = client.post(
            f'/api/productos/colores/{color.id}/imagenes/',
            data=data,
            files=files,
            content_type='multipart/form-data'
        )
        
        print(f"3. Status Code: {response.status_code}")
        print(f"4. Response: {response.content.decode()[:200]}...")
        
        if response.status_code in [200, 201]:
            print("✅ Imagen subida exitosamente")
            return True
        else:
            print("❌ Error subiendo imagen")
            return False
            
    except Exception as e:
        print(f"❌ Error en subida directa: {e}")
        return False

def test_storage_configuration():
    """Probar configuración del storage"""
    print("\n🔧 PROBANDO CONFIGURACIÓN DEL STORAGE")
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
        test_content = b"Test content for frontend upload"
        test_file = ContentFile(test_content)
        
        # Guardar archivo
        saved_name = default_storage.save("test_frontend_storage.txt", test_file)
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

def test_serializer_validation():
    """Probar validación de serializers"""
    print("\n📝 PROBANDO VALIDACIÓN DE SERIALIZERS")
    print("=" * 50)
    
    try:
        from productos.models import Producto, ColorProducto
        from productos.serializers.color_improved import ColorProductoCreateSerializer
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Obtener un producto
        producto = Producto.objects.first()
        if not producto:
            print("❌ No hay productos para probar")
            return False
        
        print(f"1. Producto: {producto.nombre}")
        
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
        
        # Datos de prueba
        test_data = {
            'nombre': 'Test Color Serializer',
            'hex_code': '#00FF00',
            'stock': 5,
            'activo': True,
            'imagenes': [
                {
                    'imagen': image_file,
                    'orden': 1,
                    'es_principal': True
                }
            ]
        }
        
        # Crear serializer
        serializer = ColorProductoCreateSerializer(data=test_data)
        
        if serializer.is_valid():
            print("2. ✅ Serializer válido")
            print(f"   Datos validados: {list(serializer.validated_data.keys())}")
            
            # Intentar guardar
            try:
                color = serializer.save(producto=producto)
                print(f"3. ✅ Color creado: {color.id}")
                print(f"   Nombre: {color.nombre}")
                print(f"   Stock: {color.stock}")
                
                # Verificar imágenes
                imagenes = color.imagenes.all()
                print(f"4. ✅ Imágenes creadas: {imagenes.count()}")
                
                for imagen in imagenes:
                    print(f"   - Imagen: {imagen.imagen.name}")
                    print(f"     URL: {imagen.imagen.url}")
                
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
    print("🚀 PRUEBA DE SUBIDA DESDE FRONTEND EN PRODUCCIÓN")
    print("=" * 60)
    
    tests = [
        ("API Endpoints", test_api_endpoints),
        ("Storage Config", test_storage_configuration),
        ("Color Creation", test_color_creation_with_image),
        ("Direct Upload", test_direct_image_upload),
        ("Serializer Validation", test_serializer_validation),
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
    print("\n📊 RESUMEN DE PRUEBAS")
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
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! La subida desde el frontend funciona.")
    elif passed >= 3:
        print("✅ La mayoría de las pruebas pasaron. Revisa los logs específicos.")
    else:
        print("⚠️ Varias pruebas fallaron. Hay problemas de configuración.")
    
    return passed >= 3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 