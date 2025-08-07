#!/usr/bin/env python
"""
Script para subir la imagen cartera-casual-para-mujer-23064.jpg al cloud
"""
import os
import sys
import django
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from productos.models import Producto, ColorProducto, ImagenProducto
from django.core.files import File

def upload_cartera_to_cloud():
    """Subir la imagen cartera al cloud"""
    
    print("👜 SUBIENDO CARTERA AL CLOUD")
    print("="*50)
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\cartera-casual-para-mujer-23064.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    # Verificar configuración de Cloudinary
    try:
        from django.conf import settings
        
        cloud_name = settings.CLOUDINARY['cloud_name']
        api_key = settings.CLOUDINARY['api_key']
        api_secret = settings.CLOUDINARY['api_secret']
        
        print(f"☁️ Cloudinary configurado:")
        print(f"  Cloud Name: {cloud_name}")
        print(f"  API Key: {api_key[:10]}...")
        print(f"  API Secret: {api_secret[:10]}...")
        
        # Configurar Cloudinary
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
    except Exception as e:
        print(f"❌ Error configurando Cloudinary: {e}")
        return False
    
    # Subir imagen directamente a Cloudinary
    try:
        print("\n🚀 Subiendo cartera a Cloudinary...")
        
        # Subir la imagen con metadatos específicos
        result = cloudinary.uploader.upload(
            image_path,
            folder="productos/colores",
            public_id="cartera-casual-mujer",
            overwrite=True,
            resource_type="image",
            transformation=[
                {"width": 800, "height": 800, "crop": "fill"},
                {"quality": "auto", "fetch_format": "auto"}
            ],
            tags=["cartera", "mujer", "casual", "accesorio"],
            context={
                "producto": "Cartera Casual para Mujer",
                "categoria": "Accesorios",
                "tipo": "Cartera"
            }
        )
        
        print("✅ Cartera subida exitosamente a Cloudinary!")
        print(f"📸 URL de la imagen: {result['secure_url']}")
        print(f"📁 Public ID: {result['public_id']}")
        print(f"📏 Tamaño: {result['bytes']} bytes")
        print(f"🖼️ Formato: {result['format']}")
        print(f"📐 Dimensiones: {result['width']}x{result['height']}")
        print(f"🏷️ Tags: {result.get('tags', [])}")
        print(f"📋 Context: {result.get('context', {})}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error subiendo a Cloudinary: {e}")
        return False

def upload_cartera_to_django():
    """Subir la cartera usando Django con Cloudinary"""
    
    print("\n" + "="*50)
    print("🔄 SUBIENDO CARTERA CON DJANGO + CLOUDINARY")
    print("="*50)
    
    # Obtener un producto y color
    try:
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
        image_path = r"D:\usuario\Downloads\bolso\cartera-casual-para-mujer-23064.jpg"
        
        if not os.path.exists(image_path):
            print(f"❌ Error: La imagen no existe en {image_path}")
            return False
        
        # Crear la imagen usando Django con Cloudinary
        with open(image_path, 'rb') as image_file:
            imagen = ImagenProducto.objects.create(
                color=color,
                imagen=File(image_file, name='cartera-casual-para-mujer-23064.jpg'),
                orden=4,
                es_principal=False
            )
            
            print("✅ Cartera creada exitosamente con Django + Cloudinary!")
            print(f"📸 ID de la imagen: {imagen.id}")
            print(f"🔗 URL de la imagen: {imagen.imagen.url}")
            print(f"📁 Nombre del archivo: {imagen.imagen.name}")
            
            # Verificar si es una URL de Cloudinary
            if 'cloudinary.com' in imagen.imagen.url:
                print("☁️ ¡La cartera se subió a Cloudinary!")
            else:
                print("📁 La cartera se guardó localmente")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al crear la imagen: {e}")
        return False

def test_multiple_cloudinary_uploads():
    """Probar múltiples subidas de la cartera a Cloudinary"""
    
    print("\n" + "="*50)
    print("🔄 MÚLTIPLES SUBIDAS DE CARTERA A CLOUDINARY")
    print("="*50)
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\cartera-casual-para-mujer-23064.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    uploads = []
    
    # Subir varias versiones de la cartera
    variations = [
        {"name": "original", "transformation": []},
        {"name": "thumbnail", "transformation": [{"width": 150, "height": 150, "crop": "fill"}]},
        {"name": "medium", "transformation": [{"width": 400, "height": 400, "crop": "fill"}]},
        {"name": "large", "transformation": [{"width": 800, "height": 800, "crop": "fill"}]},
        {"name": "webp", "transformation": [{"fetch_format": "webp", "quality": "auto"}]}
    ]
    
    for variation in variations:
        try:
            print(f"\n📸 Subiendo {variation['name']}...")
            
            result = cloudinary.uploader.upload(
                image_path,
                folder="productos/colores",
                public_id=f"cartera-casual-{variation['name']}",
                overwrite=True,
                resource_type="image",
                transformation=variation['transformation'],
                tags=["cartera", "mujer", "casual", variation['name']]
            )
            
            uploads.append({
                "name": variation['name'],
                "url": result['secure_url'],
                "public_id": result['public_id'],
                "size": result['bytes']
            })
            
            print(f"✅ {variation['name']} subido exitosamente!")
            print(f"   URL: {result['secure_url']}")
            print(f"   Tamaño: {result['bytes']} bytes")
            
        except Exception as e:
            print(f"❌ Error subiendo {variation['name']}: {e}")
    
    return uploads

def main():
    """Función principal"""
    print("🧪 SUBIDA DE CARTERA AL CLOUD")
    print("="*50)
    
    # Probar subida directa a Cloudinary
    cloudinary_result = upload_cartera_to_cloud()
    
    # Probar subida con Django + Cloudinary
    success_django = upload_cartera_to_django()
    
    # Probar múltiples subidas
    multiple_results = test_multiple_cloudinary_uploads()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE SUBIDA DE CARTERA")
    print("="*50)
    print(f"✅ Subida directa a Cloudinary: {'EXITOSA' if cloudinary_result else 'FALLIDA'}")
    print(f"✅ Subida con Django: {'EXITOSA' if success_django else 'FALLIDA'}")
    print(f"✅ Múltiples subidas: {'EXITOSA' if multiple_results else 'FALLIDA'}")
    
    if cloudinary_result:
        print(f"\n🔗 URL principal de la cartera:")
        print(f"   {cloudinary_result['secure_url']}")
    
    if multiple_results:
        print(f"\n📸 Variaciones de la cartera:")
        for upload in multiple_results:
            print(f"   {upload['name']}: {upload['url']}")
    
    if cloudinary_result or success_django:
        print("\n🎉 ¡La cartera se subió exitosamente al cloud!")
        print("💡 La imagen está disponible en Cloudinary")
    else:
        print("\n❌ Hay problemas con la subida de la cartera")

if __name__ == '__main__':
    main() 