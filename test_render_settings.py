#!/usr/bin/env python3
"""
Script para probar la configuración de render_settings.py
"""
import os
import sys
import django

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

def test_render_settings():
    """Probar configuración de render_settings"""
    print("🧪 PROBANDO CONFIGURACIÓN DE RENDER_SETTINGS")
    print("=" * 60)
    
    try:
        # Verificar configuración básica
        print("📋 Configuración básica:")
        print(f"  DEBUG: {settings.DEBUG}")
        print(f"  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"  INSTALLED_APPS: {len(settings.INSTALLED_APPS)} apps")
        
        # Verificar aplicaciones instaladas
        print("\n📱 Aplicaciones instaladas:")
        for app in settings.INSTALLED_APPS:
            print(f"  ✅ {app}")
        
        # Verificar base de datos
        print("\n🗄️ Configuración de base de datos:")
        print(f"  DATABASES: {list(settings.DATABASES.keys())}")
        
        # Verificar Cloudinary
        print("\n☁️ Configuración de Cloudinary:")
        print(f"  CLOUDINARY_CLOUD_NAME: {getattr(settings, 'CLOUDINARY_CLOUD_NAME', 'No configurado')}")
        print(f"  CLOUDINARY_API_KEY: {getattr(settings, 'CLOUDINARY_API_KEY', 'No configurado')[:10]}...")
        print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        
        # Verificar CORS
        print("\n🌐 Configuración de CORS:")
        print(f"  CORS_ALLOWED_ORIGINS: {len(settings.CORS_ALLOWED_ORIGINS)} orígenes")
        print(f"  CORS_ALLOW_ALL_ORIGINS: {getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', False)}")
        
        # Verificar REST Framework
        print("\n🔌 Configuración de REST Framework:")
        print(f"  REST_FRAMEWORK configurado: {'REST_FRAMEWORK' in dir(settings)}")
        
        # Verificar archivos estáticos
        print("\n📁 Configuración de archivos estáticos:")
        print(f"  STATIC_URL: {settings.STATIC_URL}")
        print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"  MEDIA_URL: {settings.MEDIA_URL}")
        print(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def test_models_loading():
    """Probar que los modelos se cargan correctamente"""
    print("\n🧪 PROBANDO CARGA DE MODELOS")
    print("=" * 60)
    
    try:
        # Importar modelos
        from categorias.models import CategoriaProducto
        from productos.models import Producto
        from ventas.models import Venta
        from pedidos.models import Pedido
        
        print("✅ Modelos importados correctamente:")
        print(f"  ✅ CategoriaProducto")
        print(f"  ✅ Producto")
        print(f"  ✅ Venta")
        print(f"  ✅ Pedido")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cargando modelos: {e}")
        return False

def test_cloudinary_config():
    """Probar configuración de Cloudinary"""
    print("\n🧪 PROBANDO CONFIGURACIÓN DE CLOUDINARY")
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
    print("🚀 INICIANDO PRUEBA DE RENDER_SETTINGS")
    print("=" * 60)
    
    # Probar configuración
    settings_success = test_render_settings()
    models_success = test_models_loading()
    cloudinary_success = test_cloudinary_config()
    storage_success = test_storage_config()
    
    print("\n📊 RESULTADOS DE PRUEBA")
    print("=" * 60)
    print(f"Configuración: {'✅ PASÓ' if settings_success else '❌ FALLÓ'}")
    print(f"Modelos: {'✅ PASÓ' if models_success else '❌ FALLÓ'}")
    print(f"Cloudinary: {'✅ PASÓ' if cloudinary_success else '❌ FALLÓ'}")
    print(f"Storage: {'✅ PASÓ' if storage_success else '❌ FALLÓ'}")
    
    if all([settings_success, models_success, cloudinary_success, storage_success]):
        print("\n🎉 ¡RENDER_SETTINGS FUNCIONA CORRECTAMENTE!")
        print("✅ Todas las configuraciones están correctas.")
        print("✅ Los modelos se cargan sin problemas.")
        print("✅ Cloudinary está configurado.")
        print("✅ Storage está configurado.")
        print("✅ Listo para deploy en Render.")
    else:
        print("\n⚠️ Hay problemas con la configuración.")
        print("❌ Revisa la configuración antes del deploy.") 