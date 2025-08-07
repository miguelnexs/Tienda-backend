#!/usr/bin/env python
"""
Script para verificar y corregir las credenciales de Cloudinary en Render
"""
import os
import sys
import django
import requests
import json
import time
from pathlib import Path

# Configurar Django para Render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

def check_cloudinary_credentials():
    """Verificar las credenciales de Cloudinary"""
    
    print("🔍 VERIFICANDO CREDENCIALES DE CLOUDINARY")
    print("="*50)
    
    try:
        from django.conf import settings
        
        print("📋 Configuración actual:")
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
        
        # Verificar variables de entorno
        print("\n🔧 Variables de entorno:")
        print(f"  CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME', 'No definida')}")
        print(f"  CLOUDINARY_API_KEY: {os.environ.get('CLOUDINARY_API_KEY', 'No definida')[:10]}..." if os.environ.get('CLOUDINARY_API_KEY') else "  CLOUDINARY_API_KEY: No definida")
        print(f"  CLOUDINARY_API_SECRET: {os.environ.get('CLOUDINARY_API_SECRET', 'No definida')[:10]}..." if os.environ.get('CLOUDINARY_API_SECRET') else "  CLOUDINARY_API_SECRET: No definida")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def test_cloudinary_upload():
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
            folder="test-fix-render",
            public_id="test-cloudinary-fix",
            overwrite=True,
            resource_type="image",
            transformation=[
                {"width": 400, "height": 300, "crop": "fill"},
                {"quality": "auto", "fetch_format": "auto"}
            ],
            tags=["test", "fix", "render"],
            context={
                "test": "Cloudinary Fix Render",
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

def test_render_api_with_cloudinary():
    """Probar API de Render con Cloudinary"""
    
    print("\n" + "="*50)
    print("🌐 PROBANDO API DE RENDER CON CLOUDINARY")
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
            'nombre': 'Test Cloudinary Fix',
            'descripcion': 'Prueba de corrección de Cloudinary en Render',
            'activa': True,
            'orden': 997
        }
        
        print(f"📋 Datos de la categoría: {categoria_data}")
        
        # Preparar la petición
        url = f"{RENDER_API_URL}/categorias/"
        
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('test-cloudinary-fix.jpg', image_file, 'image/jpeg')
            }
            
            print(f"\n🚀 Creando categoría en: {url}")
            
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
                        print("✅ Configuración de Cloudinary: CORRECTA")
                    else:
                        print("📁 La imagen se guardó localmente en Render")
                        print("⚠️ Configuración de Cloudinary: INCORRECTA")
                        print("🔧 Las imágenes deberían subirse a Cloudinary")
                    
                    return categoria_data
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

def check_existing_categories():
    """Verificar categorías existentes"""
    
    print("\n" + "="*50)
    print("📋 VERIFICANDO CATEGORÍAS EXISTENTES")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # Obtener categorías existentes
        url = f"{RENDER_API_URL}/categorias/"
        
        print(f"🚀 Obteniendo categorías de: {url}")
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            try:
                categorias = response.json()
                print(f"✅ Se encontraron {len(categorias)} categorías")
                
                for i, categoria in enumerate(categorias[:5]):  # Mostrar solo las primeras 5
                    print(f"\n📋 Categoría {i+1}:")
                    print(f"   ID: {categoria.get('id')}")
                    print(f"   Nombre: {categoria.get('nombre')}")
                    print(f"   Slug: {categoria.get('slug')}")
                    print(f"   URL de imagen: {categoria.get('imagen_url')}")
                    
                    # Verificar si la imagen está en Cloudinary
                    imagen_url = categoria.get('imagen_url', '')
                    if 'cloudinary.com' in imagen_url:
                        print("   ☁️ Imagen en Cloudinary")
                    else:
                        print("   📁 Imagen local en Render")
                
                return categorias
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                return False
        else:
            print(f"❌ Error obteniendo categorías: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 CORRECCIÓN DE CLOUDINARY EN RENDER")
    print("="*50)
    
    # Verificar credenciales
    credentials_ok = check_cloudinary_credentials()
    
    # Probar subida directa a Cloudinary
    cloudinary_ok = test_cloudinary_upload()
    
    # Verificar categorías existentes
    existing_categories = check_existing_categories()
    
    # Probar API de Render
    api_ok = test_render_api_with_cloudinary()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("="*50)
    print(f"✅ Credenciales de Cloudinary: {'EXITOSA' if credentials_ok else 'FALLIDA'}")
    print(f"✅ Subida directa a Cloudinary: {'EXITOSA' if cloudinary_ok else 'FALLIDA'}")
    print(f"✅ API de Render: {'EXITOSA' if api_ok else 'FALLIDA'}")
    
    # Diagnóstico
    print("\n" + "="*50)
    print("🎯 DIAGNÓSTICO")
    print("="*50)
    
    if cloudinary_ok and api_ok:
        print("✅ Cloudinary está configurado correctamente")
        print("✅ Las subidas directas funcionan")
        print("⚠️ Pero las imágenes de categorías se guardan localmente")
        print("🔧 Esto indica un problema en la configuración de Django")
    elif cloudinary_ok:
        print("✅ Cloudinary funciona para subidas directas")
        print("❌ Pero hay problemas con la API de Render")
    else:
        print("❌ Hay problemas con las credenciales de Cloudinary")
        print("🔧 Revisar configuración de variables de entorno")
    
    print("\n💡 RECOMENDACIONES:")
    print("1. Verificar que las variables de entorno estén configuradas en Render")
    print("2. Asegurar que DEFAULT_FILE_STORAGE esté configurado correctamente")
    print("3. Verificar que cloudinary_storage esté en INSTALLED_APPS")

if __name__ == '__main__':
    main() 