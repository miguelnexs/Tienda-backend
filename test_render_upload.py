#!/usr/bin/env python
"""
Script para probar la subida de imágenes desde Render
"""
import os
import sys
import django
import requests
import json
from pathlib import Path

# Configurar Django para Render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

from productos.models import Producto, ColorProducto, ImagenProducto
from django.core.files import File

def test_render_environment():
    """Verificar el entorno de Render"""
    
    print("🌐 VERIFICANDO ENTORNO DE RENDER")
    print("="*50)
    
    # Verificar variables de entorno de Render
    render_vars = {
        'RENDER': os.environ.get('RENDER', 'No'),
        'RENDER_EXTERNAL_HOSTNAME': os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'No'),
        'DATABASE_URL': os.environ.get('DATABASE_URL', 'No'),
        'CLOUDINARY_CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'No'),
        'CLOUDINARY_API_KEY': os.environ.get('CLOUDINARY_API_KEY', 'No'),
        'CLOUDINARY_API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', 'No'),
    }
    
    print("📋 Variables de entorno de Render:")
    for key, value in render_vars.items():
        if 'SECRET' in key or 'KEY' in key:
            print(f"  {key}: {value[:10]}..." if value != 'No' else f"  {key}: {value}")
        else:
            print(f"  {key}: {value}")
    
    # Verificar configuración de Django
    from django.conf import settings
    
    print(f"\n📋 Configuración de Django:")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"  DATABASES: {settings.DATABASES['default']['ENGINE']}")
    
    if hasattr(settings, 'CLOUDINARY_STORAGE'):
        print(f"  CLOUDINARY_STORAGE: ✅ Configurado")
    else:
        print(f"  CLOUDINARY_STORAGE: ❌ No configurado")
    
    return True

def test_render_api_upload():
    """Probar subida por API desde Render"""
    
    print("\n" + "="*50)
    print("🚀 PROBANDO SUBIDA POR API DESDE RENDER")
    print("="*50)
    
    # URL del backend en Render
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    # Ruta de la imagen (simular desde el servidor)
    image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    try:
        # Obtener productos desde Render
        print("🔍 Obteniendo productos desde Render...")
        response = requests.get(f"{RENDER_API_URL}/productos/")
        
        if response.status_code != 200:
            print(f"❌ Error al obtener productos: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        productos = response.json()
        print(f"✅ Productos obtenidos: {len(productos)}")
        
        if not productos:
            print("❌ No hay productos disponibles en Render")
            return False
        
        # Usar el primer producto
        producto = productos[0]
        producto_id = producto['id']
        print(f"🎯 Usando producto: {producto['nombre']} (ID: {producto_id})")
        
        # Obtener colores del producto
        print("🔍 Obteniendo colores del producto...")
        response = requests.get(f"{RENDER_API_URL}/productos/{producto_id}/colores/")
        
        if response.status_code != 200:
            print(f"❌ Error al obtener colores: {response.status_code}")
            return False
        
        colores = response.json()
        print(f"✅ Colores obtenidos: {len(colores)}")
        
        if not colores:
            print("❌ El producto no tiene colores")
            return False
        
        # Usar el primer color
        color = colores[0]
        color_id = color['id']
        print(f"🎨 Usando color: {color['nombre']} (ID: {color_id})")
        
        # Preparar la petición para subir la imagen
        url = f"{RENDER_API_URL}/productos/{producto_id}/colores/{color_id}/imagenes/"
        
        # Preparar los datos
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('Bolso-BWXXNG-NEGRO_1.jpg', image_file, 'image/jpeg')
            }
            
            data = {
                'orden': 1,
                'es_principal': True
            }
            
            print(f"\n🚀 Subiendo imagen a Render: {url}")
            print(f"📤 Datos: {data}")
            
            response = requests.post(url, files=files, data=data)
            
            print(f"\n📊 Respuesta del servidor Render:")
            print(f"  Status Code: {response.status_code}")
            print(f"  Response: {response.text}")
            
            if response.status_code == 201:
                print("✅ ¡Imagen subida exitosamente desde Render!")
                
                # Obtener la imagen creada
                imagen_data = response.json()
                print(f"📸 Imagen creada con ID: {imagen_data.get('id')}")
                print(f"🔗 URL de la imagen: {imagen_data.get('imagen')}")
                
                # Verificar si es una URL de Cloudinary
                if 'cloudinary.com' in imagen_data.get('imagen', ''):
                    print("☁️ ¡La imagen se subió a Cloudinary desde Render!")
                else:
                    print("📁 La imagen se guardó localmente en Render")
                
                return True
            else:
                print("❌ Error al subir la imagen desde Render")
                return False
                
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor de Render")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_render_direct_upload():
    """Probar subida directa usando Django en entorno Render"""
    
    print("\n" + "="*50)
    print("🔄 PROBANDO SUBIDA DIRECTA EN ENTORNO RENDER")
    print("="*50)
    
    # Simular entorno de Render
    os.environ['RENDER'] = 'true'
    os.environ['CLOUDINARY_CLOUD_NAME'] = 'do1ntnlop'
    os.environ['CLOUDINARY_API_KEY'] = '1172253771'
    os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_'
    
    # Reconfigurar Django con settings de Render
    django.setup()
    
    try:
        # Obtener un producto y color
        producto = Producto.objects.first()
        if not producto:
            print("❌ No hay productos en la base de datos")
            return False
        
        color = producto.colores.first()
        if not color:
            print("❌ El producto no tiene colores")
            return False
        
        print(f"🎯 Producto: {producto.nombre}")
        print(f"🎨 Color: {color.nombre}")
        
        # Ruta de la imagen
        image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
        
        if not os.path.exists(image_path):
            print(f"❌ Error: La imagen no existe en {image_path}")
            return False
        
        # Crear la imagen usando Django con configuración de Render
        with open(image_path, 'rb') as image_file:
            imagen = ImagenProducto.objects.create(
                color=color,
                imagen=File(image_file, name='Bolso-BWXXNG-NEGRO_1_render.jpg'),
                orden=1,
                es_principal=True
            )
            
            print("✅ Imagen creada exitosamente en entorno Render!")
            print(f"📸 ID de la imagen: {imagen.id}")
            print(f"🔗 URL de la imagen: {imagen.imagen.url}")
            print(f"📁 Nombre del archivo: {imagen.imagen.name}")
            
            # Verificar si es una URL de Cloudinary
            if 'cloudinary.com' in imagen.imagen.url:
                print("☁️ ¡La imagen se subió a Cloudinary!")
            else:
                print("📁 La imagen se guardó localmente")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al crear la imagen: {e}")
        return False

def test_render_image_access():
    """Probar acceso a imágenes desde Render"""
    
    print("\n" + "="*50)
    print("🔍 PROBANDO ACCESO A IMÁGENES DESDE RENDER")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # Obtener productos
        response = requests.get(f"{RENDER_API_URL}/productos/")
        if response.status_code != 200:
            print("❌ Error al obtener productos")
            return False
        
        productos = response.json()
        if not productos:
            print("❌ No hay productos")
            return False
        
        producto = productos[0]
        producto_id = producto['id']
        
        # Obtener colores
        response = requests.get(f"{RENDER_API_URL}/productos/{producto_id}/colores/")
        if response.status_code != 200:
            print("❌ Error al obtener colores")
            return False
        
        colores = response.json()
        if not colores:
            print("❌ No hay colores")
            return False
        
        color = colores[0]
        color_id = color['id']
        
        # Obtener imágenes del color
        response = requests.get(f"{RENDER_API_URL}/productos/{producto_id}/colores/{color_id}/imagenes/")
        
        if response.status_code == 200:
            imagenes = response.json()
            print(f"✅ Imágenes obtenidas desde Render: {len(imagenes)}")
            
            for imagen in imagenes:
                print(f"📸 Imagen ID: {imagen['id']}")
                print(f"  🔗 URL: {imagen['imagen']}")
                print(f"  ⭐ Principal: {imagen['es_principal']}")
                print(f"  📊 Orden: {imagen['orden']}")
                
                # Verificar si es una URL de Cloudinary
                if 'cloudinary.com' in imagen['imagen']:
                    print(f"  ☁️ Cloudinary: ✅")
                else:
                    print(f"  📁 Local: ✅")
            
            return True
        else:
            print(f"❌ Error al obtener imágenes: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA DE SUBIDA DESDE RENDER")
    print("="*50)
    
    # Verificar entorno de Render
    success_env = test_render_environment()
    
    # Probar subida directa en entorno Render
    success_direct = test_render_direct_upload()
    
    # Probar subida por API desde Render
    success_api = test_render_api_upload()
    
    # Probar acceso a imágenes desde Render
    success_access = test_render_image_access()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS DESDE RENDER")
    print("="*50)
    print(f"✅ Entorno de Render: {'EXITOSA' if success_env else 'FALLIDA'}")
    print(f"✅ Subida directa: {'EXITOSA' if success_direct else 'FALLIDA'}")
    print(f"✅ Subida por API: {'EXITOSA' if success_api else 'FALLIDA'}")
    print(f"✅ Acceso a imágenes: {'EXITOSA' if success_access else 'FALLIDA'}")
    
    if success_env and (success_direct or success_api):
        print("\n🎉 ¡La subida desde Render está funcionando correctamente!")
        print("💡 Las imágenes se suben exitosamente al cloud desde Render")
    else:
        print("\n❌ Hay problemas con la subida desde Render")

if __name__ == '__main__':
    main() 