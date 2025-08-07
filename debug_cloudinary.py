#!/usr/bin/env python3
"""
Script de debug para probar Cloudinary directamente
"""
import os
import sys
import django
from io import BytesIO
from PIL import Image

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

import cloudinary
import cloudinary.uploader
import cloudinary.api

def test_cloudinary_direct():
    """Probar Cloudinary directamente"""
    print("🧪 Probando Cloudinary directamente...")
    
    try:
        # Configurar Cloudinary
        cloudinary.config(
            cloud_name="do1ntnlop",
            api_key="117225377115856",
            api_secret="e0YSrk3sT_70-ijM6mwdFBIWP9w"
        )
        
        print("✅ Cloudinary configurado")
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (200, 200), color='red')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        print(f"✅ Imagen creada: {len(img_io.getvalue())} bytes")
        
        # Subir directamente a Cloudinary
        result = cloudinary.uploader.upload(
            img_io,
            public_id=f"test_direct_{os.getpid()}",
            overwrite=True
        )
        
        print("✅ Subida exitosa a Cloudinary:")
        print(f"  Public ID: {result['public_id']}")
        print(f"  URL: {result['secure_url']}")
        print(f"  Tamaño: {result.get('bytes', 0)} bytes")
        
        # Verificar que existe
        try:
            resource = cloudinary.api.resource(result['public_id'])
            print("✅ Archivo verificado en Cloudinary")
        except Exception as e:
            print(f"❌ Error verificando archivo: {e}")
        
        # Eliminar archivo de prueba
        try:
            cloudinary.uploader.destroy(result['public_id'])
            print("✅ Archivo eliminado de Cloudinary")
        except Exception as e:
            print(f"❌ Error eliminando archivo: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"❌ Tipo de error: {type(e).__name__}")
        return False

def test_django_storage():
    """Probar el storage de Django"""
    print("\n🧪 Probando storage de Django...")
    
    try:
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (150, 150), color='blue')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Crear archivo de prueba
        test_content = ContentFile(img_io.getvalue())
        test_name = f"test_storage_{os.getpid()}.png"
        
        print(f"📤 Subiendo: {test_name}")
        
        # Subir usando el storage
        saved_name = default_storage.save(test_name, test_content)
        print(f"✅ Guardado como: {saved_name}")
        
        # Obtener URL
        url = default_storage.url(saved_name)
        print(f"🔗 URL: {url}")
        
        # Verificar existencia
        exists = default_storage.exists(saved_name)
        print(f"🔍 Existe: {exists}")
        
        # Eliminar
        deleted = default_storage.delete(saved_name)
        print(f"🗑️ Eliminado: {deleted}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO DEBUG DE CLOUDINARY")
    print("=" * 50)
    
    # Probar Cloudinary directamente
    direct_success = test_cloudinary_direct()
    
    # Probar storage de Django
    storage_success = test_django_storage()
    
    print("\n📊 RESULTADOS")
    print("=" * 50)
    print(f"Cloudinary directo: {'✅ PASÓ' if direct_success else '❌ FALLÓ'}")
    print(f"Storage Django: {'✅ PASÓ' if storage_success else '❌ FALLÓ'}")
    
    if direct_success and storage_success:
        print("\n🎉 ¡Todo funciona correctamente!")
    else:
        print("\n⚠️ Hay problemas que resolver") 