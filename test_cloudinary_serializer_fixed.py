#!/usr/bin/env python
"""
Script para probar el serializer corregido con Cloudinary
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

def test_cloudinary_serializer():
    """Probar el serializer corregido con Cloudinary"""
    
    print("🔧 PROBANDO SERIALIZER CORREGIDO CON CLOUDINARY")
    print("="*50)
    
    try:
        from django.conf import settings
        
        print("📋 Configuración actual:")
        print(f"  RENDER: {os.environ.get('RENDER', 'No definido')}")
        print(f"  DEBUG: {settings.DEBUG}")
        print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        
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
        print(f"❌ Error verificando configuración: {e}")
        return False

def test_api_with_cloudinary_serializer():
    """Probar API con serializer corregido"""
    
    print("\n" + "="*50)
    print("🌐 PROBANDO API CON SERIALIZER CORREGIDO")
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
            'nombre': 'Test Cloudinary Serializer Fixed',
            'descripcion': 'Prueba del serializer corregido con Cloudinary',
            'activa': True,
            'orden': 993
        }
        
        print(f"📋 Datos de la categoría: {categoria_data}")
        
        # Preparar la petición
        url = f"{RENDER_API_URL}/categorias/"
        
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('test-cloudinary-serializer-fixed.jpg', image_file, 'image/jpeg')
            }
            
            print(f"\n🚀 Creando categoría con serializer corregido en: {url}")
            
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
                        print("✅ Serializer corregido: EXITOSO")
                        return True
                    else:
                        print("📁 La imagen se guardó localmente en Render")
                        print("⚠️ Serializer corregido: PARCIAL")
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

def test_cors_configuration():
    """Probar configuración de CORS"""
    
    print("\n" + "="*50)
    print("🌐 PROBANDO CONFIGURACIÓN DE CORS")
    print("="*50)
    
    try:
        from django.conf import settings
        
        print("📋 Configuración de CORS:")
        print(f"  CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}")
        
        # Verificar que los orígenes necesarios estén incluidos
        required_origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "https://tienda-backend-qsre.onrender.com",
        ]
        
        missing_origins = []
        for origin in required_origins:
            if origin not in settings.CORS_ALLOWED_ORIGINS:
                missing_origins.append(origin)
        
        if missing_origins:
            print(f"⚠️ Orígenes faltantes: {missing_origins}")
            return False
        else:
            print("✅ Todos los orígenes necesarios están configurados")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando CORS: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 PRUEBA DEL SERIALIZER CORREGIDO")
    print("="*50)
    
    # Probar configuración
    config_ok = test_cloudinary_serializer()
    
    # Probar configuración de CORS
    cors_ok = test_cors_configuration()
    
    # Probar API con serializer corregido
    api_ok = test_api_with_cloudinary_serializer()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    print(f"✅ Configuración de Cloudinary: {'EXITOSA' if config_ok else 'FALLIDA'}")
    print(f"✅ Configuración de CORS: {'EXITOSA' if cors_ok else 'FALLIDA'}")
    print(f"✅ API con serializer corregido: {'EXITOSA' if api_ok else 'FALLIDA'}")
    
    # Conclusión
    print("\n" + "="*50)
    print("🎯 CONCLUSIÓN")
    print("="*50)
    
    if config_ok and cors_ok and api_ok:
        print("🎉 ¡El serializer corregido funciona perfectamente!")
        print("✅ Las imágenes se suben a Cloudinary")
        print("✅ La configuración de CORS está correcta")
        print("✅ La API funciona con Cloudinary")
    elif config_ok and cors_ok:
        print("✅ La configuración está correcta")
        print("⚠️ Pero hay problemas con la API")
    elif config_ok:
        print("⚠️ La configuración básica está bien")
        print("❌ Pero hay problemas con CORS")
    else:
        print("❌ Hay problemas con la configuración")
        print("🔧 Revisar configuración de Cloudinary y CORS")
    
    print("\n💡 RECOMENDACIONES:")
    print("1. Verificar que las variables de entorno estén configuradas en Render")
    print("2. Asegurar que CORS_ALLOWED_ORIGINS incluya todos los orígenes necesarios")
    print("3. Verificar que el serializer esté usando Cloudinary correctamente")

if __name__ == '__main__':
    main() 