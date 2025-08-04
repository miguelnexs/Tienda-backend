#!/usr/bin/env python
"""
Script para verificar que el proyecto esté listo para el despliegue
"""
import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def check_database():
    """Verificar que la base de datos esté accesible"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Base de datos accesible")
        return True
    except Exception as e:
        print(f"❌ Error de base de datos: {e}")
        return False

def check_migrations():
    """Verificar que no haya migraciones pendientes"""
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # Capturar la salida del comando showmigrations
        out = StringIO()
        call_command('showmigrations', stdout=out)
        output = out.getvalue()
        
        # Verificar si hay migraciones sin aplicar
        if '[ ]' in output:
            print("⚠️  Hay migraciones pendientes")
            return False
        else:
            print("✅ Todas las migraciones aplicadas")
            return True
    except Exception as e:
        print(f"❌ Error verificando migraciones: {e}")
        return False

def check_static_files():
    """Verificar que los archivos estáticos se puedan recolectar"""
    try:
        from django.core.management import call_command
        call_command('collectstatic', '--dry-run', '--noinput')
        print("✅ Archivos estáticos OK")
        return True
    except Exception as e:
        print(f"❌ Error con archivos estáticos: {e}")
        return False

def check_settings():
    """Verificar configuración básica"""
    try:
        # Verificar configuración de base de datos
        db_config = settings.DATABASES['default']
        print(f"✅ Configuración de BD: {db_config['ENGINE']}")
        
        # Verificar configuración de archivos media
        print(f"✅ MEDIA_URL: {settings.MEDIA_URL}")
        print(f"✅ MEDIA_ROOT: {settings.MEDIA_ROOT}")
        print(f"✅ DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        
        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🔍 Verificando proyecto para despliegue...")
    print("=" * 50)
    
    checks = [
        ("Configuración", check_settings),
        ("Base de datos", check_database),
        ("Migraciones", check_migrations),
        ("Archivos estáticos", check_static_files),
    ]
    
    all_passed = True
    
    for name, check_func in checks:
        print(f"\n📋 Verificando {name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ¡Proyecto listo para despliegue!")
        return 0
    else:
        print("❌ Hay problemas que deben resolverse antes del despliegue")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 