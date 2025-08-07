#!/usr/bin/env python
"""
Script final para probar la configuración corregida de Cloudinary
"""
import os
import sys
import django
import requests
import json
import time
from pathlib import Path

# Simular entorno de Render
os.environ['RENDER'] = 'true'
os.environ['DJANGO_SETTINGS_MODULE'] = 'Backend.render_settings'

# Configurar Django
django.setup()

def test_final_configuration():
    """Probar la configuración final"""
    
    print("🎯 PRUEBA FINAL DE CONFIGURACIÓN")
    print("="*50)
    
    try:
        from django.conf import settings
        
        print("📋 Configuración final:")
        print(f"  RENDER: {os.environ.get('RENDER', 'No definido')}")
        print(f"  DEBUG: {settings.DEBUG}")
        print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        print(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
        
        # Verificar configuración de Cloudinary
        if hasattr(settings, 'CLOUDINARY'):
            print("\n☁️ Configuración de Cloudinary:")
            print(f"  Cloud Name: {settings.CLOUDINARY.get('cloud_name', 'No definido')}")
            print(f"  API Key: {settings.CLOUDINARY.get('api_key', 'No definido')[:10]}..." if settings.CLOUDINARY.get('api_key') else "  API Key: No definido")
            print(f"  API Secret: {settings.CLOUDINARY.get('api_secret', 'No definido')[:10]}..." if settings.CLOUDINARY.get('api_secret') else "  API Secret: No definido")
        else:
            print("\n❌ No se encontró configuración de Cloudinary")
            return False
        
        # Verificar CLOUDINARY_STORAGE
        if hasattr(settings, 'CLOUDINARY_STORAGE'):
            print("\n💾 Configuración de CLOUDINARY_STORAGE:")
            print(f"  CLOUD_NAME: {settings.CLOUDINARY_STORAGE.get('CLOUD_NAME', 'No definido')}")
            print(f"  API_KEY: {settings.CLOUDINARY_STORAGE.get('API_KEY', 'No definido')[:10]}..." if settings.CLOUDINARY_STORAGE.get('API_KEY') else "  API_KEY: No definido")
            print(f"  API_SECRET: {settings.CLOUDINARY_STORAGE.get('API_SECRET', 'No definido')[:10]}..." if settings.CLOUDINARY_STORAGE.get('API_SECRET') else "  API_SECRET: No definido")
        else:
            print("\n❌ No se encontró configuración de CLOUDINARY_STORAGE")
            return False
        
        # Verificar CORS
        print("\n🌐 Configuración de CORS:")
        print(f"  CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def test_api_final():
    """Probar API final"""
    
    print("\n" + "="*50)
    print("🌐 PROBANDO API FINAL")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\cartera-casual-para-mujer-23064.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    try:
        # Preparar datos de la categoría
        categoria_data = {
            'nombre': 'Test Final Configuration',
            'descripcion': 'Prueba final de configuración corregida',
            'activa': True,
            'orden': 992
        }
        
        print(f"📋 Datos de la categoría: {categoria_data}")
        
        # Preparar la petición
        url = f"{RENDER_API_URL}/categorias/"
        
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('test-final-configuration.jpg', image_file, 'image/jpeg')
            }
            
            print(f"\n🚀 Creando categoría final en: {url}")
            
            response = requests.post(url, files=files, data=categoria_data, timeout=60)
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📊 Response Headers: {dict(response.headers)}")
            print(f"📊 Response Text: {response.text}")
            
            if response.status_code == 201:
                try:
                    categoria_data = response.json()
                    print("✅ ¡Categoría creada exitosamente!")
                    print(f"📸 ID de la categoría: {categoria_data.get('id')}")
                    print(f"🏷️ Nombre: {categoria_data.get('nombre')}")
                    print(f"🔗 Slug: {categoria_data.get('slug')}")
                    print(f"🔗 URL de la imagen: {categoria_data.get('imagen_url')}")
                    
                    # Verificar si la imagen se subió a Cloudinary
                    imagen_url = categoria_data.get('imagen_url', '')
                    if 'cloudinary.com' in imagen_url:
                        print("☁️ ¡La imagen se subió a Cloudinary!")
                        print("✅ Configuración final: EXITOSA")
                        return True
                    else:
                        print("📁 La imagen se guardó localmente en Render")
                        print("⚠️ Configuración final: PARCIAL")
                        print("🔧 Las imágenes deberían subirse a Cloudinary")
                        return False
                    
                except json.JSONDecodeError as e:
                    print(f"❌ Error decodificando respuesta: {e}")
                    return False
            else:
                print(f"❌ Error al crear la categoría: {response.status_code}")
                return False
                
    except requests.exceptions.Timeout:
        print("❌ Timeout: La creación tardó demasiado")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión durante la creación")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 PRUEBA FINAL DE CONFIGURACIÓN")
    print("="*50)
    
    # Probar configuración
    config_ok = test_final_configuration()
    
    # Probar API final
    api_ok = test_api_final()
    
    print("\n" + "="*50)
    print("📊 RESUMEN FINAL")
    print("="*50)
    print(f"✅ Configuración final: {'EXITOSA' if config_ok else 'FALLIDA'}")
    print(f"✅ API final: {'EXITOSA' if api_ok else 'FALLIDA'}")
    
    # Conclusión final
    print("\n" + "="*50)
    print("🎯 CONCLUSIÓN FINAL")
    print("="*50)
    
    if config_ok and api_ok:
        print("🎉 ¡La configuración final funciona perfectamente!")
        print("✅ Las imágenes se suben a Cloudinary")
        print("✅ La configuración está correcta")
        print("✅ La API funciona con Cloudinary")
    elif config_ok:
        print("✅ La configuración está correcta")
        print("⚠️ Pero hay problemas con la API")
        print("🔧 Esto indica un problema en el entorno de Render")
    else:
        print("❌ Hay problemas con la configuración")
        print("🔧 Revisar configuración de Cloudinary")
    
    print("\n💡 RECOMENDACIONES FINALES:")
    print("1. Verificar que las variables de entorno estén configuradas en Render")
    print("2. Asegurar que cloudinary_storage esté en INSTALLED_APPS")
    print("3. Verificar que DEFAULT_FILE_STORAGE esté configurado correctamente")
    print("4. Considerar actualizar django-cloudinary-storage a una versión más reciente")
    print("5. Verificar que el entorno de Render esté usando render_settings.py")

if __name__ == '__main__':
    main() 