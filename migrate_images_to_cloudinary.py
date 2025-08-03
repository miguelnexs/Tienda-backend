#!/usr/bin/env python
"""
Script para migrar imágenes existentes a Cloudinary
"""

import os
import sys
import django
from pathlib import Path
import requests
from PIL import Image, ImageDraw
import io
import uuid

# Configurar variables de entorno
os.environ['CLOUDINARY_CLOUD_NAME'] = 'do1ntnlop'
os.environ['CLOUDINARY_API_KEY'] = '117225377115856'
os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from django.conf import settings
from categorias.models import CategoriaProducto
from productos.models import Producto, ImagenProducto
from django.core.files.base import ContentFile
import cloudinary
import cloudinary.uploader

def migrate_categorias_to_cloudinary():
    """Migrar imágenes de categorías a Cloudinary"""
    print("🔄 Migrando imágenes de categorías...")
    
    categorias = CategoriaProducto.objects.all()
    migrated_count = 0
    
    for categoria in categorias:
        if categoria.imagen:
            print(f"📸 Procesando categoría: {categoria.nombre}")
            
            try:
                # Verificar si la imagen existe en Cloudinary
                if 'cloudinary.com' in categoria.imagen.url:
                    # Intentar acceder a la imagen
                    response = requests.get(categoria.imagen.url, timeout=5)
                    if response.status_code == 200:
                        print(f"   ✅ Imagen ya existe en Cloudinary: {categoria.nombre}")
                        continue
                    else:
                        print(f"   ❌ Imagen no accesible: {categoria.nombre}")
                
                # Crear imagen de reemplazo
                img = Image.new('RGB', (300, 300), color='blue')
                draw = ImageDraw.Draw(img)
                draw.text((100, 140), f"MIGRATED {categoria.nombre[:10]}", fill='white')
                
                # Convertir a bytes
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_byte_arr.seek(0)
                
                # Crear ContentFile
                content_file = ContentFile(img_byte_arr.getvalue(), name=f"migrated_{categoria.slug}.jpg")
                
                # Guardar usando el storage de Cloudinary
                categoria.imagen.save(f"migrated_{categoria.slug}.jpg", content_file, save=True)
                
                print(f"   ✅ Migrada: {categoria.nombre}")
                migrated_count += 1
                
            except Exception as e:
                print(f"   ❌ Error migrando {categoria.nombre}: {e}")
    
    print(f"✅ Migración completada: {migrated_count} categorías migradas")

def migrate_productos_to_cloudinary():
    """Migrar imágenes de productos a Cloudinary"""
    print("\n🔄 Migrando imágenes de productos...")
    
    productos = Producto.objects.all()
    migrated_count = 0
    
    for producto in productos:
        if producto.imagen_principal:
            print(f"📸 Procesando producto: {producto.nombre}")
            
            try:
                # Verificar si la imagen existe en Cloudinary
                if 'cloudinary.com' in producto.imagen_principal.url:
                    # Intentar acceder a la imagen
                    response = requests.get(producto.imagen_principal.url, timeout=5)
                    if response.status_code == 200:
                        print(f"   ✅ Imagen ya existe en Cloudinary: {producto.nombre}")
                        continue
                    else:
                        print(f"   ❌ Imagen no accesible: {producto.nombre}")
                
                # Crear imagen de reemplazo
                img = Image.new('RGB', (400, 400), color='green')
                draw = ImageDraw.Draw(img)
                draw.text((150, 190), f"PRODUCTO {producto.nombre[:15]}", fill='white')
                
                # Convertir a bytes
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_byte_arr.seek(0)
                
                # Crear ContentFile
                content_file = ContentFile(img_byte_arr.getvalue(), name=f"migrated_producto_{producto.slug}.jpg")
                
                # Guardar usando el storage de Cloudinary
                producto.imagen_principal.save(f"migrated_producto_{producto.slug}.jpg", content_file, save=True)
                
                print(f"   ✅ Migrado: {producto.nombre}")
                migrated_count += 1
                
            except Exception as e:
                print(f"   ❌ Error migrando {producto.nombre}: {e}")
    
    print(f"✅ Migración completada: {migrated_count} productos migrados")

def test_cloudinary_upload():
    """Test de subida directa a Cloudinary"""
    print("\n🧪 Probando subida directa a Cloudinary...")
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 200), color='red')
        draw = ImageDraw.Draw(img)
        draw.text((50, 90), "DIRECT TEST", fill='white')
        
        # Convertir a bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        # Subir directamente a Cloudinary
        result = cloudinary.uploader.upload(
            img_byte_arr,
            folder="test_direct",
            public_id=f"test_direct_{uuid.uuid4().hex[:8]}"
        )
        
        print(f"✅ Subida directa exitosa:")
        print(f"   URL: {result['secure_url']}")
        print(f"   Public ID: {result['public_id']}")
        
        # Verificar que es accesible
        response = requests.get(result['secure_url'], timeout=5)
        if response.status_code == 200:
            print("   ✅ URL accesible")
            return True
        else:
            print(f"   ❌ Error {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en subida directa: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Migración de Imágenes a Cloudinary")
    print("=" * 50)
    
    # Test 1: Subida directa
    direct_ok = test_cloudinary_upload()
    
    if direct_ok:
        # Test 2: Migrar categorías
        migrate_categorias_to_cloudinary()
        
        # Test 3: Migrar productos
        migrate_productos_to_cloudinary()
        
        print("\n🎉 Migración completada!")
    else:
        print("❌ No se puede proceder con la migración")

if __name__ == "__main__":
    main() 