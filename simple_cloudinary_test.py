#!/usr/bin/env python3
"""
Script simple para probar Cloudinary
"""
import os
import sys
import django
from pathlib import Path
import cloudinary
import cloudinary.uploader
import requests
from PIL import Image
import io

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

def test_basic_cloudinary():
    """Prueba básica de Cloudinary"""
    print("🚀 PRUEBA BÁSICA DE CLOUDINARY")
    print("=" * 50)
    
    # 1. Verificar configuración
    print("1. Verificando configuración...")
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'do1ntnlop')
    api_key = os.environ.get('CLOUDINARY_API_KEY', '117225377115856')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET', 'e0YSrk3sT_70-ijM6mwdFBIWP9w')
    
    print(f"   Cloud Name: {cloud_name}")
    print(f"   API Key: {api_key[:10]}...")
    print(f"   API Secret: {api_secret[:10]}...")
    
    # 2. Configurar Cloudinary
    print("\n2. Configurando Cloudinary...")
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )
    print("   ✅ Configuración completada")
    
    # 3. Probar conexión
    print("\n3. Probando conexión...")
    try:
        result = cloudinary.api.ping()
        print(f"   ✅ Conexión exitosa: {result.get('status', 'OK')}")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False
    
    # 4. Crear imagen de prueba
    print("\n4. Creando imagen de prueba...")
    img = Image.new('RGB', (300, 200), color='green')
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.text((100, 80), "CLOUDINARY", fill='white')
    draw.text((80, 120), "TEST OK", fill='white')
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    print("   ✅ Imagen creada")
    
    # 5. Subir imagen
    print("\n5. Subiendo imagen...")
    try:
        result = cloudinary.uploader.upload(
            buffer,
            public_id='test_simple_upload',
            overwrite=True,
            invalidate=True
        )
        print(f"   ✅ Subida exitosa")
        print(f"   Public ID: {result['public_id']}")
        print(f"   URL: {result['secure_url']}")
        print(f"   Tamaño: {result['bytes']} bytes")
        
        # 6. Verificar que la imagen es accesible
        print("\n6. Verificando accesibilidad...")
        response = requests.get(result['secure_url'], timeout=10)
        if response.status_code == 200:
            print("   ✅ Imagen accesible desde URL")
        else:
            print(f"   ⚠️ Imagen no accesible: {response.status_code}")
        
        # 7. Eliminar imagen de prueba
        print("\n7. Eliminando imagen de prueba...")
        delete_result = cloudinary.uploader.destroy('test_simple_upload')
        if delete_result.get('result') == 'ok':
            print("   ✅ Imagen eliminada")
        else:
            print(f"   ⚠️ No se pudo eliminar: {delete_result.get('result')}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en subida: {e}")
        return False

def test_django_storage():
    """Probar el storage de Django"""
    print("\n🔧 PROBANDO STORAGE DE DJANGO")
    print("=" * 50)
    
    try:
        from django.conf import settings
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        print(f"1. Storage configurado: {type(default_storage).__name__}")
        print(f"2. Clase del storage: {settings.DEFAULT_FILE_STORAGE}")
        
        # Crear archivo de prueba
        test_content = b"Test content for Django storage"
        test_file = ContentFile(test_content)
        
        # Guardar archivo
        saved_name = default_storage.save("test_django_storage.txt", test_file)
        print(f"3. Archivo guardado como: {saved_name}")
        
        # Verificar existencia
        exists = default_storage.exists(saved_name)
        print(f"4. Archivo existe: {exists}")
        
        # Obtener URL
        url = default_storage.url(saved_name)
        print(f"5. URL del archivo: {url}")
        
        # Eliminar archivo
        default_storage.delete(saved_name)
        print("6. Archivo eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando storage: {e}")
        return False

def test_cloudinary_urls():
    """Probar URLs de Cloudinary existentes"""
    print("\n🔗 PROBANDO URLs DE CLOUDINARY")
    print("=" * 50)
    
    try:
        from productos.models import Producto, ColorProducto, ImagenProducto
        
        # Buscar productos con colores e imágenes
        productos = Producto.objects.filter(colores__imagenes__isnull=False).distinct()[:3]
        
        if productos:
            print(f"Encontrados {len(productos)} productos con imágenes:")
            
            for producto in productos:
                print(f"\n📦 Producto: {producto.nombre}")
                
                # Obtener colores con imágenes
                colores = producto.colores.filter(imagenes__isnull=False)
                
                for color in colores:
                    print(f"  🎨 Color: {color.nombre}")
                    
                    # Obtener imágenes del color
                    imagenes = color.imagenes.all()
                    
                    for imagen in imagenes:
                        print(f"    🖼️ Imagen: {imagen.imagen.name}")
                        print(f"       URL: {imagen.imagen.url}")
                        
                        # Verificar si la URL es accesible
                        try:
                            response = requests.get(imagen.imagen.url, timeout=10)
                            if response.status_code == 200:
                                print(f"       ✅ Accesible ({response.headers.get('content-length', 'N/A')} bytes)")
                            else:
                                print(f"       ❌ No accesible (Status: {response.status_code})")
                        except Exception as e:
                            print(f"       ⚠️ Error verificando URL: {e}")
        else:
            print("No se encontraron productos con imágenes")
            print("💡 Sugerencia: Crea algunos productos con imágenes para probar")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando URLs: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS SIMPLES DE CLOUDINARY")
    print("=" * 60)
    
    tests = [
        ("Cloudinary Básico", test_basic_cloudinary),
        ("Django Storage", test_django_storage),
        ("URLs Cloudinary", test_cloudinary_urls),
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
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! Cloudinary está funcionando correctamente.")
    elif passed >= 2:
        print("✅ La mayoría de las pruebas pasaron. Cloudinary está funcionando bien.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración de Cloudinary.")
    
    return passed >= 2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 