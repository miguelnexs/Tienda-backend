#!/usr/bin/env python
"""
Script para migrar imágenes existentes a Cloudinary
Uso: python migrate_to_cloudinary.py
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from productos.models import Producto, ImagenProducto
import cloudinary.uploader
import cloudinary.api

def migrate_images_to_cloudinary():
    """
    Migra todas las imágenes existentes a Cloudinary
    """
    print("Iniciando migración de imágenes a Cloudinary...")
    
    # Migrar imágenes de productos principales
    productos = Producto.objects.filter(imagen_principal__isnull=False)
    print(f"Encontrados {productos.count()} productos con imagen principal")
    
    for producto in productos:
        if producto.imagen_principal:
            try:
                # Leer el archivo local
                with open(producto.imagen_principal.path, 'rb') as f:
                    file_content = f.read()
                
                # Subir a Cloudinary
                upload_result = cloudinary.uploader.upload(
                    file_content,
                    folder="productos",
                    public_id=f"producto_{producto.id}_principal",
                    overwrite=True
                )
                
                # Actualizar el modelo con la URL de Cloudinary
                producto.imagen_principal.name = upload_result['secure_url']
                producto.save()
                
                print(f"✅ Migrado: {producto.nombre} - {upload_result['secure_url']}")
                
            except Exception as e:
                print(f"❌ Error migrando {producto.nombre}: {str(e)}")
    
    # Migrar imágenes de colores de productos
    imagenes = ImagenProducto.objects.all()
    print(f"Encontradas {imagenes.count()} imágenes de colores")
    
    for imagen in imagenes:
        if imagen.imagen:
            try:
                # Leer el archivo local
                with open(imagen.imagen.path, 'rb') as f:
                    file_content = f.read()
                
                # Subir a Cloudinary
                upload_result = cloudinary.uploader.upload(
                    file_content,
                    folder="productos/colores",
                    public_id=f"color_{imagen.color.id}_imagen_{imagen.id}",
                    overwrite=True
                )
                
                # Actualizar el modelo con la URL de Cloudinary
                imagen.imagen.name = upload_result['secure_url']
                imagen.save()
                
                print(f"✅ Migrado: {imagen.color.producto.nombre} - {imagen.color.nombre} - {upload_result['secure_url']}")
                
            except Exception as e:
                print(f"❌ Error migrando imagen {imagen.id}: {str(e)}")
    
    print("Migración completada!")

if __name__ == '__main__':
    migrate_images_to_cloudinary() 