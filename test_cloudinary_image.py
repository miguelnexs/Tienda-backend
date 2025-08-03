#!/usr/bin/env python
"""
Script para probar Cloudinary con imagen real
"""

import os
import sys
import django
from pathlib import Path

# Configurar variables de entorno ANTES de importar Django
os.environ['CLOUDINARY_CLOUD_NAME'] = 'do1ntnlop'
os.environ['CLOUDINARY_API_KEY'] = '117225377115856'
os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from cloudinary_storage.storage import MediaCloudinaryStorage
from django.core.files.base import ContentFile

def test_cloudinary_image():
    """Probar Cloudinary con imagen real"""
    print("🖼️  Probando Cloudinary con imagen real...")
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\0fbfa4d6-958d-42c1-9db7-8c87784d28e6.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ La imagen no existe en: {image_path}")
        return
    
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        print(f"✅ Imagen leída: {len(image_data)} bytes")
    except Exception as e:
        print(f"❌ Error leyendo imagen: {e}")
        return
    
    # Crear instancia de Cloudinary storage
    cloudinary_storage = MediaCloudinaryStorage()
    print(f"✅ Cloudinary storage creado: {cloudinary_storage}")
    
    # Crear archivo de imagen
    image_file = ContentFile(image_data)
    
    try:
        # Subir imagen
        file_path = cloudinary_storage.save('test_bolso.jpg', image_file)
        print(f"✅ Imagen subida: {file_path}")
        
        # Obtener URL
        file_url = cloudinary_storage.url(file_path)
        print(f"🌐 URL de la imagen: {file_url}")
        
        if 'cloudinary.com' in file_url:
            print("✅ ¡Imagen subida a Cloudinary correctamente!")
            print(f"🔗 URL completa: {file_url}")
        else:
            print("⚠️  URL local detectada")
            
        # Limpiar
        cloudinary_storage.delete(file_path)
        print("🗑️  Imagen eliminada")
        
        return file_url
        
    except Exception as e:
        print(f"❌ Error subiendo imagen: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_product_with_cloudinary():
    """Probar creación de producto con Cloudinary"""
    print("\n📦 Probando creación de producto con Cloudinary...")
    
    from productos.models import Producto
    import uuid
    
    # Crear datos únicos
    unique_id = str(uuid.uuid4())[:8]
    
    # Crear producto
    producto = Producto.objects.create(
        nombre=f'Bolso Cloudinary Final {unique_id}',
        sku=f'BOLSO-FINAL-{unique_id}',
        slug=f'bolso-cloudinary-final-{unique_id}',
        precio='45.99',
        descripcion_corta='Bolso final de prueba con Cloudinary',
        descripcion_larga='Este es el bolso final de prueba para verificar que Cloudinary funciona correctamente.',
        tipo='fisico',
        estado='publicado',
        gestion_stock=True,
        stock=20,
        costo='25.00'
    )
    
    print(f"✅ Producto creado: {producto.nombre} (ID: {producto.id})")
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\0fbfa4d6-958d-42c1-9db7-8c87784d28e6.jpg"
    
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # Subir imagen usando Cloudinary storage directamente
        cloudinary_storage = MediaCloudinaryStorage()
        image_file = ContentFile(image_data)
        
        # Subir imagen
        file_path = cloudinary_storage.save(f'productos/bolso_{unique_id}.jpg', image_file)
        print(f"✅ Imagen subida a Cloudinary: {file_path}")
        
        # Asignar al producto
        producto.imagen_principal.name = file_path
        producto.save()
        
        print(f"✅ Imagen asignada al producto: {producto.imagen_principal.name}")
        
        # Obtener URL
        image_url = producto.imagen_principal.url
        print(f"🌐 URL de la imagen: {image_url}")
        
        if 'cloudinary.com' in image_url:
            print("✅ ¡Producto con imagen en Cloudinary!")
            print(f"🔗 URL completa: {image_url}")
        else:
            print("⚠️  URL local detectada")
        
        return producto
        
    except Exception as e:
        print(f"❌ Error procesando imagen: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Probar imagen directa
    image_url = test_cloudinary_image()
    
    # Probar producto
    producto = test_product_with_cloudinary() 