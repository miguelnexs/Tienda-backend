#!/usr/bin/env python3
"""
Script para migrar imágenes existentes de Cloudinary a ImageKit.io
Ejecutar con: python migrate_to_imagekit.py
"""

import os
import sys
import django
import requests
from pathlib import Path
from urllib.parse import urlparse

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from productos.models import ImagenProducto, Producto
from categorias.models import CategoriaProducto

def print_header(title):
    """Imprimir encabezado formateado"""
    print(f"\n{'='*50}")
    print(f"🔄 {title}")
    print(f"{'='*50}")

def download_from_cloudinary(url):
    """Descargar imagen desde Cloudinary"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"❌ Error descargando {url}: {e}")
        return None

def upload_to_imagekit(image_data, filename):
    """Subir imagen a ImageKit"""
    try:
        content = ContentFile(image_data)
        content.name = filename
        
        # Subir usando el storage
        file_path = default_storage.save(filename, content)
        file_url = default_storage.url(file_path)
        
        print(f"✅ Subido: {filename}")
        return file_path, file_url
    except Exception as e:
        print(f"❌ Error subiendo {filename}: {e}")
        return None, None

def migrate_imagen_producto():
    """Migrar imágenes de productos"""
    print_header("MIGRACIÓN DE IMÁGENES DE PRODUCTOS")
    
    imagenes = ImagenProducto.objects.all()
    total = imagenes.count()
    migrated = 0
    failed = 0
    
    print(f"📊 Total de imágenes a migrar: {total}")
    
    for imagen in imagenes:
        try:
            # Obtener URL actual (Cloudinary)
            current_url = imagen.imagen.url
            
            # Verificar si ya es una URL de ImageKit
            if 'imagekit.io' in current_url:
                print(f"⏭️ Ya migrada: {imagen.imagen.name}")
                continue
            
            # Verificar si es una URL de Cloudinary
            if 'cloudinary.com' not in current_url:
                print(f"⚠️ URL no reconocida: {current_url}")
                continue
            
            # Descargar desde Cloudinary
            print(f"📥 Descargando: {current_url}")
            image_data = download_from_cloudinary(current_url)
            
            if not image_data:
                failed += 1
                continue
            
            # Generar nuevo nombre de archivo
            filename = f"productos/colores/{imagen.imagen.name.split('/')[-1]}"
            
            # Subir a ImageKit
            file_path, file_url = upload_to_imagekit(image_data, filename)
            
            if file_path and file_url:
                # Actualizar modelo
                imagen.imagen.name = file_path
                imagen.save()
                migrated += 1
                print(f"✅ Migrada: {filename}")
            else:
                failed += 1
                
        except Exception as e:
            print(f"❌ Error migrando imagen {imagen.id}: {e}")
            failed += 1
    
    print(f"\n📊 Resultados:")
    print(f"✅ Migradas: {migrated}")
    print(f"❌ Fallidas: {failed}")
    print(f"⏭️ Ya migradas: {total - migrated - failed}")

def migrate_producto_imagen_principal():
    """Migrar imágenes principales de productos"""
    print_header("MIGRACIÓN DE IMÁGENES PRINCIPALES")
    
    productos = Producto.objects.filter(imagen_principal__isnull=False)
    total = productos.count()
    migrated = 0
    failed = 0
    
    print(f"📊 Total de productos con imagen principal: {total}")
    
    for producto in productos:
        try:
            current_url = producto.imagen_principal.url
            
            # Verificar si ya es una URL de ImageKit
            if 'imagekit.io' in current_url:
                print(f"⏭️ Ya migrada: {producto.imagen_principal.name}")
                continue
            
            # Verificar si es una URL de Cloudinary
            if 'cloudinary.com' not in current_url:
                print(f"⚠️ URL no reconocida: {current_url}")
                continue
            
            # Descargar desde Cloudinary
            print(f"📥 Descargando: {current_url}")
            image_data = download_from_cloudinary(current_url)
            
            if not image_data:
                failed += 1
                continue
            
            # Generar nuevo nombre de archivo
            filename = f"productos/{producto.imagen_principal.name.split('/')[-1]}"
            
            # Subir a ImageKit
            file_path, file_url = upload_to_imagekit(image_data, filename)
            
            if file_path and file_url:
                # Actualizar modelo
                producto.imagen_principal.name = file_path
                producto.save()
                migrated += 1
                print(f"✅ Migrada: {filename}")
            else:
                failed += 1
                
        except Exception as e:
            print(f"❌ Error migrando producto {producto.id}: {e}")
            failed += 1
    
    print(f"\n📊 Resultados:")
    print(f"✅ Migradas: {migrated}")
    print(f"❌ Fallidas: {failed}")
    print(f"⏭️ Ya migradas: {total - migrated - failed}")

def migrate_categoria_imagenes():
    """Migrar imágenes de categorías"""
    print_header("MIGRACIÓN DE IMÁGENES DE CATEGORÍAS")
    
    categorias = CategoriaProducto.objects.filter(imagen__isnull=False)
    total = categorias.count()
    migrated = 0
    failed = 0
    
    print(f"📊 Total de categorías con imagen: {total}")
    
    for categoria in categorias:
        try:
            current_url = categoria.imagen.url
            
            # Verificar si ya es una URL de ImageKit
            if 'imagekit.io' in current_url:
                print(f"⏭️ Ya migrada: {categoria.imagen.name}")
                continue
            
            # Verificar si es una URL de Cloudinary
            if 'cloudinary.com' not in current_url:
                print(f"⚠️ URL no reconocida: {current_url}")
                continue
            
            # Descargar desde Cloudinary
            print(f"📥 Descargando: {current_url}")
            image_data = download_from_cloudinary(current_url)
            
            if not image_data:
                failed += 1
                continue
            
            # Generar nuevo nombre de archivo
            filename = f"categorias/{categoria.imagen.name.split('/')[-1]}"
            
            # Subir a ImageKit
            file_path, file_url = upload_to_imagekit(image_data, filename)
            
            if file_path and file_url:
                # Actualizar modelo
                categoria.imagen.name = file_path
                categoria.save()
                migrated += 1
                print(f"✅ Migrada: {filename}")
            else:
                failed += 1
                
        except Exception as e:
            print(f"❌ Error migrando categoría {categoria.id}: {e}")
            failed += 1
    
    print(f"\n📊 Resultados:")
    print(f"✅ Migradas: {migrated}")
    print(f"❌ Fallidas: {failed}")
    print(f"⏭️ Ya migradas: {total - migrated - failed}")

def main():
    """Función principal"""
    print("🚀 MIGRACIÓN DE CLOUDINARY A IMAGEKIT.IO")
    print("="*50)
    
    # Verificar configuración
    if not os.environ.get('IMAGEKIT_PUBLIC_KEY'):
        print("❌ ERROR: IMAGEKIT_PUBLIC_KEY no configurada")
        return
    
    if not os.environ.get('IMAGEKIT_PRIVATE_KEY'):
        print("❌ ERROR: IMAGEKIT_PRIVATE_KEY no configurada")
        return
    
    if not os.environ.get('IMAGEKIT_URL_ENDPOINT'):
        print("❌ ERROR: IMAGEKIT_URL_ENDPOINT no configurada")
        return
    
    print("✅ Configuración verificada")
    
    # Ejecutar migraciones
    migrate_imagen_producto()
    migrate_producto_imagen_principal()
    migrate_categoria_imagenes()
    
    print("\n🎉 ¡MIGRACIÓN COMPLETADA!")
    print("Verifica que todas las imágenes se hayan migrado correctamente.")

if __name__ == "__main__":
    main() 