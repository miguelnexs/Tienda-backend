#!/usr/bin/env python3
"""
Script simple para verificar que la configuración de deploy funciona
"""
import os
import sys
import django

# Configurar variables de entorno para prueba
os.environ['DATABASE_URL'] = 'postgresql://test:test@localhost:5432/testdb'

# Configurar Django con render_settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
    print("✅ Django configurado correctamente con render_settings")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

from django.conf import settings

def test_basic_config():
    """Probar configuración básica"""
    print("🧪 PROBANDO CONFIGURACIÓN BÁSICA")
    print("=" * 60)
    
    try:
        # Verificar configuración básica
        print("📋 Configuración básica:")
        print(f"  DEBUG: {settings.DEBUG}")
        print(f"  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"  INSTALLED_APPS: {len(settings.INSTALLED_APPS)} apps")
        print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        
        # Verificar Cloudinary
        print("\n☁️ Configuración de Cloudinary:")
        print(f"  CLOUDINARY_CLOUD_NAME: {getattr(settings, 'CLOUDINARY_CLOUD_NAME', 'No configurado')}")
        print(f"  CLOUDINARY_API_KEY: {getattr(settings, 'CLOUDINARY_API_KEY', 'No configurado')[:10]}...")
        
        # Verificar base de datos
        print("\n🗄️ Configuración de base de datos:")
        print(f"  DATABASES: {list(settings.DATABASES.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def test_cloudinary_connection():
    """Probar conexión con Cloudinary"""
    print("\n🧪 PROBANDO CONEXIÓN CON CLOUDINARY")
    print("=" * 60)
    
    try:
        import cloudinary
        print(f"✅ Cloudinary configurado:")
        print(f"  Cloud Name: {cloudinary.config().cloud_name}")
        print(f"  API Key: {cloudinary.config().api_key[:10]}...")
        
        # Probar configuración básica
        if cloudinary.config().cloud_name and cloudinary.config().api_key:
            print("✅ Credenciales de Cloudinary configuradas")
            return True
        else:
            print("❌ Credenciales de Cloudinary no configuradas")
            return False
            
    except Exception as e:
        print(f"❌ Error configurando Cloudinary: {e}")
        return False

def test_storage_config():
    """Probar configuración de storage"""
    print("\n🧪 PROBANDO CONFIGURACIÓN DE STORAGE")
    print("=" * 60)
    
    try:
        from django.core.files.storage import default_storage
        print(f"✅ Storage configurado: {type(default_storage).__name__}")
        
        # Verificar que es nuestro storage personalizado
        if 'CloudinaryStorageFixedURLs' in str(type(default_storage)):
            print("✅ Storage personalizado de Cloudinary configurado")
            return True
        else:
            print("❌ Storage personalizado no configurado")
            return False
            
    except Exception as e:
        print(f"❌ Error configurando storage: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA SIMPLE DE DEPLOY")
    print("=" * 60)
    
    # Probar configuración
    basic_success = test_basic_config()
    cloudinary_success = test_cloudinary_connection()
    storage_success = test_storage_config()
    
    print("\n📊 RESULTADOS DE PRUEBA")
    print("=" * 60)
    print(f"Configuración básica: {'✅ PASÓ' if basic_success else '❌ FALLÓ'}")
    print(f"Cloudinary: {'✅ PASÓ' if cloudinary_success else '❌ FALLÓ'}")
    print(f"Storage: {'✅ PASÓ' if storage_success else '❌ FALLÓ'}")
    
    if all([basic_success, cloudinary_success, storage_success]):
        print("\n🎉 ¡CONFIGURACIÓN DE DEPLOY LISTA!")
        print("✅ Todas las configuraciones están correctas.")
        print("✅ Cloudinary está configurado.")
        print("✅ Storage está configurado.")
        print("✅ Listo para deploy en Render.")
        print("\n🚀 PUEDES HACER DEPLOY EN RENDER")
    else:
        print("\n⚠️ Hay problemas con la configuración.")
        print("❌ Revisa la configuración antes del deploy.") 