#!/usr/bin/env python
"""
Script simplificado para migraciones en Render
"""
import os
import sys
import django
from django.core.management import call_command
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

def simple_migrate():
    """Ejecutar migraciones de manera simple"""
    try:
        print("🗄️  Iniciando migraciones...")
        
        # Verificar conexión a la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexión a BD establecida")
        
        # Ejecutar migraciones una por una
        apps = ['contenttypes', 'auth', 'admin', 'sessions', 'categorias', 'productos', 'ventas', 'pedidos']
        
        for app in apps:
            try:
                print(f"📋 Migrando {app}...")
                call_command('migrate', app, verbosity=1, interactive=False)
                print(f"✅ {app} migrado")
            except Exception as e:
                print(f"⚠️  Error migrando {app}: {e}")
                # Continuar con la siguiente app
                continue
        
        # Ejecutar migraciones finales
        call_command('migrate', verbosity=1, interactive=False)
        print("✅ Todas las migraciones completadas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

def create_superuser():
    """Crear superusuario"""
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("✅ Superusuario creado")
        return True
    except Exception as e:
        print(f"❌ Error creando superusuario: {e}")
        return False

def collect_static():
    """Recolectar archivos estáticos"""
    try:
        call_command('collectstatic', '--noinput', verbosity=1)
        print("✅ Archivos estáticos recolectados")
        return True
    except Exception as e:
        print(f"❌ Error recolectando estáticos: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando despliegue...")
    
    if simple_migrate():
        create_superuser()
        collect_static()
        print("🎉 ¡Despliegue completado!")
        return 0
    else:
        print("❌ Fallo en el despliegue")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 