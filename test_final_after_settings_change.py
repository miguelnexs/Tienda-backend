#!/usr/bin/env python
"""
Script para probar la configuración después del cambio de DJANGO_SETTINGS_MODULE
"""
import os
import sys
import django
import requests
import json
import time
from pathlib import Path

def test_render_api_after_settings_change():
    """Probar la API de Render después del cambio de configuración"""
    
    print("🎯 PRUEBA DESPUÉS DEL CAMBIO DE CONFIGURACIÓN")
    print("="*60)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # 1. Probar obtener categorías existentes
        print("📋 1. Probando obtener categorías existentes...")
        url = f"{RENDER_API_URL}/categorias/"
        
        response = requests.get(url, timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                categorias = response.json()
                print(f"✅ Se obtuvieron {len(categorias)} categorías")
                
                # Verificar si hay imágenes en Cloudinary
                cloudinary_images = 0
                local_images = 0
                
                for categoria in categorias:
                    if isinstance(categoria, dict) and categoria.get('imagen_url'):
                        if 'cloudinary.com' in categoria['imagen_url']:
                            cloudinary_images += 1
                        elif 'onrender.com/media' in categoria['imagen_url']:
                            local_images += 1
                
                print(f"☁️ Imágenes en Cloudinary: {cloudinary_images}")
                print(f"📁 Imágenes locales: {local_images}")
                
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                print(f"📊 Response Text: {response.text[:200]}...")
                return False
            
        else:
            print(f"❌ Error obteniendo categorías: {response.status_code}")
            print(f"📊 Response: {response.text}")
            return False
        
        # 2. Crear una nueva categoría para probar
        print("\n📋 2. Probando crear nueva categoría...")
        
        # Buscar imagen de prueba
        imagen_path = Path("D:/usuario/Downloads/bolso/cartera-casual-para-mujer-23064.jpg")
        if not imagen_path.exists():
            print("❌ No se encontró la imagen de prueba")
            return False
        
        print(f"📁 Imagen encontrada: {imagen_path}")
        
        # Preparar datos
        data = {
            'nombre': 'Test After Settings Change',
            'descripcion': 'Prueba después del cambio de configuración',
            'activa': True,
            'orden': 990
        }
        
        # Preparar archivo
        files = {
            'imagen': ('cartera-casual-para-mujer-23064.jpg', open(imagen_path, 'rb'), 'image/jpeg')
        }
        
        # Crear categoría
        response = requests.post(
            f"{RENDER_API_URL}/categorias/",
            data=data,
            files=files,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 201:
            try:
                categoria = response.json()
                print("✅ ¡Categoría creada exitosamente!")
                print(f"📸 ID: {categoria['id']}")
                print(f"🏷️ Nombre: {categoria['nombre']}")
                print(f"🔗 URL de la imagen: {categoria['imagen_url']}")
                
                # Verificar si se subió a Cloudinary
                if 'cloudinary.com' in categoria['imagen_url']:
                    print("☁️ ¡EXCELENTE! La imagen se subió a Cloudinary")
                    return True
                else:
                    print("📁 La imagen se guardó localmente")
                    return False
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                print(f"📊 Response Text: {response.text}")
                return False
        else:
            print(f"❌ Error creando categoría: {response.status_code}")
            print(f"📊 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: La petición tardó demasiado")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión durante la petición")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_database_connection():
    """Probar conexión a base de datos"""
    
    print("\n" + "="*60)
    print("🗄️ PROBANDO CONEXIÓN A BASE DE DATOS")
    print("="*60)
    
    try:
        # Simular entorno de Render
        os.environ['RENDER'] = 'true'
        os.environ['DJANGO_SETTINGS_MODULE'] = 'Backend.render_settings'
        
        # Configurar DATABASE_URL para pruebas locales
        if not os.environ.get('DATABASE_URL'):
            os.environ['DATABASE_URL'] = 'postgresql://tienda_user:PWKuO99372EAcsyx5KpHlV9VBIQJkvle@dpg-d278j5u3jp1c73en5gbg-a.ohio-postgres.render.com/tienda_production'
        
        # Configurar Django
        django.setup()
        
        from django.conf import settings
        from django.db import connection
        
        print("📋 Configuración de base de datos:")
        print(f"  ENGINE: {settings.DATABASES['default']['ENGINE']}")
        print(f"  NAME: {settings.DATABASES['default']['NAME']}")
        print(f"  HOST: {settings.DATABASES['default']['HOST']}")
        
        # Probar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Conexión exitosa a PostgreSQL: {version[0]}")
            return True
            
    except Exception as e:
        print(f"❌ Error de conexión a base de datos: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 PRUEBA DESPUÉS DEL CAMBIO DE DJANGO_SETTINGS_MODULE")
    print("="*60)
    
    # Probar conexión a base de datos
    db_ok = test_database_connection()
    
    # Probar API
    api_ok = test_render_api_after_settings_change()
    
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL")
    print("="*60)
    print(f"✅ Conexión a base de datos: {'EXITOSA' if db_ok else 'FALLIDA'}")
    print(f"✅ API con nueva configuración: {'EXITOSA' if api_ok else 'FALLIDA'}")
    
    # Conclusión
    print("\n" + "="*60)
    print("🎯 CONCLUSIÓN")
    print("="*60)
    
    if db_ok and api_ok:
        print("🎉 ¡PERFECTO! La configuración está funcionando correctamente")
        print("✅ La base de datos está conectada")
        print("✅ Las imágenes se suben a Cloudinary")
        print("✅ El servicio está usando render_settings.py")
    elif db_ok:
        print("✅ La base de datos está conectada")
        print("⚠️ Pero las imágenes aún se guardan localmente")
        print("🔧 Verificar que el servicio se haya reiniciado completamente")
    else:
        print("❌ Hay problemas con la base de datos")
        print("🔧 Revisar configuración de DATABASE_URL")
    
    print("\n💡 RECOMENDACIONES:")
    if not api_ok:
        print("1. Esperar unos minutos más para que el servicio se reinicie completamente")
        print("2. Verificar en los logs de Render que no hay errores")
        print("3. Intentar crear otra categoría para confirmar")
    else:
        print("1. ¡Todo está funcionando perfectamente!")
        print("2. Las nuevas imágenes se subirán a Cloudinary")
        print("3. El servicio está configurado correctamente")

if __name__ == '__main__':
    main() 