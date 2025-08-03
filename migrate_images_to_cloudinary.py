#!/usr/bin/env python
"""
Script para migrar imágenes existentes a Cloudinary
Ejecutar solo después de configurar Cloudinary correctamente
"""

import os
import sys
import django
from pathlib import Path
from django.core.files.base import ContentFile
import cloudinary.uploader

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from productos.models import Producto, ImagenProducto
from django.conf import settings

def migrate_images_to_cloudinary():
    """Migra imágenes existentes a Cloudinary"""
    print("🔄 Iniciando migración de imágenes a Cloudinary...")
    
    # Verificar que estamos en producción
    if 'RENDER' not in os.environ:
        print("❌ Este script debe ejecutarse en producción (Render)")
        return
    
    # Verificar configuración de Cloudinary
    if not all([
        os.environ.get('CLOUDINARY_CLOUD_NAME'),
        os.environ.get('CLOUDINARY_API_KEY'),
        os.environ.get('CLOUDINARY_API_SECRET')
    ]):
        print("❌ Variables de entorno de Cloudinary no configuradas")
        return
    
    # Migrar imágenes principales de productos
    productos = Producto.objects.filter(imagen_principal__isnull=False)
    print(f"📦 Encontrados {productos.count()} productos con imágenes principales")
    
    for producto in productos:
        try:
            if producto.imagen_principal and hasattr(producto.imagen_principal, 'path'):
                print(f"📤 Migrando imagen de {producto.nombre}...")
                
                # Leer el archivo
                with open(producto.imagen_principal.path, 'rb') as f:
                    file_content = f.read()
                
                # Subir a Cloudinary
                result = cloudinary.uploader.upload(
                    file_content,
                    folder="productos",
                    public_id=f"producto_{producto.id}",
                    overwrite=True
                )
                
                # Actualizar el modelo
                producto.imagen_principal.name = result['public_id']
                producto.save()
                
                print(f"✅ {producto.nombre} migrado exitosamente")
                
        except Exception as e:
            print(f"❌ Error migrando {producto.nombre}: {e}")
    
    # Migrar imágenes de colores
    imagenes = ImagenProducto.objects.all()
    print(f"🎨 Encontradas {imagenes.count()} imágenes de colores")
    
    for imagen in imagenes:
        try:
            if imagen.imagen and hasattr(imagen.imagen, 'path'):
                print(f"📤 Migrando imagen de color {imagen.color.nombre}...")
                
                # Leer el archivo
                with open(imagen.imagen.path, 'rb') as f:
                    file_content = f.read()
                
                # Subir a Cloudinary
                result = cloudinary.uploader.upload(
                    file_content,
                    folder="productos/colores",
                    public_id=f"color_{imagen.color.id}_{imagen.id}",
                    overwrite=True
                )
                
                # Actualizar el modelo
                imagen.imagen.name = result['public_id']
                imagen.save()
                
                print(f"✅ Imagen de color {imagen.color.nombre} migrada")
                
        except Exception as e:
            print(f"❌ Error migrando imagen de color: {e}")
    
    print("🎉 Migración completada!")

if __name__ == "__main__":
    migrate_images_to_cloudinary() 