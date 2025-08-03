#!/usr/bin/env python
"""
Script para forzar la configuración de Cloudinary y probarla
"""

import os
import sys
import django
from django.conf import settings

def force_cloudinary_config():
    """Forzar configuración de Cloudinary"""
    print("🔧 Forzando configuración de Cloudinary...")
    
    # Configurar variables de entorno manualmente
    os.environ['RENDER'] = 'true'
    os.environ['CLOUDINARY_CLOUD_NAME'] = 'do1ntnlop'
    os.environ['CLOUDINARY_API_KEY'] = '117225377115856'
    os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
    django.setup()
    
    print("\n📋 Variables de entorno forzadas:")
    print(f"RENDER: {os.environ.get('RENDER')}")
    print(f"CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME')}")
    print(f"CLOUDINARY_API_KEY: {os.environ.get('CLOUDINARY_API_KEY')}")
    print(f"CLOUDINARY_API_SECRET: {os.environ.get('CLOUDINARY_API_SECRET')}")
    
    print("\n🔧 Configuración de Django:")
    print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No definida')}")
    print(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'No definida')}")
    print(f"MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'No definida')}")
    
    # Verificar si CLOUDINARY está configurado
    if hasattr(settings, 'CLOUDINARY'):
        print(f"\n☁️ Configuración de Cloudinary:")
        print(f"cloud_name: {settings.CLOUDINARY.get('cloud_name')}")
        print(f"api_key: {settings.CLOUDINARY.get('api_key')}")
        print(f"api_secret: {settings.CLOUDINARY.get('api_secret')}")
    else:
        print("\n❌ CLOUDINARY no está configurado en settings")
    
    # Verificar la condición de activación
    render_in_env = 'RENDER' in os.environ
    cloudinary_name_in_env = bool(os.environ.get('CLOUDINARY_CLOUD_NAME'))
    
    print(f"\n🎯 Condiciones de activación:")
    print(f"'RENDER' in os.environ: {render_in_env}")
    print(f"os.environ.get('CLOUDINARY_CLOUD_NAME'): {cloudinary_name_in_env}")
    print(f"Condición total: {render_in_env or cloudinary_name_in_env}")
    
    return render_in_env or cloudinary_name_in_env

def test_cloudinary_upload_forced():
    """Probar subida a Cloudinary con configuración forzada"""
    print("\n🧪 Probando subida a Cloudinary con configuración forzada...")
    
    try:
        import cloudinary
        import cloudinary.uploader
        
        # Verificar configuración
        print(f"Cloudinary configurado: {cloudinary.config()}")
        
        # Crear un archivo de prueba
        test_content = b"test image content for cloudinary"
        
        # Intentar subir
        result = cloudinary.uploader.upload(
            test_content,
            public_id="test_forced_upload",
            resource_type="auto"
        )
        
        print(f"✅ Subida exitosa: {result.get('url', 'No URL')}")
        return True
        
    except Exception as e:
        print(f"❌ Error en subida directa: {e}")
        return False

def test_django_storage_forced():
    """Probar el storage de Django con configuración forzada"""
    print("\n📁 Probando storage de Django con configuración forzada...")
    
    try:
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        print(f"Storage actual: {default_storage}")
        print(f"Clase del storage: {type(default_storage)}")
        
        # Verificar si es MediaCloudinaryStorage
        if 'MediaCloudinaryStorage' in str(type(default_storage)):
            print("✅ Storage es MediaCloudinaryStorage")
        else:
            print("❌ Storage NO es MediaCloudinaryStorage")
        
        # Intentar guardar un archivo de prueba
        test_file = ContentFile(b"test content for forced storage", name="test_forced.txt")
        saved_path = default_storage.save("test_forced_upload.txt", test_file)
        
        print(f"✅ Archivo guardado en: {saved_path}")
        
        # Verificar si existe
        exists = default_storage.exists(saved_path)
        print(f"Archivo existe: {exists}")
        
        if exists:
            # Obtener URL
            url = default_storage.url(saved_path)
            print(f"URL del archivo: {url}")
            
            # Verificar si es URL de Cloudinary
            if 'cloudinary.com' in url:
                print("✅ URL es de Cloudinary")
                return True
            else:
                print("⚠️  URL NO es de Cloudinary")
                return False
        
    except Exception as e:
        print(f"❌ Error en storage de Django: {e}")
        return False

def test_product_creation_forced():
    """Probar creación de producto con configuración forzada"""
    print("\n📦 Probando creación de producto con configuración forzada...")
    
    try:
        from productos.models import Producto
        from django.core.files.base import ContentFile
        
        # Crear un producto de prueba
        producto = Producto.objects.create(
            nombre="Test Producto Forzado",
            sku="TEST-FORCED-001",
            slug="test-producto-forzado",
            precio=99.99,
            descripcion_corta="Test con configuración forzada",
            tipo="fisico",
            estado="publicado",
            gestion_stock=True,
            stock=10,
            costo=50.00
        )
        
        # Crear un archivo de imagen de prueba
        test_image_content = b"fake image content"
        test_image = ContentFile(test_image_content, name="test_image.jpg")
        
        # Guardar la imagen
        producto.imagen_principal.save("test_forced_image.jpg", test_image, save=True)
        
        print(f"✅ Producto creado: {producto.nombre}")
        print(f"📸 URL de imagen: {producto.imagen_principal.url}")
        
        # Verificar si la URL es de Cloudinary
        if 'cloudinary.com' in producto.imagen_principal.url:
            print("✅ ¡URL de Cloudinary detectada!")
            return True
        else:
            print("⚠️  URL local detectada")
            return False
            
    except Exception as e:
        print(f"❌ Error en creación de producto: {e}")
        return False

if __name__ == "__main__":
    # Forzar configuración
    cloudinary_active = force_cloudinary_config()
    
    if cloudinary_active:
        print("\n✅ Cloudinary debería estar activo")
        
        # Probar subida directa
        test_cloudinary_upload_forced()
        
        # Probar storage de Django
        test_django_storage_forced()
        
        # Probar creación de producto
        test_product_creation_forced()
        
    else:
        print("\n❌ Cloudinary no debería estar activo") 