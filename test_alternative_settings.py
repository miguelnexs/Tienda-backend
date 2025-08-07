#!/usr/bin/env python
"""
Script para probar diferentes configuraciones de DJANGO_SETTINGS_MODULE
"""
import os
import sys
import django

def test_settings_module(module_path):
    """Probar un módulo de settings específico"""
    
    print(f"\n🔍 PROBANDO: {module_path}")
    print("="*50)
    
    try:
        # Limpiar configuración anterior
        if 'DJANGO_SETTINGS_MODULE' in os.environ:
            del os.environ['DJANGO_SETTINGS_MODULE']
        
        # Configurar nuevo módulo
        os.environ['DJANGO_SETTINGS_MODULE'] = module_path
        os.environ['RENDER'] = 'true'
        
        # Configurar DATABASE_URL para pruebas
        if not os.environ.get('DATABASE_URL'):
            os.environ['DATABASE_URL'] = 'postgresql://tienda_user:PWKuO99372EAcsyx5KpHlV9VBIQJkvle@dpg-d278j5u3jp1c73en5gbg-a.ohio-postgres.render.com/tienda_production'
        
        # Configurar Django
        django.setup()
        
        from django.conf import settings
        
        print("✅ Módulo cargado exitosamente")
        print(f"📋 DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        print(f"📋 STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
        
        if hasattr(settings, 'CLOUDINARY'):
            print(f"☁️ CLOUDINARY configurado: {settings.CLOUDINARY}")
        else:
            print("❌ CLOUDINARY no configurado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 PROBANDO DIFERENTES CONFIGURACIONES DE SETTINGS")
    print("="*60)
    
    # Lista de módulos a probar
    modules_to_test = [
        'Backend.render_settings',
        'Backend.settings',
        'render_settings',
        'settings',
        'Backend.Backend.render_settings',
        'Backend.Backend.settings',
    ]
    
    results = {}
    
    for module in modules_to_test:
        success = test_settings_module(module)
        results[module] = success
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    for module, success in results.items():
        status = "✅ EXITOSO" if success else "❌ FALLIDO"
        print(f"{module}: {status}")
    
    print("\n💡 RECOMENDACIONES:")
    print("1. Si 'Backend.render_settings' falla, probar con 'render_settings'")
    print("2. Si 'render_settings' funciona, cambiar la variable en Render")
    print("3. Verificar que el archivo render_settings.py existe en la ubicación correcta")

if __name__ == '__main__':
    main() 