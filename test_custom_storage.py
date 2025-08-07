#!/usr/bin/env python
"""
Script para probar nuestro storage personalizado de Cloudinary
"""
import os
import sys
import django
from pathlib import Path

def test_custom_storage():
    """Probar nuestro storage personalizado"""
    
    print("🧪 PROBANDO STORAGE PERSONALIZADO DE CLOUDINARY")
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
        
        from django.conf import settings
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        print("✅ Django configurado correctamente")
        print(f"📋 DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        print(f"📋 Storage actual: {default_storage}")
        print(f"📋 Storage class: {type(default_storage)}")
        
        # Importar nuestro storage personalizado
        try:
            from Backend.cloudinary_storage import CloudinaryStorage
            print("✅ CloudinaryStorage importado correctamente")
            
            # Crear instancia de nuestro storage
            cloudinary_storage = CloudinaryStorage()
            print(f"📋 CloudinaryStorage creado: {cloudinary_storage}")
            
            # Probar subida directa
            print("\n🧪 PROBANDO SUBIDA DIRECTA CON CLOUDINARYSTORAGE")
            
            test_content = b"Test file content for Cloudinary upload"
            test_file = ContentFile(test_content, name="test_direct_upload.txt")
            
            # Guardar usando nuestro storage directamente
            saved_path = cloudinary_storage.save('test/direct_upload.txt', test_file)
            print(f"✅ Archivo guardado en: {saved_path}")
            
            # Verificar URL
            url = cloudinary_storage.url(saved_path)
            print(f"🔗 URL del archivo: {url}")
            
            if 'cloudinary.com' in url:
                print("☁️ ¡EXCELENTE! El archivo se subió a Cloudinary")
                return True
            else:
                print("📁 El archivo se guardó localmente")
                return False
                
        except ImportError as e:
            print(f"❌ Error importando CloudinaryStorage: {e}")
            return False
        except Exception as e:
            print(f"❌ Error con CloudinaryStorage: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_serializer_with_custom_storage():
    """Probar serializer con nuestro storage personalizado"""
    
    print("\n🧪 PROBANDO SERIALIZER CON STORAGE PERSONALIZADO")
    print("="*60)
    
    try:
        from categorias.models import CategoriaProducto
        from categorias.serializers import CategoriaProductoSerializer
        from django.core.files.base import ContentFile
        from django.core.files.uploadedfile import InMemoryUploadedFile
        from io import BytesIO
        from datetime import datetime
        
        # Crear una categoría de prueba
        categoria = CategoriaProducto.objects.create(
            nombre=f"Test Custom Storage {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            descripcion="Prueba con storage personalizado",
            activa=True,
            orden=997
        )
        
        # Crear un archivo de prueba
        test_content = b"Test image content for custom storage upload"
        test_file = ContentFile(test_content, name="test_custom_image.jpg")
        
        # Simular InMemoryUploadedFile
        file_obj = InMemoryUploadedFile(
            file=BytesIO(test_content),
            field_name='imagen',
            name='test_custom_image.jpg',
            content_type='image/jpeg',
            size=len(test_content),
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
    print("🔍 PRUEBA DE STORAGE PERSONALIZADO")
    print("="*60)
    
    # Probar storage personalizado
    storage_ok = test_custom_storage()
    
    # Probar serializer con storage personalizado
    serializer_ok = test_serializer_with_custom_storage()
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    print(f"✅ Storage personalizado: {'EXITOSO' if storage_ok else 'FALLIDO'}")
    print(f"✅ Serializer con storage personalizado: {'EXITOSO' if serializer_ok else 'FALLIDO'}")
    
    if storage_ok and serializer_ok:
        print("🎉 ¡PERFECTO! El storage personalizado funciona correctamente")
        print("✅ Las imágenes se suben a Cloudinary")
        print("✅ El problema está resuelto")
    elif storage_ok:
        print("✅ El storage personalizado funciona")
        print("❌ Pero hay problemas con el serializer")
        print("🔧 Revisar la implementación del serializer")
    else:
        print("❌ Hay problemas con el storage personalizado")
        print("🔧 Revisar la implementación de CloudinaryStorage")

if __name__ == '__main__':
    main() 