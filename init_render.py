#!/usr/bin/env python
"""
Script de inicialización para Render
"""
import os
import sys
import django
from django.core.management import call_command

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

def init_database():
    """Inicializar la base de datos en Render"""
    try:
        print("🗄️  Inicializando base de datos...")
        
        # Ejecutar migraciones
        print("📋 Ejecutando migraciones...")
        call_command('migrate', verbosity=2)
        
        # Crear superusuario si no existe
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            print("👤 Creando superusuario...")
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("✅ Superusuario creado: admin/admin123")
        
        # Recolectar archivos estáticos
        print("📁 Recolectando archivos estáticos...")
        call_command('collectstatic', '--noinput', verbosity=2)
        
        print("✅ Inicialización completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1) 