#!/usr/bin/env python
"""
Script para probar la configuración de base de datos corregida
"""
import os
import sys
import django
import requests
import json
import time
from pathlib import Path

# Simular entorno de Render
os.environ['RENDER'] = 'true'
os.environ['DJANGO_SETTINGS_MODULE'] = 'Backend.render_settings'

# Configurar DATABASE_URL para pruebas locales
if not os.environ.get('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'postgresql://tienda_user:PWKuO99372EAcsyx5KpHlV9VBIQJkvle@dpg-d278j5u3jp1c73en5gbg-a.ohio-postgres.render.com/tienda_production'

# Configurar Django
django.setup()

def test_database_connection():
    """Probar la conexión a la base de datos"""
    
    print("🗄️ PROBANDO CONEXIÓN A BASE DE DATOS")
    print("="*50)
    
    try:
        from django.conf import settings
        from django.db import connection
        
        print("📋 Configuración de base de datos:")
        print(f"  DATABASE_URL: {os.environ.get('DATABASE_URL', 'No definida')[:50]}...")
        print(f"  ENGINE: {settings.DATABASES['default']['ENGINE']}")
        print(f"  NAME: {settings.DATABASES['default']['NAME']}")
        print(f"  HOST: {settings.DATABASES['default']['HOST']}")
        print(f"  PORT: {settings.DATABASES['default']['PORT']}")
        
        # Probar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Conexión exitosa a PostgreSQL: {version[0]}")
            return True
            
    except Exception as e:
        print(f"❌ Error de conexión a base de datos: {e}")
        return False

def test_api_with_database():
    """Probar API con base de datos corregida"""
    
    print("\n" + "="*50)
    print("🌐 PROBANDO API CON BASE DE DATOS CORREGIDA")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # Probar obtener categorías
        url = f"{RENDER_API_URL}/categorias/"
        
        print(f"🚀 Obteniendo categorías de: {url}")
        
        response = requests.get(url, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                categorias = response.json()
                print(f"✅ Se obtuvieron {len(categorias)} categorías")
                print("✅ API funcionando correctamente con base de datos")
                return True
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                return False
        else:
            print(f"❌ Error en API: {response.status_code}")
            print(f"📊 Response Text: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: La petición tardó demasiado")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión durante la petición")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_cloudinary_config():
    """Probar configuración de Cloudinary"""
    
    print("\n" + "="*50)
    print("☁️ PROBANDO CONFIGURACIÓN DE CLOUDINARY")
    print("="*50)
    
    try:
        from django.conf import settings
        
        print("📋 Configuración de Cloudinary:")
        print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        print(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
        
        if hasattr(settings, 'CLOUDINARY'):
            print("\n☁️ Configuración de Cloudinary:")
            print(f"  Cloud Name: {settings.CLOUDINARY.get('cloud_name', 'No definido')}")
            print(f"  API Key: {settings.CLOUDINARY.get('api_key', 'No definido')[:10]}..." if settings.CLOUDINARY.get('api_key') else "  API Key: No definido")
            print(f"  API Secret: {settings.CLOUDINARY.get('api_secret', 'No definido')[:10]}..." if settings.CLOUDINARY.get('api_secret') else "  API Secret: No definido")
        else:
            print("\n❌ No se encontró configuración de Cloudinary")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando Cloudinary: {e}")
        return False

def main():
    """Función principal"""
    print("🗄️ PRUEBA DE CONFIGURACIÓN DE BASE DE DATOS")
    print("="*50)
    
    # Probar conexión a base de datos
    db_ok = test_database_connection()
    
    # Probar configuración de Cloudinary
    cloudinary_ok = test_cloudinary_config()
    
    # Probar API
    api_ok = test_api_with_database()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    print(f"✅ Conexión a base de datos: {'EXITOSA' if db_ok else 'FALLIDA'}")
    print(f"✅ Configuración de Cloudinary: {'EXITOSA' if cloudinary_ok else 'FALLIDA'}")
    print(f"✅ API con base de datos: {'EXITOSA' if api_ok else 'FALLIDA'}")
    
    # Conclusión
    print("\n" + "="*50)
    print("🎯 CONCLUSIÓN")
    print("="*50)
    
    if db_ok and cloudinary_ok and api_ok:
        print("🎉 ¡La configuración está funcionando perfectamente!")
        print("✅ La base de datos está conectada")
        print("✅ Cloudinary está configurado")
        print("✅ La API funciona correctamente")
    elif db_ok and cloudinary_ok:
        print("✅ La base de datos y Cloudinary están bien")
        print("⚠️ Pero hay problemas con la API")
    elif db_ok:
        print("✅ La base de datos está conectada")
        print("❌ Pero hay problemas con Cloudinary")
    else:
        print("❌ Hay problemas con la base de datos")
        print("🔧 Revisar configuración de DATABASE_URL")
    
    print("\n💡 RECOMENDACIONES:")
    print("1. Verificar que DATABASE_URL esté configurada correctamente")
    print("2. Asegurar que las credenciales de Cloudinary sean válidas")
    print("3. Verificar que el servicio esté usando render_settings.py")

if __name__ == '__main__':
    main() 