#!/usr/bin/env python
"""
Script para probar subida de imagen real a Cloudinary
"""
import os
import sys
import django
from pathlib import Path

def test_real_image_upload():
    """Probar subida de imagen real"""
    
    print("🧪 PROBANDO SUBIDA DE IMAGEN REAL A CLOUDINARY")
    print("="*60)
    
    try:
        # Simular entorno de Render
        os.environ['RENDER'] = 'true'
        os.environ['DJANGO_SETTINGS_MODULE'] = 'Backend.render_settings'
        
        # Configurar DATABASE_URL para pruebas
        if not os.environ.get('DATABASE_URL'):
            os.environ['DATABASE_URL'] = 'postgresql://tienda_user:PWKuO99372EAcsyx5KpHlV9VBIQJkvle@dpg-d278j5u3jp1c73en5gbg-a.ohio-postgres.render.com/tienda_production'
        
        # Configurar Django
        django.setup()
        
        from django.core.files.base import ContentFile
        from django.core.files.uploadedfile import InMemoryUploadedFile
        from io import BytesIO
        from datetime import datetime
        
        # Buscar imagen real
        imagen_path = Path("D:/usuario/Downloads/bolso/cartera-casual-para-mujer-23064.jpg")
        
        if not imagen_path.exists():
            print("❌ No se encontró la imagen de prueba")
            return False
        
        # Leer imagen real
        with open(imagen_path, 'rb') as f:
            image_content = f.read()
        
        print(f"✅ Imagen encontrada: {imagen_path}")
        print(f"📁 Tamaño: {len(image_content)} bytes")
        
        # Importar nuestro storage personalizado
        from Backend.cloudinary_storage import CloudinaryStorage
        cloudinary_storage = CloudinaryStorage()
        
        # Crear ContentFile con imagen real
        content_file = ContentFile(image_content, name="cartera-casual-para-mujer-23064.jpg")
        
        # Generar nombre único
        import uuid
        unique_name = f"test_images/{uuid.uuid4().hex}_cartera.jpg"
        
        print(f"📤 Subiendo imagen a Cloudinary...")
        print(f"📋 Nombre: {unique_name}")
        
        # Guardar usando nuestro storage personalizado
        saved_path = cloudinary_storage.save(unique_name, content_file)
        
        print(f"✅ Archivo guardado en: {saved_path}")
        
        # Verificar URL
        url = cloudinary_storage.url(saved_path)
        print(f"🔗 URL del archivo: {url}")
        
        if 'cloudinary.com' in url:
            print("☁️ ¡EXCELENTE! La imagen se subió a Cloudinary")
            return True
        else:
            print("📁 La imagen se guardó localmente")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        return False

def test_serializer_with_real_image():
    """Probar serializer con imagen real"""
    
    print("\n🧪 PROBANDO SERIALIZER CON IMAGEN REAL")
    print("="*60)
    
    try:
        from categorias.models import CategoriaProducto
        from categorias.serializers import CategoriaProductoSerializer
        from django.core.files.uploadedfile import InMemoryUploadedFile
        from io import BytesIO
        from datetime import datetime
        
        # Buscar imagen real
        imagen_path = Path("D:/usuario/Downloads/bolso/cartera-casual-para-mujer-23064.jpg")
        
        if not imagen_path.exists():
            print("❌ No se encontró la imagen de prueba")
            return False
        
        # Leer imagen real
        with open(imagen_path, 'rb') as f:
            image_content = f.read()
        
        # Crear una categoría de prueba
        categoria = CategoriaProducto.objects.create(
            nombre=f"Test Real Image {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            descripcion="Prueba con imagen real",
            activa=True,
            orden=996
        )
        
        # Simular InMemoryUploadedFile con imagen real
        file_obj = InMemoryUploadedFile(
            file=BytesIO(image_content),
            field_name='imagen',
            name='cartera-casual-para-mujer-23064.jpg',
            content_type='image/jpeg',
            size=len(image_content),
            charset=None
        )
        
        # Crear serializer y probar _save_imagen
        serializer = CategoriaProductoSerializer()
        serializer._save_imagen(categoria, file_obj)
        
        print(f"✅ Imagen guardada para categoría: {categoria.nombre}")
        print(f"📁 Ruta de la imagen: {categoria.imagen.name}")
        print(f"🔗 URL de la imagen: {categoria.imagen.url}")
        
        if 'cloudinary.com' in categoria.imagen.url:
            print("☁️ ¡EXCELENTE! La imagen se subió a Cloudinary")
            return True
        else:
            print("📁 La imagen se guardó localmente")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de serializer: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 PRUEBA DE SUBIDA DE IMAGEN REAL")
    print("="*60)
    
    # Probar subida directa con imagen real
    direct_ok = test_real_image_upload()
    
    # Probar serializer con imagen real
    serializer_ok = test_serializer_with_real_image()
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    print(f"✅ Subida directa con imagen real: {'EXITOSA' if direct_ok else 'FALLIDA'}")
    print(f"✅ Serializer con imagen real: {'EXITOSA' if serializer_ok else 'FALLIDA'}")
    
    if direct_ok and serializer_ok:
        print("🎉 ¡PERFECTO! Todo funciona correctamente")
        print("✅ Las imágenes se suben a Cloudinary")
        print("✅ El problema está resuelto")
    elif direct_ok:
        print("✅ La subida directa funciona")
        print("❌ Pero hay problemas con el serializer")
        print("🔧 Revisar la implementación del serializer")
    else:
        print("❌ Hay problemas con la subida a Cloudinary")
        print("🔧 Revisar la configuración de Cloudinary")

if __name__ == '__main__':
    main() 