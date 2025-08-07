#!/usr/bin/env python
"""
Script para forzar el uso de Cloudinary en desarrollo y probar la subida completa
"""
import os
import sys
import django
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from productos.models import Producto, ColorProducto, ImagenProducto
from django.core.files import File
from django.conf import settings

def force_cloudinary_settings():
    """Forzar configuración de Cloudinary para pruebas"""
    
    print("🔧 FORZANDO CONFIGURACIÓN DE CLOUDINARY")
    print("="*50)
    
    # Configurar Cloudinary manualmente
    cloudinary.config(
        cloud_name="do1ntnlop",
        api_key="1172253771",
        api_secret="e0YSrk3sT_"
    )
    
    print("✅ Cloudinary configurado manualmente")
    print(f"  Cloud Name: do1ntnlop")
    print(f"  API Key: 1172253771")
    print(f"  API Secret: e0YSrk3sT_")
    
    return True

def test_cloudinary_upload_with_metadata():
    """Probar subida a Cloudinary con metadatos específicos"""
    
    print("\n" + "="*50)
    print("📸 SUBIDA A CLOUDINARY CON METADATOS")
    print("="*50)
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    try:
        # Subir imagen con metadatos específicos
        result = cloudinary.uploader.upload(
            image_path,
            folder="productos/colores",
            public_id="bolso-negro-metadata-test",
            overwrite=True,
            resource_type="image",
            transformation=[
                {"width": 800, "height": 800, "crop": "fill"},
                {"quality": "auto", "fetch_format": "auto"}
            ],
            tags=["bolso", "negro", "producto", "test"],
            context={
                "producto": "Bolso Negro",
                "color": "Negro",
                "categoria": "Accesorios"
            }
        )
        
        print("✅ Imagen subida exitosamente con metadatos!")
        print(f"📸 URL de la imagen: {result['secure_url']}")
        print(f"📁 Public ID: {result['public_id']}")
        print(f"📏 Tamaño: {result['bytes']} bytes")
        print(f"🖼️ Formato: {result['format']}")
        print(f"📐 Dimensiones: {result['width']}x{result['height']}")
        print(f"🏷️ Tags: {result.get('tags', [])}")
        print(f"📋 Context: {result.get('context', {})}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error subiendo a Cloudinary: {e}")
        return False

def test_multiple_cloudinary_uploads():
    """Probar múltiples subidas a Cloudinary"""
    
    print("\n" + "="*50)
    print("🔄 MÚLTIPLES SUBIDAS A CLOUDINARY")
    print("="*50)
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    uploads = []
    
    # Subir varias versiones de la imagen
    variations = [
        {"name": "original", "transformation": []},
        {"name": "thumbnail", "transformation": [{"width": 150, "height": 150, "crop": "fill"}]},
        {"name": "medium", "transformation": [{"width": 400, "height": 400, "crop": "fill"}]},
        {"name": "large", "transformation": [{"width": 800, "height": 800, "crop": "fill"}]}
    ]
    
    for variation in variations:
        try:
            print(f"\n📸 Subiendo {variation['name']}...")
            
            result = cloudinary.uploader.upload(
                image_path,
                folder="productos/colores",
                public_id=f"bolso-negro-{variation['name']}",
                overwrite=True,
                resource_type="image",
                transformation=variation['transformation'],
                tags=["bolso", "negro", variation['name']]
            )
            
            uploads.append({
                "name": variation['name'],
                "url": result['secure_url'],
                "public_id": result['public_id'],
                "size": result['bytes']
            })
            
            print(f"✅ {variation['name']} subido exitosamente!")
            print(f"   URL: {result['secure_url']}")
            print(f"   Tamaño: {result['bytes']} bytes")
            
        except Exception as e:
            print(f"❌ Error subiendo {variation['name']}: {e}")
    
    return uploads

def test_cloudinary_url_generation():
    """Probar generación de URLs de Cloudinary"""
    
    print("\n" + "="*50)
    print("🔗 GENERACIÓN DE URLs DE CLOUDINARY")
    print("="*50)
    
    # URL base de la imagen subida
    base_url = "https://res.cloudinary.com/do1ntnlop/image/upload/v1754349202/productos/colores/bolso-negro-test.png"
    
    # Generar diferentes transformaciones
    transformations = [
        {"name": "Original", "url": base_url},
        {"name": "Thumbnail", "url": base_url.replace("/upload/", "/upload/w_150,h_150,c_fill/")},
        {"name": "Medium", "url": base_url.replace("/upload/", "/upload/w_400,h_400,c_fill/")},
        {"name": "Large", "url": base_url.replace("/upload/", "/upload/w_800,h_800,c_fill/")},
        {"name": "Auto Format", "url": base_url.replace("/upload/", "/upload/f_auto/")},
        {"name": "Quality Auto", "url": base_url.replace("/upload/", "/upload/q_auto/")}
    ]
    
    print("🔗 URLs generadas:")
    for trans in transformations:
        print(f"  {trans['name']}: {trans['url']}")
    
    return transformations

def main():
    """Función principal"""
    print("🧪 PRUEBA COMPLETA DE CLOUDINARY")
    print("="*50)
    
    # Forzar configuración de Cloudinary
    success_config = force_cloudinary_settings()
    
    # Probar subida con metadatos
    metadata_result = test_cloudinary_upload_with_metadata()
    
    # Probar múltiples subidas
    multiple_results = test_multiple_cloudinary_uploads()
    
    # Probar generación de URLs
    url_results = test_cloudinary_url_generation()
    
    print("\n" + "="*50)
    print("📊 RESUMEN COMPLETO DE PRUEBAS")
    print("="*50)
    print(f"✅ Configuración forzada: {'EXITOSA' if success_config else 'FALLIDA'}")
    print(f"✅ Subida con metadatos: {'EXITOSA' if metadata_result else 'FALLIDA'}")
    print(f"✅ Múltiples subidas: {'EXITOSA' if multiple_results else 'FALLIDA'}")
    print(f"✅ Generación de URLs: {'EXITOSA' if url_results else 'FALLIDA'}")
    
    if metadata_result:
        print(f"\n🔗 URL principal de la imagen:")
        print(f"   {metadata_result['secure_url']}")
    
    if multiple_results:
        print(f"\n📸 Variaciones subidas:")
        for upload in multiple_results:
            print(f"   {upload['name']}: {upload['url']}")
    
    if success_config and metadata_result:
        print("\n🎉 ¡Cloudinary está funcionando perfectamente!")
        print("💡 La imagen se subió exitosamente al cloud")
    else:
        print("\n❌ Hay problemas con Cloudinary")

if __name__ == '__main__':
    main() 