#!/usr/bin/env python3
"""
Script de prueba para verificar Cloudinary en Render
Ejecutar con: python test_render_cloudinary.py
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Intentar cargar configuración de producción primero
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
    django.setup()
    print("✅ Configuración de producción cargada (render_settings.py)")
except Exception as e:
    print(f"⚠️ Error cargando configuración de producción: {e}")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
        django.setup()
        print("✅ Configuración de desarrollo cargada (settings.py)")
    except Exception as e2:
        print(f"❌ Error cargando configuración: {e2}")
        sys.exit(1)

import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings

def test_basic_config():
    """Prueba básica de configuración"""
    print("\n🔧 PRUEBA BÁSICA DE CONFIGURACIÓN")
    print("=" * 50)
    
    # Verificar variables de entorno
    env_vars = {
        'CLOUDINARY_CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'CLOUDINARY_API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'CLOUDINARY_API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
        'DATABASE_URL': os.environ.get('DATABASE_URL'),
        'RENDER': os.environ.get('RENDER'),
    }
    
    print("📋 Variables de Entorno:")
    for var, value in env_vars.items():
        if value:
            if 'SECRET' in var or 'KEY' in var:
                display_value = f"{value[:10]}..."
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: NO ENCONTRADA")
    
    # Verificar configuración de Django
    print(f"\n⚙️ Configuración Django:")
    print(f"  DEBUG: {getattr(settings, 'DEBUG', 'No configurado')}")
    print(f"  DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    print(f"  MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'No configurado')}")
    
    return all(env_vars.values())

def test_cloudinary_connection():
    """Probar conexión a Cloudinary"""
    print("\n🌐 PRUEBA DE CONEXIÓN A CLOUDINARY")
    print("=" * 50)
    
    try:
        # Configurar Cloudinary
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
        api_key = os.environ.get('CLOUDINARY_API_KEY')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET')
        
        if not all([cloud_name, api_key, api_secret]):
            print("❌ Faltan variables de entorno de Cloudinary")
            return False
        
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
        # Probar ping
        result = cloudinary.api.ping()
        print(f"✅ Conexión exitosa: {result.get('status', 'OK')}")
        
        # Obtener información de la cuenta
        account_info = cloudinary.api.account()
        print(f"✅ Información de cuenta:")
        print(f"  Cloud Name: {account_info.get('cloud_name')}")
        print(f"  Plan: {account_info.get('plan')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_upload_functionality():
    """Probar funcionalidad de subida"""
    print("\n📤 PRUEBA DE SUBIDA")
    print("=" * 50)
    
    try:
        from PIL import Image
        import io
        
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 150), color='purple')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.text((50, 60), "RENDER TEST", fill='white')
        draw.text((30, 90), "CLOUDINARY", fill='white')
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Subir imagen
        result = cloudinary.uploader.upload(
            buffer,
            public_id='render_test_upload',
            overwrite=True,
            invalidate=True
        )
        
        print(f"✅ Subida exitosa:")
        print(f"  Public ID: {result['public_id']}")
        print(f"  URL: {result['secure_url']}")
        print(f"  Tamaño: {result['bytes']} bytes")
        
        # Verificar acceso
        import requests
        response = requests.get(result['secure_url'], timeout=10)
        if response.status_code == 200:
            print("✅ Imagen accesible desde URL")
        else:
            print(f"⚠️ Error accediendo a imagen: {response.status_code}")
        
        # Limpiar archivo de prueba
        delete_result = cloudinary.uploader.destroy('render_test_upload')
        if delete_result.get('result') == 'ok':
            print("✅ Archivo de prueba eliminado")
        else:
            print(f"⚠️ No se pudo eliminar archivo: {delete_result.get('result')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en subida: {e}")
        return False

def test_django_storage():
    """Probar storage de Django"""
    print("\n🔧 PRUEBA DE STORAGE DJANGO")
    print("=" * 50)
    
    try:
        from django.core.files.storage import default_storage
        
        print(f"Storage actual: {type(default_storage).__name__}")
        print(f"Storage configurado: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
        
        # Verificar si es CloudinaryStorage
        if 'CloudinaryStorage' in str(type(default_storage)):
            print("✅ Usando CloudinaryStorage")
        else:
            print("⚠️ No usando CloudinaryStorage")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando storage: {e}")
        return False

def test_api_endpoints():
    """Probar endpoints de la API"""
    print("\n🌐 PRUEBA DE ENDPOINTS API")
    print("=" * 50)
    
    try:
        from django.test import Client
        
        client = Client()
        
        endpoints = [
            ('/api/productos/', 'Productos'),
            ('/api/categorias/', 'Categorías'),
        ]
        
        for url, name in endpoints:
            try:
                response = client.get(url)
                if response.status_code == 200:
                    print(f"✅ {name}: OK ({response.status_code})")
                else:
                    print(f"⚠️ {name}: {response.status_code}")
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando endpoints: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 PRUEBA DE CLOUDINARY EN RENDER")
    print("=" * 60)
    
    # Ejecutar pruebas
    tests = [
        ("Configuración Básica", test_basic_config),
        ("Conexión Cloudinary", test_cloudinary_connection),
        ("Subida de Archivos", test_upload_functionality),
        ("Storage Django", test_django_storage),
        ("Endpoints API", test_api_endpoints),
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
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! Cloudinary está funcionando correctamente en Render.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 