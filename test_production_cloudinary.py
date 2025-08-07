#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión a Cloudinary en producción
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

def print_header(title):
    """Imprimir un encabezado formateado"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_section(title):
    """Imprimir una sección formateada"""
    print(f"\n📋 {title}")
    print(f"{'-'*40}")

def test_environment_variables():
    """Verificar variables de entorno"""
    print_header("VERIFICACIÓN DE VARIABLES DE ENTORNO")
    
    required_vars = [
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY', 
        'CLOUDINARY_API_SECRET',
        'DATABASE_URL',
        'SECRET_KEY',
        'RENDER'
    ]
    
    print_section("Variables Requeridas")
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            if 'SECRET' in var or 'KEY' in var:
                display_value = f"{value[:10]}..." if len(value) > 10 else "***"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NO ENCONTRADA")
    
    print_section("Variables de Configuración")
    print(f"DEBUG: {os.environ.get('DEBUG', 'No definido')}")
    print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'No definido')}")
    print(f"TIME_ZONE: {os.environ.get('TIME_ZONE', 'No definido')}")

def test_cloudinary_config():
    """Probar configuración de Cloudinary"""
    print_header("CONFIGURACIÓN DE CLOUDINARY")
    
    try:
        # Obtener variables de entorno
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
        api_key = os.environ.get('CLOUDINARY_API_KEY')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET')
        
        if not all([cloud_name, api_key, api_secret]):
            print("❌ Faltan variables de entorno de Cloudinary")
            return False
        
        # Configurar Cloudinary
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
        print_section("Configuración Aplicada")
        config = cloudinary.config()
        print(f"Cloud Name: {config.cloud_name}")
        print(f"API Key: {config.api_key[:10]}...")
        print(f"API Secret: {config.api_secret[:10]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error configurando Cloudinary: {e}")
        return False

def test_cloudinary_connection():
    """Probar conexión a Cloudinary"""
    print_header("CONEXIÓN A CLOUDINARY")
    
    try:
        # Probar ping a Cloudinary
        result = cloudinary.api.ping()
        
        print_section("Test de Conexión")
        print(f"Status: {result.get('status', 'OK')}")
        print("✅ Conexión exitosa a Cloudinary")
        
        # Obtener información de la cuenta
        account_info = cloudinary.api.account()
        
        print_section("Información de la Cuenta")
        print(f"Cloud Name: {account_info.get('cloud_name')}")
        print(f"Plan: {account_info.get('plan')}")
        print(f"Credits: {account_info.get('credits', {}).get('used', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_upload_functionality():
    """Probar funcionalidad de subida"""
    print_header("PRUEBA DE SUBIDA")
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 200), color='blue')
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        draw.text((50, 80), "PRODUCTION", fill='white')
        draw.text((30, 120), "CLOUDINARY TEST", fill='white')
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        print_section("Subida de Imagen")
        
        # Subir imagen
        result = cloudinary.uploader.upload(
            buffer,
            public_id='production_test_image',
            overwrite=True,
            invalidate=True
        )
        
        print(f"✅ Subida exitosa")
        print(f"Public ID: {result['public_id']}")
        print(f"URL: {result['secure_url']}")
        print(f"Tamaño: {result['bytes']} bytes")
        print(f"Formato: {result['format']}")
        
        # Verificar acceso
        response = requests.get(result['secure_url'], timeout=10)
        if response.status_code == 200:
            print("✅ Imagen accesible desde URL")
        else:
            print(f"⚠️ Error accediendo a imagen: {response.status_code}")
        
        return result['public_id']
        
    except Exception as e:
        print(f"❌ Error en subida: {e}")
        return None

def test_django_storage():
    """Probar storage de Django"""
    print_header("STORAGE DE DJANGO")
    
    try:
        print_section("Configuración de Storage")
        print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
        print(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'No configurado')}")
        print(f"MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'No configurado')}")
        
        # Verificar si estamos en producción
        if 'RENDER' in os.environ:
            print("✅ Ejecutando en Render (producción)")
        else:
            print("⚠️ No ejecutando en Render")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando storage: {e}")
        return False

def test_api_endpoints():
    """Probar endpoints de la API"""
    print_header("ENDPOINTS DE LA API")
    
    try:
        from django.test import Client
        
        client = Client()
        
        endpoints = [
            ('/api/productos/', 'Productos'),
            ('/api/categorias/', 'Categorías'),
            ('/api/ventas/', 'Ventas'),
            ('/api/pedidos/', 'Pedidos'),
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

def test_database_connection():
    """Probar conexión a la base de datos"""
    print_header("CONEXIÓN A BASE DE DATOS")
    
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

def cleanup_test_files():
    """Limpiar archivos de prueba"""
    print_header("LIMPIEZA")
    
    try:
        # Eliminar archivo de prueba
        result = cloudinary.uploader.destroy('production_test_image')
        if result.get('result') == 'ok':
            print("✅ Archivo de prueba eliminado")
        else:
            print(f"⚠️ No se pudo eliminar archivo: {result.get('result')}")
        
    except Exception as e:
        print(f"❌ Error en limpieza: {e}")

def generate_report(results):
    """Generar reporte final"""
    print_header("REPORTE FINAL")
    
    print_section("Resumen de Pruebas")
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:25} {status}")
    
    print(f"\n🎯 RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! Cloudinary está funcionando correctamente en producción.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración.")
    
    return passed == total

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DE PRODUCCIÓN - CLOUDINARY")
    print("=" * 70)
    
    # Ejecutar todas las pruebas
    tests = [
        ("Variables de Entorno", test_environment_variables),
        ("Configuración Cloudinary", test_cloudinary_config),
        ("Conexión Cloudinary", test_cloudinary_connection),
        ("Subida de Archivos", test_upload_functionality),
        ("Storage Django", test_django_storage),
        ("Endpoints API", test_api_endpoints),
        ("Base de Datos", test_database_connection),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results[test_name] = False
    
    # Limpiar archivos de prueba
    cleanup_test_files()
    
    # Generar reporte
    success = generate_report(results)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 