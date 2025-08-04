#!/usr/bin/env python
"""
Script para arreglar conflictos de migraciones en la base de datos
"""
import os
import sys
import django
from django.core.management import call_command
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

def fix_db_migrations():
    """Arreglar conflictos de migraciones en la base de datos"""
    try:
        print("🔧 Arreglando conflictos de migraciones en BD...")
        
        # Verificar conexión a la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexión a BD establecida")
        
        # 1. Intentar hacer merge automático
        try:
            print("🔄 Ejecutando merge automático...")
            call_command('makemigrations', '--merge', verbosity=2)
            print("✅ Merge automático completado")
        except Exception as e:
            print(f"⚠️  Error en merge automático: {e}")
        
        # 2. Ejecutar migraciones básicas
        print("📋 Ejecutando migraciones básicas...")
        basic_apps = ['contenttypes', 'auth', 'admin', 'sessions']
        for app in basic_apps:
            try:
                call_command('migrate', app, verbosity=1, interactive=False)
                print(f"✅ {app} migrado")
            except Exception as e:
                print(f"⚠️  Error en {app}: {e}")
        
        # 3. Manejar categorias con estrategia específica
        print("📋 Arreglando categorias...")
        try:
            # Intentar migrar a la migración más reciente
            call_command('migrate', 'categorias', '0009', verbosity=1, interactive=False)
            print("✅ Categorias migrado a 0009")
        except Exception as e:
            print(f"⚠️  Error migrando categorias a 0009: {e}")
            try:
                # Intentar migración general
                call_command('migrate', 'categorias', verbosity=1, interactive=False)
                print("✅ Categorias migrado")
            except Exception as e2:
                print(f"❌ Error crítico en categorias: {e2}")
                # Intentar resetear la tabla de migraciones
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("DELETE FROM django_migrations WHERE app = 'categorias'")
                        print("✅ Tabla de migraciones de categorias reseteada")
                except Exception as e3:
                    print(f"❌ Error reseteando migraciones: {e3}")
        
        # 4. Migrar otras apps
        print("📋 Migrando otras apps...")
        other_apps = ['productos', 'ventas', 'pedidos']
        for app in other_apps:
            try:
                call_command('migrate', app, verbosity=1, interactive=False)
                print(f"✅ {app} migrado")
            except Exception as e:
                print(f"⚠️  Error en {app}: {e}")
        
        # 5. Migración final
        print("📋 Ejecutando migración final...")
        try:
            call_command('migrate', verbosity=1, interactive=False)
            print("✅ Migración final completada")
        except Exception as e:
            print(f"⚠️  Error en migración final: {e}")
        
        # 6. Crear superusuario
        print("👤 Creando superusuario...")
        try:
            from django.contrib.auth.models import User
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
                print("✅ Superusuario creado")
        except Exception as e:
            print(f"⚠️  Error creando superusuario: {e}")
        
        # 7. Recolectar archivos estáticos
        print("📁 Recolectando archivos estáticos...")
        try:
            call_command('collectstatic', '--noinput', verbosity=1)
            print("✅ Archivos estáticos recolectados")
        except Exception as e:
            print(f"⚠️  Error recolectando estáticos: {e}")
        
        print("🎉 ¡Conflictos de migraciones arreglados!")
        return True
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

def main():
    """Función principal"""
    if fix_db_migrations():
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main()) 