#!/usr/bin/env python
"""
Script para resolver conflictos de migraciones
"""
import os
import sys
import django
from django.core.management import call_command
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

def fix_migration_conflicts():
    """Resolver conflictos de migraciones"""
    try:
        print("🔄 Resolviendo conflictos de migraciones...")
        
        # Verificar conexión a la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexión a BD establecida")
        
        # Intentar hacer merge de migraciones
        try:
            call_command('makemigrations', '--merge', verbosity=2)
            print("✅ Merge de migraciones completado")
        except Exception as e:
            print(f"⚠️  Error en merge: {e}")
        
        # Ejecutar migraciones
        call_command('migrate', verbosity=2, interactive=False)
        print("✅ Migraciones aplicadas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error resolviendo conflictos: {e}")
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
    print("🚀 Iniciando resolución de conflictos...")
    
    if fix_migration_conflicts():
        create_superuser()
        collect_static()
        print("🎉 ¡Conflictos resueltos!")
        return 0
    else:
        print("❌ Fallo resolviendo conflictos")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 