#!/usr/bin/env python
"""
Script para probar la configuración corregida de Cloudinary
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

def test_cloudinary_configuration():
    """Probar la configuración de Cloudinary"""
    
    print("🔧 PROBANDO CONFIGURACIÓN CORREGIDA DE CLOUDINARY")
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

def test_django_storage():
    """Probar el storage de Django"""
    
    print("\n" + "="*50)
    print("💾 PROBANDO STORAGE DE DJANGO")
    print("="*50)
    
    try:
        from django.conf import settings
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        print("📋 Información del storage:")
        print(f"  Storage class: {type(default_storage).__name__}")
        print(f"  Storage module: {default_storage.__class__.__module__}")
        
        # Probar escritura de archivo
        test_content = b"Test file for Django storage with Cloudinary"
        test_filename = "test-cloudinary-fixed.txt"
        
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
                    print("✅ Configuración de Cloudinary: CORRECTA")
                else:
                    print("📁 El archivo se guardó localmente")
                    print("⚠️ Configuración de Cloudinary: INCORRECTA")
                
                # Limpiar archivo de prueba
                default_storage.delete(path)
                print("🧹 Archivo de prueba eliminado")
                
                return 'cloudinary.com' in url
        else:
            print("❌ No se pudo verificar el archivo")
            return False
            
    except Exception as e:
        print(f"❌ Error en storage de Django: {e}")
        return False

def test_api_with_cloudinary():
    """Probar API con Cloudinary"""
    
    print("\n" + "="*50)
    print("🌐 PROBANDO API CON CLOUDINARY")
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
            'nombre': 'Test Cloudinary Fixed',
            'descripcion': 'Prueba de configuración corregida de Cloudinary',
            'activa': True,
            'orden': 996
        }
        
        print(f"📋 Datos de la categoría: {categoria_data}")
        
        # Preparar la petición
        url = f"{RENDER_API_URL}/categorias/"
        
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('test-cloudinary-fixed.jpg', image_file, 'image/jpeg')
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
                        print("✅ Configuración corregida: EXITOSA")
                        return True
                    else:
                        print("📁 La imagen se guardó localmente en Render")
                        print("⚠️ Configuración corregida: PARCIAL")
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
    print("🔧 PRUEBA DE CONFIGURACIÓN CORREGIDA")
    print("="*50)
    
    # Probar configuración
    config_ok = test_cloudinary_configuration()
    
    # Probar storage de Django
    storage_ok = test_django_storage()
    
    # Probar API
    api_ok = test_api_with_cloudinary()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    print(f"✅ Configuración de Cloudinary: {'EXITOSA' if config_ok else 'FALLIDA'}")
    print(f"✅ Storage de Django: {'EXITOSA' if storage_ok else 'FALLIDA'}")
    print(f"✅ API con Cloudinary: {'EXITOSA' if api_ok else 'FALLIDA'}")
    
    # Conclusión
    print("\n" + "="*50)
    print("🎯 CONCLUSIÓN")
    print("="*50)
    
    if config_ok and storage_ok and api_ok:
        print("🎉 ¡La configuración corregida funciona perfectamente!")
        print("✅ Las imágenes se suben a Cloudinary")
        print("✅ El storage está configurado correctamente")
        print("✅ La API funciona con Cloudinary")
    elif config_ok and storage_ok:
        print("✅ La configuración está correcta")
        print("⚠️ Pero hay problemas con la API")
    elif config_ok:
        print("⚠️ La configuración básica está bien")
        print("❌ Pero hay problemas con el storage")
    else:
        print("❌ Hay problemas con la configuración")
        print("🔧 Revisar configuración de Cloudinary")

if __name__ == '__main__':
    main() 