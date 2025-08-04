#!/usr/bin/env python
"""
Script para resetear migraciones problemáticas
"""
import os
import sys
import django
from django.core.management import call_command
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

def reset_problematic_migrations():
    """Resetear migraciones problemáticas"""
    try:
        print("🔄 Reseteando migraciones problemáticas...")
        
        # Marcar migraciones como no aplicadas
        call_command('migrate', 'categorias', '0002', verbosity=2)
        print("✅ Migraciones de categorias reseteadas")
        
        # Aplicar migraciones corregidas
        call_command('migrate', verbosity=2)
        print("✅ Migraciones aplicadas correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reseteando migraciones: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando reset de migraciones...")
    print("=" * 50)
    
    if reset_problematic_migrations():
        print("🎉 ¡Reset completado exitosamente!")
        return 0
    else:
        print("❌ Fallo en el reset")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 