#!/usr/bin/env python
"""
Script para verificar que el proyecto esté listo para el despliegue
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')

def check_settings():
    """Verifica la configuración de Django"""
    print("🔍 Verificando configuración de Django...")
    
    try:
        django.setup()
        from django.conf import settings
        
        # Verificar configuración básica
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}")
        
        # Verificar configuración de Cloudinary
        if hasattr(settings, 'CLOUDINARY'):
            print(f"✅ CLOUDINARY configurado")
            print(f"   Cloud Name: {settings.CLOUDINARY.get('cloud_name')}")
        else:
            print("⚠️  CLOUDINARY no configurado")
            
        # Verificar storage
        if hasattr(settings, 'DEFAULT_FILE_STORAGE'):
            print(f"✅ DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        else:
            print("⚠️  DEFAULT_FILE_STORAGE no configurado")
            
        # Verificar middleware
        print(f"✅ MIDDLEWARE configurado ({len(settings.MIDDLEWARE)} elementos)")
        
        # Verificar apps instaladas
        print(f"✅ INSTALLED_APPS configurado ({len(settings.INSTALLED_APPS)} apps)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def check_database():
    """Verifica la configuración de la base de datos"""
    print("\n🗄️  Verificando configuración de base de datos...")
    
    try:
        from django.db import connection
        from django.core.management import execute_from_command_line
        
        # Verificar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Conexión a base de datos exitosa")
            
        # Verificar migraciones
        print("📋 Verificando migraciones...")
        execute_from_command_line(['manage.py', 'showmigrations'])
        
        return True
        
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
        return False

def check_static_files():
    """Verifica la configuración de archivos estáticos"""
    print("\n📁 Verificando archivos estáticos...")
    
    try:
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        # Verificar collectstatic
        print("📦 Ejecutando collectstatic...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        print("✅ Archivos estáticos configurados correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en archivos estáticos: {e}")
        return False

def check_cloudinary():
    """Verifica la configuración de Cloudinary"""
    print("\n☁️  Verificando configuración de Cloudinary...")
    
    try:
        import cloudinary
        
        # Verificar variables de entorno
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
        api_key = os.environ.get('CLOUDINARY_API_KEY')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET')
        
        print(f"📋 Variables de entorno:")
        print(f"   Cloud Name: {'✅ Configurado' if cloud_name else '❌ No configurado'}")
        print(f"   API Key: {'✅ Configurado' if api_key else '❌ No configurado'}")
        print(f"   API Secret: {'✅ Configurado' if api_secret else '❌ No configurado'}")
        
        if all([cloud_name, api_key, api_secret]):
            # Configurar Cloudinary
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )
            
            # Verificar configuración
            config = cloudinary.config()
            print(f"✅ Cloudinary configurado: {config.cloud_name}")
            return True
        else:
            print("❌ Variables de entorno de Cloudinary no configuradas")
            return False
            
    except Exception as e:
        print(f"❌ Error configurando Cloudinary: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Verificación de preparación para despliegue")
    print("=" * 50)
    
    # Verificar configuración
    settings_ok = check_settings()
    
    if settings_ok:
        # Verificar base de datos
        db_ok = check_database()
        
        # Verificar archivos estáticos
        static_ok = check_static_files()
        
        # Verificar Cloudinary
        cloudinary_ok = check_cloudinary()
        
        print("\n" + "=" * 50)
        print("📊 Resumen:")
        print(f"   Configuración Django: {'✅ OK' if settings_ok else '❌ Error'}")
        print(f"   Base de datos: {'✅ OK' if db_ok else '❌ Error'}")
        print(f"   Archivos estáticos: {'✅ OK' if static_ok else '❌ Error'}")
        print(f"   Cloudinary: {'✅ OK' if cloudinary_ok else '❌ Error'}")
        
        if settings_ok and db_ok and static_ok and cloudinary_ok:
            print("\n🎉 ¡Proyecto listo para despliegue!")
        else:
            print("\n⚠️  Hay problemas que necesitan corrección antes del despliegue")
    else:
        print("\n❌ No se puede verificar la configuración")

if __name__ == "__main__":
    main() 