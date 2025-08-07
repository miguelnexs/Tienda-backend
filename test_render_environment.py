#!/usr/bin/env python
"""
Script para simular el entorno de Render y probar la configuración
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

def test_render_environment():
    """Probar el entorno de Render simulado"""
    
    print("🌐 PROBANDO ENTORNO DE RENDER SIMULADO")
    print("="*50)
    
    try:
        from django.conf import settings
        
        print("📋 Configuración del entorno:")
        print(f"  RENDER: {os.environ.get('RENDER', 'No definido')}")
        print(f"  DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
        print(f"  DEBUG: {settings.DEBUG}")
        
        print("\n📋 Configuración de almacenamiento:")
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
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando entorno: {e}")
        return False

def test_storage_in_render():
    """Probar storage en entorno de Render"""
    
    print("\n" + "="*50)
    print("💾 PROBANDO STORAGE EN ENTORNO DE RENDER")
    print("="*50)
    
    try:
        from django.conf import settings
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        print("📋 Información del storage:")
        print(f"  Storage class: {type(default_storage).__name__}")
        print(f"  Storage module: {default_storage.__class__.__module__}")
        
        # Verificar si está usando Cloudinary
        if 'cloudinary' in str(type(default_storage)).lower():
            print("✅ Storage configurado para Cloudinary")
        else:
            print("⚠️ Storage NO configurado para Cloudinary")
        
        # Probar escritura de archivo
        test_content = b"Test file for Render environment with Cloudinary"
        test_filename = "test-render-environment.txt"
        
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
                    print("✅ Configuración de Render: CORRECTA")
                else:
                    print("📁 El archivo se guardó localmente")
                    print("⚠️ Configuración de Render: INCORRECTA")
                
                # Limpiar archivo de prueba
                try:
                    default_storage.delete(path)
                    print("🧹 Archivo de prueba eliminado")
                except:
                    print("⚠️ No se pudo eliminar el archivo de prueba")
                
                return 'cloudinary.com' in url
        else:
            print("❌ No se pudo verificar el archivo")
            return False
            
    except Exception as e:
        print(f"❌ Error en storage de Render: {e}")
        return False

def test_api_in_render():
    """Probar API en entorno de Render"""
    
    print("\n" + "="*50)
    print("🌐 PROBANDO API EN ENTORNO DE RENDER")
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
            'nombre': 'Test Render Environment',
            'descripcion': 'Prueba de entorno de Render con Cloudinary',
            'activa': True,
            'orden': 995
        }
        
        print(f"📋 Datos de la categoría: {categoria_data}")
        
        # Preparar la petición
        url = f"{RENDER_API_URL}/categorias/"
        
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('test-render-environment.jpg', image_file, 'image/jpeg')
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
                        print("✅ Entorno de Render: EXITOSO")
                        return True
                    else:
                        print("📁 La imagen se guardó localmente en Render")
                        print("⚠️ Entorno de Render: PARCIAL")
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
    print("🌐 PRUEBA DE ENTORNO DE RENDER")
    print("="*50)
    
    # Probar entorno
    env_ok = test_render_environment()
    
    # Probar storage en Render
    storage_ok = test_storage_in_render()
    
    # Probar API en Render
    api_ok = test_api_in_render()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    print(f"✅ Entorno de Render: {'EXITOSA' if env_ok else 'FALLIDA'}")
    print(f"✅ Storage en Render: {'EXITOSA' if storage_ok else 'FALLIDA'}")
    print(f"✅ API en Render: {'EXITOSA' if api_ok else 'FALLIDA'}")
    
    # Conclusión
    print("\n" + "="*50)
    print("🎯 CONCLUSIÓN")
    print("="*50)
    
    if env_ok and storage_ok and api_ok:
        print("🎉 ¡El entorno de Render funciona perfectamente!")
        print("✅ Las imágenes se suben a Cloudinary")
        print("✅ El storage está configurado correctamente")
        print("✅ La API funciona con Cloudinary")
    elif env_ok and storage_ok:
        print("✅ El entorno está configurado correctamente")
        print("⚠️ Pero hay problemas con la API")
    elif env_ok:
        print("⚠️ El entorno básico está bien")
        print("❌ Pero hay problemas con el storage")
    else:
        print("❌ Hay problemas con el entorno de Render")
        print("🔧 Revisar configuración de variables de entorno")

if __name__ == '__main__':
    main() 