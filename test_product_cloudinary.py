#!/usr/bin/env python
"""
Script para probar la subida de producto con Cloudinary forzado
"""

import os
import sys
import django
from pathlib import Path
import uuid

# Forzar variables de entorno de Cloudinary
os.environ['CLOUDINARY_CLOUD_NAME'] = 'do1ntnlop'
os.environ['CLOUDINARY_API_KEY'] = '117225377115856'
os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from django.conf import settings
from productos.models import Producto
from django.core.files.base import ContentFile
import cloudinary

def test_product_upload_cloudinary():
    """Prueba la subida de un producto con Cloudinary forzado"""
    print("🧪 Probando subida de producto con Cloudinary...")
    
    # Verificar configuración
    print(f"🔧 DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\0fbfa4d6-958d-42c1-9db7-8c87784d28e6.jpg"
    
    # Verificar que la imagen existe
    if not os.path.exists(image_path):
        print(f"❌ La imagen no existe en: {image_path}")
        return
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    # Leer la imagen
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        print(f"✅ Imagen leída: {len(image_data)} bytes")
    except Exception as e:
        print(f"❌ Error leyendo imagen: {e}")
        return
    
    # Crear un producto de prueba con slug único
    unique_id = str(uuid.uuid4())[:8]
    product_data = {
        'nombre': f'Bolso Cloudinary Test {unique_id}',
        'sku': f'BOLSO-CLOUD-{unique_id}',
        'slug': f'bolso-cloudinary-test-{unique_id}',
        'precio': '35.99',
        'descripcion_corta': 'Bolso de prueba con Cloudinary forzado',
        'descripcion_larga': 'Este es un bolso de prueba para verificar que Cloudinary funciona correctamente cuando se fuerza en desarrollo.',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 15,
        'costo': '18.00'
    }
    
    print("📦 Datos del producto:")
    for key, value in product_data.items():
        print(f"   {key}: {value}")
    
    # Simular la subida usando la API de Django
    try:
        # Crear el producto
        producto = Producto.objects.create(
            nombre=product_data['nombre'],
            sku=product_data['sku'],
            slug=product_data['slug'],
            precio=product_data['precio'],
            descripcion_corta=product_data['descripcion_corta'],
            descripcion_larga=product_data['descripcion_larga'],
            tipo=product_data['tipo'],
            estado=product_data['estado'],
            gestion_stock=product_data['gestion_stock'],
            stock=product_data['stock'],
            costo=product_data['costo']
        )
        
        print(f"✅ Producto creado: {producto.nombre} (ID: {producto.id})")
        
        # Subir la imagen
        image_name = os.path.basename(image_path)
        producto.imagen_principal.save(image_name, ContentFile(image_data), save=True)
        
        print(f"✅ Imagen subida: {producto.imagen_principal.name}")
        
        # Obtener la URL de la imagen
        if producto.imagen_principal:
            image_url = producto.imagen_principal.url
            print(f"🌐 URL de la imagen: {image_url}")
            
            # Verificar si es una URL de Cloudinary
            if 'cloudinary.com' in image_url:
                print("✅ ¡La imagen se subió a Cloudinary correctamente!")
                print(f"🔗 URL completa: {image_url}")
            else:
                print("⚠️  La imagen se guardó localmente")
                print(f"🔗 URL local: {image_url}")
        
        return producto
        
    except Exception as e:
        print(f"❌ Error creando producto: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    producto = test_product_upload_cloudinary() 