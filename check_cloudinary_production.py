#!/usr/bin/env python3
"""
Script final para verificar Cloudinary en producción
Ejecutar con: python check_cloudinary_production.py
"""
import os
import sys
import django
from pathlib import Path
import time

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

print("🚀 VERIFICACIÓN DE CLOUDINARY EN PRODUCCIÓN")
print("=" * 60)
print(f"📁 Directorio actual: {os.getcwd()}")
print(f"🐍 Python version: {sys.version}")
print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# Intentar cargar configuración de producción
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

def check_environment():
    """Verificar variables de entorno"""
    print("\n🔧 VERIFICANDO VARIABLES DE ENTORNO")
    print("-" * 40)
    
    required_vars = {
        'CLOUDINARY_CLOUD_NAME': 'do1ntnlop',
        'CLOUDINARY_API_KEY': '117225377115856',
        'CLOUDINARY_API_SECRET': 'e0YSrk3sT_70-ijM6mwdFBIWP9w',
        'DATABASE_URL': 'postgresql://tienda_user:PWKuO99372EAcsyx5KpHlV9VBIQJkvle@dpg-d278j5u3jp1c73en5gbg-a.ohio-postgres.render.com/tienda_production',
        'RENDER': 'true',
        'DEBUG': 'False',
        'SECRET_KEY': 'r@4-b1_76%pp5%body-8!!cnbkh+sz+5m!ry2&7cpst7o+1p_d'
    }
    
    all_present = True
    for var, expected_value in required_vars.items():
        actual_value = os.environ.get(var)
        if actual_value:
            if 'SECRET' in var or 'KEY' in var:
                display_actual = f"{actual_value[:10]}..."
                display_expected = f"{expected_value[:10]}..."
            else:
                display_actual = actual_value
                display_expected = expected_value
            
            if actual_value == expected_value:
                print(f"✅ {var}: {display_actual}")
            else:
                print(f"⚠️ {var}: {display_actual} (esperado: {display_expected})")
                all_present = False
        else:
            print(f"❌ {var}: NO ENCONTRADA")
            all_present = False
    
    return all_present

def check_cloudinary_config():
    """Verificar configuración de Cloudinary"""
    print("\n☁️ VERIFICANDO CONFIGURACIÓN DE CLOUDINARY")
    print("-" * 40)
    
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
        
        print(f"✅ Cloudinary configurado:")
        print(f"  Cloud Name: {cloud_name}")
        print(f"  API Key: {api_key[:10]}...")
        print(f"  API Secret: {api_secret[:10]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error configurando Cloudinary: {e}")
        return False

def test_cloudinary_connection():
    """Probar conexión a Cloudinary"""
    print("\n🌐 PROBANDO CONEXIÓN A CLOUDINARY")
    print("-" * 40)
    
    try:
        # Probar ping
        result = cloudinary.api.ping()
        print(f"✅ Conexión exitosa: {result.get('status', 'OK')}")
        
        # Obtener información de la cuenta
        account_info = cloudinary.api.account()
        print(f"✅ Información de cuenta:")
        print(f"  Cloud Name: {account_info.get('cloud_name')}")
        print(f"  Plan: {account_info.get('plan')}")
        print(f"  Credits usados: {account_info.get('credits', {}).get('used', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_upload_functionality():
    """Probar funcionalidad de subida"""
    print("\n📤 PROBANDO SUBIDA DE ARCHIVOS")
    print("-" * 40)
    
    try:
        from PIL import Image
        import io
        
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 200), color='blue')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.text((80, 80), "PRODUCTION", fill='white')
        draw.text((60, 120), "CLOUDINARY TEST", fill='white')
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Subir imagen
        result = cloudinary.uploader.upload(
            buffer,
            public_id='production_test_final',
            overwrite=True,
            invalidate=True
        )
        
        print(f"✅ Subida exitosa:")
        print(f"  Public ID: {result['public_id']}")
        print(f"  URL: {result['secure_url']}")
        print(f"  Tamaño: {result['bytes']} bytes")
        print(f"  Formato: {result['format']}")
        
        # Verificar acceso
        import requests
        response = requests.get(result['secure_url'], timeout=10)
        if response.status_code == 200:
            print("✅ Imagen accesible desde URL")
        else:
            print(f"⚠️ Error accediendo a imagen: {response.status_code}")
        
        # Limpiar archivo de prueba
        delete_result = cloudinary.uploader.destroy('production_test_final')
        if delete_result.get('result') == 'ok':
            print("✅ Archivo de prueba eliminado")
        else:
            print(f"⚠️ No se pudo eliminar archivo: {delete_result.get('result')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en subida: {e}")
        return False

def check_django_storage():
    """Verificar storage de Django"""
    print("\n🔧 VERIFICANDO STORAGE DE DJANGO")
    print("-" * 40)
    
    try:
        from django.core.files.storage import default_storage
        
        print(f"Storage actual: {type(default_storage).__name__}")
        print(f"Storage configurado: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
        print(f"DEBUG: {getattr(settings, 'DEBUG', 'No configurado')}")
        print(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'No configurado')}")
        
        # Verificar si es CloudinaryStorage
        if 'CloudinaryStorage' in str(type(default_storage)):
            print("✅ Usando CloudinaryStorage")
        else:
            print("⚠️ No usando CloudinaryStorage")
        
        # Verificar si estamos en producción
        if os.environ.get('RENDER'):
            print("✅ Ejecutando en Render (producción)")
        else:
            print("⚠️ No ejecutando en Render")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando storage: {e}")
        return False

def test_api_endpoints():
    """Probar endpoints de la API"""
    print("\n🌐 PROBANDO ENDPOINTS DE LA API")
    print("-" * 40)
    
    try:
        from django.test import Client
        
        client = Client()
        
        endpoints = [
            ('/api/productos/', 'Productos'),
            ('/api/categorias/', 'Categorías'),
            ('/api/ventas/', 'Ventas'),
            ('/api/pedidos/', 'Pedidos'),
        ]
        
        all_ok = True
        for url, name in endpoints:
            try:
                response = client.get(url)
                if response.status_code == 200:
                    print(f"✅ {name}: OK ({response.status_code})")
                else:
                    print(f"⚠️ {name}: {response.status_code}")
                    all_ok = False
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Error probando endpoints: {e}")
        return False

def test_database_connection():
    """Probar conexión a la base de datos"""
    print("\n🗄️ PROBANDO CONEXIÓN A BASE DE DATOS")
    print("-" * 40)
    
    try:
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Conexión exitosa a PostgreSQL")
            print(f"Versión: {version[0]}")
        
        # Probar consulta simple
        from productos.models import Producto
        count = Producto.objects.count()
        print(f"Productos en BD: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión a BD: {e}")
        return False

def main():
    """Función principal"""
    print("\n🎯 INICIANDO VERIFICACIONES")
    print("=" * 60)
    
    # Ejecutar todas las verificaciones
    checks = [
        ("Variables de Entorno", check_environment),
        ("Configuración Cloudinary", check_cloudinary_config),
        ("Conexión Cloudinary", test_cloudinary_connection),
        ("Subida de Archivos", test_upload_functionality),
        ("Storage Django", check_django_storage),
        ("Endpoints API", test_api_endpoints),
        ("Base de Datos", test_database_connection),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results[check_name] = result
        except Exception as e:
            print(f"❌ Error en {check_name}: {e}")
            results[check_name] = False
    
    # Resumen final
    print("\n📊 RESUMEN FINAL")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{check_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ Cloudinary está funcionando correctamente en producción.")
        print("✅ La aplicación está lista para usar en Render.")
    else:
        print("⚠️ Algunas verificaciones fallaron.")
        print("🔧 Revisa la configuración antes de desplegar.")
    
    print(f"\n⏰ Verificación completada: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 