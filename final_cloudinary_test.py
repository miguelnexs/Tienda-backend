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

def test_final_cloudinary_config():
    """Probar la configuración final de Cloudinary"""
    
    print("🎯 PRUEBA FINAL DE CLOUDINARY")
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
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def test_direct_cloudinary_upload():
    """Probar subida directa a Cloudinary"""
    
    print("\n" + "="*50)
    print("☁️ PROBANDO SUBIDA DIRECTA A CLOUDINARY")
    print("="*50)
    
    try:
        import cloudinary
        import cloudinary.uploader
        import cloudinary.api
        
        # Obtener configuración de Django
        from django.conf import settings
        
        cloud_name = settings.CLOUDINARY.get('cloud_name')
        api_key = settings.CLOUDINARY.get('api_key')
        api_secret = settings.CLOUDINARY.get('api_secret')
        
        print(f"🔑 Configurando Cloudinary:")
        print(f"  Cloud Name: {cloud_name}")
        print(f"  API Key: {api_key[:10]}..." if api_key else "  API Key: No disponible")
        print(f"  API Secret: {api_secret[:10]}..." if api_secret else "  API Secret: No disponible")
        
        if not all([cloud_name, api_key, api_secret]):
            print("❌ Faltan credenciales de Cloudinary")
            return False
        
        # Configurar Cloudinary
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
        print("\n🚀 Probando conexión a Cloudinary...")
        
        # Probar conexión subiendo una imagen de prueba
        test_image_path = r"D:\usuario\Downloads\bolso\cartera-casual-para-mujer-23064.jpg"
        
        if not os.path.exists(test_image_path):
            print(f"❌ No se encuentra la imagen de prueba: {test_image_path}")
            return False
        
        print(f"📁 Subiendo imagen de prueba: {test_image_path}")
        
        result = cloudinary.uploader.upload(
            test_image_path,
            folder="final-test",
            public_id="final-cloudinary-test",
            overwrite=True,
            resource_type="image",
            transformation=[
                {"width": 500, "height": 400, "crop": "fill"},
                {"quality": "auto", "fetch_format": "auto"}
            ],
            tags=["final", "test", "cloudinary"],
            context={
                "test": "Final Cloudinary Test",
                "timestamp": str(int(time.time()))
            }
        )
        
        print("✅ Subida a Cloudinary exitosa!")
        print(f"📸 URL de la imagen: {result['secure_url']}")
        print(f"📁 Public ID: {result['public_id']}")
        print(f"📏 Tamaño: {result['bytes']} bytes")
        print(f"🖼️ Formato: {result['format']}")
        print(f"📐 Dimensiones: {result['width']}x{result['height']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error en subida a Cloudinary: {e}")
        return False

def test_api_final():
    """Probar API final con Cloudinary"""
    
    print("\n" + "="*50)
    print("🌐 PROBANDO API FINAL CON CLOUDINARY")
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
            'nombre': 'Test Final Cloudinary',
            'descripcion': 'Prueba final de configuración de Cloudinary',
            'activa': True,
            'orden': 994
        }
        
        print(f"📋 Datos de la categoría: {categoria_data}")
        
        # Preparar la petición
        url = f"{RENDER_API_URL}/categorias/"
        
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('test-final-cloudinary.jpg', image_file, 'image/jpeg')
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
    print("🎯 PRUEBA FINAL DE CLOUDINARY")
    print("="*50)
    
    # Probar configuración
    config_ok = test_final_cloudinary_config()
    
    # Probar subida directa
    direct_ok = test_direct_cloudinary_upload()
    
    # Probar API final
    api_ok = test_api_final()
    
    print("\n" + "="*50)
    print("📊 RESUMEN FINAL")
    print("="*50)
    print(f"✅ Configuración de Cloudinary: {'EXITOSA' if config_ok else 'FALLIDA'}")
    print(f"✅ Subida directa a Cloudinary: {'EXITOSA' if direct_ok else 'FALLIDA'}")
    print(f"✅ API con Cloudinary: {'EXITOSA' if api_ok else 'FALLIDA'}")
    
    # Conclusión final
    print("\n" + "="*50)
    print("🎯 CONCLUSIÓN FINAL")
    print("="*50)
    
    if config_ok and direct_ok and api_ok:
        print("🎉 ¡La configuración final funciona perfectamente!")
        print("✅ Las imágenes se suben a Cloudinary")
        print("✅ La configuración está correcta")
        print("✅ La API funciona con Cloudinary")
    elif config_ok and direct_ok:
        print("✅ La configuración está correcta")
        print("✅ Las subidas directas funcionan")
        print("⚠️ Pero hay problemas con la API")
        print("🔧 Esto indica un problema en el entorno de Render")
    elif config_ok:
        print("⚠️ La configuración básica está bien")
        print("❌ Pero hay problemas con las subidas")
    else:
        print("❌ Hay problemas con la configuración")
        print("🔧 Revisar configuración de Cloudinary")
    
    print("\n💡 RECOMENDACIONES FINALES:")
    print("1. Verificar que las variables de entorno estén configuradas en Render")
    print("2. Asegurar que cloudinary_storage esté en INSTALLED_APPS")
    print("3. Verificar que DEFAULT_FILE_STORAGE esté configurado correctamente")
    print("4. Considerar actualizar django-cloudinary-storage a una versión más reciente")

if __name__ == '__main__':
    main() 