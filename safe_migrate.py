#!/usr/bin/env python
"""
Script para ejecutar migraciones de manera segura en Render
"""
import os
import sys
import django
from django.core.management import call_command
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

def safe_migrate():
    """Ejecutar migraciones de manera segura"""
    try:
        print("🗄️  Iniciando migraciones seguras...")
        
        # Verificar conexión a la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexión a BD establecida")
        
        # Ejecutar migraciones con manejo de errores
        print("📋 Ejecutando migraciones...")
        call_command('migrate', verbosity=2, interactive=False)
        
        print("✅ Migraciones completadas exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante las migraciones: {e}")
        
        # Intentar migración específica para categorias
        try:
            print("🔄 Intentando migración específica para categorias...")
            call_command('migrate', 'categorias', verbosity=2, interactive=False)
            print("✅ Migración de categorias completada")
            
            # Continuar con el resto de las apps
            call_command('migrate', verbosity=2, interactive=False)
            print("✅ Todas las migraciones completadas")
            return True
            
        except Exception as e2:
            print(f"❌ Error en migración específica: {e2}")
            return False

def create_superuser():
    """Crear superusuario si no existe"""
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            print("👤 Creando superusuario...")
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("✅ Superusuario creado: admin/admin123")
        else:
            print("✅ Superusuario ya existe")
        return True
    except Exception as e:
        print(f"❌ Error creando superusuario: {e}")
        return False

def collect_static():
    """Recolectar archivos estáticos"""
    try:
        print("📁 Recolectando archivos estáticos...")
        call_command('collectstatic', '--noinput', verbosity=2)
        print("✅ Archivos estáticos recolectados")
        return True
    except Exception as e:
        print(f"❌ Error recolectando archivos estáticos: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando despliegue seguro...")
    print("=" * 50)
    
    # Ejecutar migraciones
    if not safe_migrate():
        print("❌ Fallo en migraciones")
        return 1
    
    # Crear superusuario
    if not create_superuser():
        print("❌ Fallo creando superusuario")
        return 1
    
    # Recolectar archivos estáticos
    if not collect_static():
        print("❌ Fallo recolectando archivos estáticos")
        return 1
    
    print("🎉 ¡Despliegue completado exitosamente!")
    return 0

if __name__ == '__main__':
    sys.exit(main()) 