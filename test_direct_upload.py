#!/usr/bin/env python
"""
Script para simular la subida directamente usando Django
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

from django.core.files.base import ContentFile
from productos.models import Producto
from productos.serializers.producto import ProductoSerializer
from rest_framework.test import APIRequestFactory
import uuid

def simulate_frontend_upload_direct():
    """Simular la subida directamente usando Django"""
    print("🎯 Simulando subida directamente con Django...")
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\0fbfa4d6-958d-42c1-9db7-8c87784d28e6.jpg"
    
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
    
    # Crear datos únicos
    unique_id = str(uuid.uuid4())[:8]
    
    # Datos del producto (como los enviaría el frontend)
    product_data = {
        'nombre': f'Bolso Django Test {unique_id}',
        'sku': f'BOLSO-DJANGO-{unique_id}',
        'slug': f'bolso-django-test-{unique_id}',
        'precio': '59.99',
        'descripcion_corta': 'Bolso de prueba con Django directo',
        'descripcion_larga': 'Este es un bolso de prueba subido directamente con Django para verificar que Cloudinary funciona correctamente.',
        'tipo': 'fisico',
        'estado': 'publicado',
        'gestion_stock': True,
        'stock': 30,
        'costo': '35.00'
    }
    
    print("📦 Datos del producto:")
    for key, value in product_data.items():
        print(f"   {key}: {value}")
    
    try:
        # Crear el producto usando el modelo directamente
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
        image_name = f'bolso_django_{unique_id}.jpg'
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
        
        # Simular la respuesta del serializer
        factory = APIRequestFactory()
        request = factory.get('/')
        
        # Usar el serializer para obtener la respuesta como la API
        serializer = ProductoSerializer(producto, context={'request': request})
        serialized_data = serializer.data
        
        print(f"\n📄 Respuesta del serializer:")
        print(f"   ID: {serialized_data.get('id')}")
        print(f"   Nombre: {serialized_data.get('nombre')}")
        print(f"   SKU: {serialized_data.get('sku')}")
        print(f"   URL de imagen: {serialized_data.get('imagen_principal_url')}")
        
        return producto
        
    except Exception as e:
        print(f"❌ Error creando producto: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_existing_products():
    """Probar productos existentes"""
    print("\n🔍 Probando productos existentes...")
    
    try:
        # Obtener productos existentes
        productos = Producto.objects.all()[:5]
        
        print(f"✅ Productos encontrados: {productos.count()}")
        
        for producto in productos:
            print(f"\n📦 Producto: {producto.nombre}")
            print(f"   ID: {producto.id}")
            print(f"   SKU: {producto.sku}")
            
            if producto.imagen_principal:
                image_url = producto.imagen_principal.url
                print(f"   URL de imagen: {image_url}")
                
                # Verificar si la URL es de Cloudinary
                if 'cloudinary.com' in image_url:
                    print("   ✅ ¡URL de Cloudinary detectada!")
                else:
                    print("   ⚠️  URL local detectada")
            else:
                print("   ❌ Sin imagen")
                
    except Exception as e:
        print(f"❌ Error obteniendo productos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Simular subida directa
    producto = simulate_frontend_upload_direct()
    
    # Probar productos existentes
    test_existing_products() 