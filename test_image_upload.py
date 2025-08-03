#!/usr/bin/env python3
"""
Script de prueba para verificar la subida de imágenes a Cloudinary
"""

import os
import sys
import django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from productos.models import Producto, ColorProducto, ImagenProducto
from productos.serializers.color import ImagenProductoSerializer


def test_cloudinary_configuration():
    """Prueba la configuración de Cloudinary"""
    print("=== PRUEBA DE CONFIGURACIÓN DE CLOUDINARY ===")
    
    # Verificar variables de entorno
    cloudinary_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
    cloudinary_key = os.environ.get('CLOUDINARY_API_KEY')
    cloudinary_secret = os.environ.get('CLOUDINARY_API_SECRET')
    
    print(f"CLOUDINARY_CLOUD_NAME: {'✅ Configurado' if cloudinary_name else '❌ No configurado'}")
    print(f"CLOUDINARY_API_KEY: {'✅ Configurado' if cloudinary_key else '❌ No configurado'}")
    print(f"CLOUDINARY_API_SECRET: {'✅ Configurado' if cloudinary_secret else '❌ No configurado'}")
    
    # Verificar configuración de Django
    print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    print(f"CLOUDINARY_STORAGE: {'✅ Configurado' if hasattr(settings, 'CLOUDINARY_STORAGE') else '❌ No configurado'}")
    
    # Verificar si estamos en producción
    render_env = 'RENDER' in os.environ
    print(f"Entorno RENDER: {'✅ Sí' if render_env else '❌ No'}")
    
    return all([cloudinary_name, cloudinary_key, cloudinary_secret])


def test_image_upload():
    """Prueba la subida de una imagen de prueba"""
    print("\n=== PRUEBA DE SUBIDA DE IMAGEN ===")
    
    try:
        # Crear un producto de prueba
        producto, created = Producto.objects.get_or_create(
            sku='TEST-001',
            defaults={
                'nombre': 'Producto de Prueba',
                'slug': 'producto-prueba',
                'descripcion_corta': 'Producto para pruebas',
                'descripcion_larga': 'Producto de prueba para verificar subida de imágenes',
                'precio': 100.00,
                'costo': 50.00,
                'stock': 10
            }
        )
        
        # Crear un color de prueba
        color, created = ColorProducto.objects.get_or_create(
            producto=producto,
            nombre='Rojo',
            defaults={
                'hex_code': '#FF0000',
                'stock': 5
            }
        )
        
        # Crear una imagen de prueba (1x1 pixel PNG)
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf6\x178\x00\x00\x00\x00IEND\xaeB`\x82'
        
        imagen_archivo = SimpleUploadedFile(
            'test_image.png',
            png_data,
            content_type='image/png'
        )
        
        # Crear la imagen en la base de datos
        imagen = ImagenProducto.objects.create(
            color=color,
            imagen=imagen_archivo,
            orden=1,
            es_principal=True
        )
        
        print(f"✅ Imagen creada exitosamente: {imagen.id}")
        print(f"📁 Ruta de la imagen: {imagen.imagen.name}")
        print(f"🌐 URL de la imagen: {imagen.imagen.url}")
        
        # Probar el serializador
        serializer = ImagenProductoSerializer(imagen, context={'request': None})
        data = serializer.data
        print(f"📊 Datos del serializador: {data}")
        
        # Limpiar
        imagen.delete()
        color.delete()
        producto.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba de subida: {e}")
        return False


def main():
    """Función principal"""
    print("🔍 INICIANDO PRUEBAS DE SUBIDA DE IMÁGENES")
    
    # Prueba 1: Configuración de Cloudinary
    cloudinary_ok = test_cloudinary_configuration()
    
    # Prueba 2: Subida de imagen
    upload_ok = test_image_upload()
    
    print("\n=== RESULTADOS ===")
    print(f"Configuración Cloudinary: {'✅ OK' if cloudinary_ok else '❌ ERROR'}")
    print(f"Subida de imagen: {'✅ OK' if upload_ok else '❌ ERROR'}")
    
    if cloudinary_ok and upload_ok:
        print("\n🎉 Todas las pruebas pasaron exitosamente!")
        return 0
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa la configuración.")
        return 1


if __name__ == '__main__':
    sys.exit(main()) 