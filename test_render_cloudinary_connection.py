#!/usr/bin/env python
"""
Script para probar la conexión entre Render y Cloudinary
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

def test_render_cloudinary_settings():
    """Probar configuración de Cloudinary en Render"""
    
    print("🔧 PROBANDO CONFIGURACIÓN DE CLOUDINARY EN RENDER")
    print("="*50)
    
    try:
        from django.conf import settings
        
        print("📋 Configuración de Django:")
        print(f"  DEBUG: {settings.DEBUG}")
        print(f"  RENDER: {os.environ.get('RENDER', 'No definido')}")
        print(f"  DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
        
        # Verificar configuración de Cloudinary
        if hasattr(settings, 'CLOUDINARY'):
            print("\n☁️ Configuración de Cloudinary:")
            print(f"  Cloud Name: {settings.CLOUDINARY.get('cloud_name', 'No definido')}")
            print(f"  API Key: {settings.CLOUDINARY.get('api_key', 'No definido')[:10]}..." if settings.CLOUDINARY.get('api_key') else "  API Key: No definido")
            print(f"  API Secret: {settings.CLOUDINARY.get('api_secret', 'No definido')[:10]}..." if settings.CLOUDINARY.get('api_secret') else "  API Secret: No definido")
        else:
            print("\n❌ No se encontró configuración de Cloudinary")
            return False
        
        # Verificar configuración de almacenamiento
        print(f"\n💾 Configuración de almacenamiento:")
        print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        print(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
        
        # Verificar si está configurado para Cloudinary
        if 'cloudinary' in str(settings.DEFAULT_FILE_STORAGE).lower():
            print("✅ Almacenamiento configurado para Cloudinary")
        else:
            print("⚠️ Almacenamiento NO configurado para Cloudinary")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def test_cloudinary_direct_connection():
    """Probar conexión directa a Cloudinary"""
    
    print("\n" + "="*50)
    print("☁️ PROBANDO CONEXIÓN DIRECTA A CLOUDINARY")
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
            folder="test-render-connection",
            public_id="test-render-cloudinary",
            overwrite=True,
            resource_type="image",
            transformation=[
                {"width": 300, "height": 200, "crop": "fill"},
                {"quality": "auto", "fetch_format": "auto"}
            ],
            tags=["test", "render", "connection"],
            context={
                "test": "Render Cloudinary Connection",
                "timestamp": str(int(time.time()))
            }
        )
        
        print("✅ Conexión a Cloudinary exitosa!")
        print(f"📸 URL de la imagen: {result['secure_url']}")
        print(f"📁 Public ID: {result['public_id']}")
        print(f"📏 Tamaño: {result['bytes']} bytes")
        print(f"🖼️ Formato: {result['format']}")
        print(f"📐 Dimensiones: {result['width']}x{result['height']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error en conexión directa a Cloudinary: {e}")
        return False

def test_render_api_cloudinary_upload():
    """Probar subida de imagen via API de Render"""
    
    print("\n" + "="*50)
    print("🌐 PROBANDO SUBIDA VIA API DE RENDER")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\cartera-casual-para-mujer-23064.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    try:
        # Preparar datos de prueba
        test_data = {
            'nombre': 'Test Render Cloudinary',
            'descripcion': 'Prueba de conexión entre Render y Cloudinary',
            'activa': True,
            'orden': 999
        }
        
        print(f"📋 Datos de prueba: {test_data}")
        
        # Preparar la petición
        url = f"{RENDER_API_URL}/categorias/"
        
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('test-render-cloudinary.jpg', image_file, 'image/jpeg')
            }
            
            print(f"\n🚀 Creando categoría de prueba en: {url}")
            
            response = requests.post(url, files=files, data=test_data, timeout=60)
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📊 Response Headers: {dict(response.headers)}")
            print(f"📊 Response Text: {response.text}")
            
            if response.status_code == 201:
                try:
                    categoria_data = response.json()
                    print("✅ ¡Categoría de prueba creada exitosamente en Render!")
                    print(f"📸 ID de la categoría: {categoria_data.get('id')}")
                    print(f"🏷️ Nombre: {categoria_data.get('nombre')}")
                    print(f"🔗 Slug: {categoria_data.get('slug')}")
                    print(f"🔗 URL de la imagen: {categoria_data.get('imagen_url')}")
                    
                    # Verificar si la imagen se subió a Cloudinary
                    imagen_url = categoria_data.get('imagen_url', '')
                    if 'cloudinary.com' in imagen_url:
                        print("☁️ ¡La imagen se subió a Cloudinary desde Render!")
                        print("✅ Conexión Render-Cloudinary: EXITOSA")
                    else:
                        print("📁 La imagen se guardó localmente en Render")
                        print("⚠️ Conexión Render-Cloudinary: PARCIAL (local)")
                    
                    return categoria_data
                except json.JSONDecodeError as e:
                    print(f"❌ Error decodificando respuesta: {e}")
                    return False
            else:
                print(f"❌ Error al crear la categoría de prueba: {response.status_code}")
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

def test_render_environment_variables():
    """Probar variables de entorno de Render"""
    
    print("\n" + "="*50)
    print("🔧 PROBANDO VARIABLES DE ENTORNO DE RENDER")
    print("="*50)
    
    # Variables importantes de Render
    render_vars = [
        'RENDER',
        'RENDER_EXTERNAL_HOSTNAME',
        'RENDER_EXTERNAL_URL',
        'RENDER_SERVICE_ID',
        'RENDER_SERVICE_NAME',
        'RENDER_SERVICE_TYPE',
        'RENDER_INSTANCE_ID',
        'PORT',
        'DATABASE_URL',
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY',
        'CLOUDINARY_API_SECRET'
    ]
    
    print("📋 Variables de entorno de Render:")
    for var in render_vars:
        value = os.environ.get(var, 'No definida')
        if 'SECRET' in var or 'KEY' in var:
            display_value = f"{value[:10]}..." if value != 'No definida' else value
        else:
            display_value = value
        print(f"  {var}: {display_value}")
    
    # Verificar si estamos en Render
    is_render = os.environ.get('RENDER') == 'true'
    print(f"\n🌐 ¿Estamos en Render?: {'SÍ' if is_render else 'NO'}")
    
    return is_render

def test_django_cloudinary_integration():
    """Probar integración de Django con Cloudinary"""
    
    print("\n" + "="*50)
    print("🔗 PROBANDO INTEGRACIÓN DJANGO-CLOUDINARY")
    print("="*50)
    
    try:
        from django.conf import settings
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        print("📋 Configuración de almacenamiento:")
        print(f"  Storage class: {type(default_storage).__name__}")
        print(f"  Storage module: {default_storage.__class__.__module__}")
        
        # Probar escritura de archivo
        test_content = b"Test file for Django-Cloudinary integration"
        test_filename = "test-render-cloudinary.txt"
        
        print(f"\n🚀 Probando escritura de archivo: {test_filename}")
        
        # Escribir archivo
        path = default_storage.save(test_filename, ContentFile(test_content))
        print(f"✅ Archivo guardado en: {path}")
        
        # Leer archivo
        if default_storage.exists(path):
            with default_storage.open(path, 'rb') as f:
                content = f.read()
                print(f"✅ Archivo leído correctamente: {len(content)} bytes")
                
                # Verificar URL
                url = default_storage.url(path)
                print(f"🔗 URL del archivo: {url}")
                
                if 'cloudinary.com' in url:
                    print("☁️ ¡El archivo se guardó en Cloudinary!")
                else:
                    print("📁 El archivo se guardó localmente")
                
                # Limpiar archivo de prueba
                default_storage.delete(path)
                print("🧹 Archivo de prueba eliminado")
                
                return True
        else:
            print("❌ No se pudo verificar el archivo")
            return False
            
    except Exception as e:
        print(f"❌ Error en integración Django-Cloudinary: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA DE CONEXIÓN RENDER-CLOUDINARY")
    print("="*50)
    
    # Probar configuración
    config_ok = test_render_cloudinary_settings()
    
    # Probar variables de entorno
    is_render = test_render_environment_variables()
    
    # Probar conexión directa a Cloudinary
    cloudinary_ok = test_cloudinary_direct_connection()
    
    # Probar integración Django-Cloudinary
    django_cloudinary_ok = test_django_cloudinary_integration()
    
    # Probar subida via API
    api_ok = test_render_api_cloudinary_upload()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    print(f"✅ Configuración de Cloudinary: {'EXITOSA' if config_ok else 'FALLIDA'}")
    print(f"✅ Variables de entorno Render: {'EXITOSA' if is_render else 'NO EN RENDER'}")
    print(f"✅ Conexión directa Cloudinary: {'EXITOSA' if cloudinary_ok else 'FALLIDA'}")
    print(f"✅ Integración Django-Cloudinary: {'EXITOSA' if django_cloudinary_ok else 'FALLIDA'}")
    print(f"✅ Subida via API Render: {'EXITOSA' if api_ok else 'FALLIDA'}")
    
    # Conclusión
    print("\n" + "="*50)
    print("🎯 CONCLUSIÓN")
    print("="*50)
    
    if cloudinary_ok and api_ok:
        print("🎉 ¡Render está conectado correctamente con Cloudinary!")
        print("✅ Se pueden subir imágenes desde Render a Cloudinary")
        print("✅ La configuración está funcionando correctamente")
    elif cloudinary_ok:
        print("⚠️ Cloudinary funciona, pero hay problemas con la API de Render")
        print("✅ La configuración básica está correcta")
    elif api_ok:
        print("⚠️ La API de Render funciona, pero Cloudinary tiene problemas")
        print("✅ Las subidas funcionan localmente en Render")
    else:
        print("❌ Hay problemas con la conexión Render-Cloudinary")
        print("🔧 Revisar configuración y credenciales")

if __name__ == '__main__':
    main() 