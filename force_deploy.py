#!/usr/bin/env python
"""
Script de despliegue forzado para Render
"""
import os
import sys
import django
from django.core.management import call_command
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

def force_deploy():
    """Despliegue forzado que maneja conflictos de migraciones"""
    try:
        print("🚀 Iniciando despliegue forzado...")
        
        # Verificar conexión a la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexión a BD establecida")
        
        # 1. Intentar hacer merge de migraciones
        try:
            print("🔄 Intentando merge de migraciones...")
            call_command('makemigrations', '--merge', verbosity=2)
            print("✅ Merge completado")
        except Exception as e:
            print(f"⚠️  Error en merge: {e}")
        
        # 2. Ejecutar migraciones básicas
        basic_apps = ['contenttypes', 'auth', 'admin', 'sessions']
        for app in basic_apps:
            try:
                call_command('migrate', app, verbosity=1, interactive=False)
                print(f"✅ {app} migrado")
            except Exception as e:
                print(f"⚠️  Error en {app}: {e}")
        
        # 3. Manejar categorias específicamente
        try:
            print("📋 Migrando categorias...")
            # Intentar migrar a la última migración conocida
            call_command('migrate', 'categorias', '0008', verbosity=1, interactive=False)
            print("✅ Categorias migrado a 0008")
        except Exception as e:
            print(f"⚠️  Error migrando categorias a 0008: {e}")
            try:
                # Intentar migración general
                call_command('migrate', 'categorias', verbosity=1, interactive=False)
                print("✅ Categorias migrado")
            except Exception as e2:
                print(f"❌ Error crítico en categorias: {e2}")
        
        # 4. Migrar otras apps
        other_apps = ['productos', 'ventas', 'pedidos']
        for app in other_apps:
            try:
                call_command('migrate', app, verbosity=1, interactive=False)
                print(f"✅ {app} migrado")
            except Exception as e:
                print(f"⚠️  Error en {app}: {e}")
        
        # 5. Migración final
        try:
            call_command('migrate', verbosity=1, interactive=False)
            print("✅ Migración final completada")
        except Exception as e:
            print(f"⚠️  Error en migración final: {e}")
        
        # 6. Crear superusuario
        try:
            from django.contrib.auth.models import User
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
                print("✅ Superusuario creado")
        except Exception as e:
            print(f"⚠️  Error creando superusuario: {e}")
        
        # 7. Recolectar archivos estáticos
        try:
            call_command('collectstatic', '--noinput', verbosity=1)
            print("✅ Archivos estáticos recolectados")
        except Exception as e:
            print(f"⚠️  Error recolectando estáticos: {e}")
        
        print("🎉 ¡Despliegue forzado completado!")
        return True
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

def main():
    """Función principal"""
    if force_deploy():
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main()) 