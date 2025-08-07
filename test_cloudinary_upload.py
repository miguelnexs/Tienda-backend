#!/usr/bin/env python
"""
Script para probar la subida de imagen directamente a Cloudinary
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

def test_cloudinary_upload():
    """Probar la subida directa a Cloudinary"""
    
    print("☁️ PROBANDO SUBIDA A CLOUDINARY")
    print("="*50)
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    # Verificar configuración de Cloudinary
    try:
        # Obtener configuración desde settings
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
        print("💡 Verifica que las variables de entorno estén configuradas")
        return False
    
    # Subir imagen directamente a Cloudinary
    try:
        print("\n🚀 Subiendo imagen a Cloudinary...")
        
        # Subir la imagen
        result = cloudinary.uploader.upload(
            image_path,
            folder="productos/colores",
            public_id="bolso-negro-test",
            overwrite=True,
            resource_type="image"
        )
        
        print("✅ Imagen subida exitosamente a Cloudinary!")
        print(f"📸 URL de la imagen: {result['secure_url']}")
        print(f"📁 Public ID: {result['public_id']}")
        print(f"📏 Tamaño: {result['bytes']} bytes")
        print(f"🖼️ Formato: {result['format']}")
        print(f"📐 Dimensiones: {result['width']}x{result['height']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error subiendo a Cloudinary: {e}")
        return False

def test_django_cloudinary_upload():
    """Probar la subida usando Django con Cloudinary"""
    
    print("\n" + "="*50)
    print("🔄 PROBANDO SUBIDA CON DJANGO + CLOUDINARY")
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
        image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
        
        if not os.path.exists(image_path):
            print(f"❌ Error: La imagen no existe en {image_path}")
            return False
        
        # Crear la imagen usando Django con Cloudinary
        with open(image_path, 'rb') as image_file:
            imagen = ImagenProducto.objects.create(
                color=color,
                imagen=File(image_file, name='Bolso-BWXXNG-NEGRO_1_cloudinary.jpg'),
                orden=3,
                es_principal=False
            )
            
            print("✅ Imagen creada exitosamente con Django + Cloudinary!")
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

def test_cloudinary_settings():
    """Verificar la configuración de Cloudinary en Django"""
    
    print("\n" + "="*50)
    print("🔧 VERIFICANDO CONFIGURACIÓN DE CLOUDINARY")
    print("="*50)
    
    try:
        from django.conf import settings
        
        print("📋 Configuración de Cloudinary:")
        print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        
        if hasattr(settings, 'CLOUDINARY_STORAGE'):
            print(f"  CLOUDINARY_STORAGE configurado: ✅")
            for key, value in settings.CLOUDINARY_STORAGE.items():
                if 'SECRET' in key or 'KEY' in key:
                    print(f"    {key}: {str(value)[:10]}...")
                else:
                    print(f"    {key}: {value}")
        else:
            print(f"  CLOUDINARY_STORAGE: ❌ No configurado")
        
        # Verificar si estamos en producción (Render)
        if 'RENDER' in os.environ:
            print("🌐 Entorno: PRODUCCIÓN (Render)")
            print("☁️ Cloudinary debería estar activo")
        else:
            print("💻 Entorno: DESARROLLO")
            print("📁 Almacenamiento local activo")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA DE SUBIDA A CLOUDINARY")
    print("="*50)
    
    # Verificar configuración
    success_config = test_cloudinary_settings()
    
    # Probar subida directa a Cloudinary
    cloudinary_result = test_cloudinary_upload()
    
    # Probar subida con Django + Cloudinary
    success_django = test_django_cloudinary_upload()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS CLOUDINARY")
    print("="*50)
    print(f"✅ Configuración: {'EXITOSA' if success_config else 'FALLIDA'}")
    print(f"✅ Subida directa a Cloudinary: {'EXITOSA' if cloudinary_result else 'FALLIDA'}")
    print(f"✅ Subida con Django: {'EXITOSA' if success_django else 'FALLIDA'}")
    
    if cloudinary_result:
        print(f"\n🔗 URL de la imagen en Cloudinary:")
        print(f"   {cloudinary_result['secure_url']}")
    
    if success_config and (cloudinary_result or success_django):
        print("\n🎉 ¡Cloudinary está funcionando correctamente!")
    else:
        print("\n❌ Hay problemas con la configuración de Cloudinary")

if __name__ == '__main__':
    main() 