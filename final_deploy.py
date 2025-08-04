#!/usr/bin/env python
"""
Script final de despliegue para Render
"""
import os
import sys
import django
from django.core.management import call_command
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

def deploy():
    """Despliegue completo"""
    try:
        print("🚀 Iniciando despliegue final...")
        
        # 1. Verificar conexión a BD
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexión a BD establecida")
        
        # 2. Ejecutar migraciones básicas primero
        basic_apps = ['contenttypes', 'auth', 'admin', 'sessions']
        for app in basic_apps:
            try:
                call_command('migrate', app, verbosity=1, interactive=False)
                print(f"✅ {app} migrado")
            except Exception as e:
                print(f"⚠️  Error en {app}: {e}")
        
        # 3. Ejecutar migraciones de apps personalizadas
        custom_apps = ['categorias', 'productos', 'ventas', 'pedidos']
        for app in custom_apps:
            try:
                call_command('migrate', app, verbosity=1, interactive=False)
                print(f"✅ {app} migrado")
            except Exception as e:
                print(f"⚠️  Error en {app}: {e}")
                # Intentar migración específica
                try:
                    call_command('migrate', app, '0001', verbosity=1, interactive=False)
                    print(f"✅ {app} migrado a 0001")
                except Exception as e2:
                    print(f"❌ Error crítico en {app}: {e2}")
        
        # 4. Migración final
        call_command('migrate', verbosity=1, interactive=False)
        print("✅ Migración final completada")
        
        # 5. Crear superusuario
        try:
            from django.contrib.auth.models import User
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
                print("✅ Superusuario creado")
        except Exception as e:
            print(f"⚠️  Error creando superusuario: {e}")
        
        # 6. Recolectar archivos estáticos
        try:
            call_command('collectstatic', '--noinput', verbosity=1)
            print("✅ Archivos estáticos recolectados")
        except Exception as e:
            print(f"⚠️  Error recolectando estáticos: {e}")
        
        print("🎉 ¡Despliegue completado!")
        return True
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

def main():
    """Función principal"""
    if deploy():
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main()) 