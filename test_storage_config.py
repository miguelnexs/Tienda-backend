#!/usr/bin/env python3
"""
Script para verificar la configuración del storage
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image
import io
from django.core.files import File

def test_storage_config():
    """Probar configuración del storage"""
    print("🔧 VERIFICANDO CONFIGURACIÓN DEL STORAGE")
    print("=" * 50)
    
    # Verificar configuración
    print(f"📋 Configuración actual:")
    print(f"  DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    print(f"  MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'No configurado')}")
    print(f"  MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'No configurado')}")
    
    # Verificar storage por defecto
    print(f"\n🔧 Storage por defecto:")
    print(f"  Tipo: {type(default_storage).__name__}")
    print(f"  Clase: {default_storage.__class__.__name__}")
    
    # Verificar si es CloudinaryStorage
    if 'CloudinaryStorage' in str(type(default_storage)):
        print("✅ Usando CloudinaryStorage")
    else:
        print("❌ No usando CloudinaryStorage")
    
    return True

def test_upload_to_storage():
    """Probar subida al storage"""
    print("\n📤 PROBANDO SUBIDA AL STORAGE")
    print("=" * 50)
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 150), color='red')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.text((50, 60), "STORAGE", fill='white')
        draw.text((30, 90), "TEST", fill='white')
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Crear archivo temporal
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(buffer.getvalue())
            temp_file_path = temp_file.name
        
        # Subir archivo
        test_name = 'test_storage_config.png'
        
        with open(temp_file_path, 'rb') as f:
            django_file = File(f, name=test_name)
            
            # Subir usando el storage por defecto
            saved_name = default_storage.save(test_name, django_file)
            
            print(f"✅ Archivo subido:")
            print(f"  Nombre original: {test_name}")
            print(f"  Nombre guardado: {saved_name}")
            
            # Obtener URL
            url = default_storage.url(saved_name)
            print(f"  URL: {url}")
            
            # Verificar si está en Cloudinary
            if 'cloudinary.com' in url:
                print("☁️ ¡Archivo subido a Cloudinary!")
            else:
                print("📁 Archivo guardado localmente")
            
            # Verificar existencia
            exists = default_storage.exists(saved_name)
            print(f"  Existe: {exists}")
            
            # Limpiar
            default_storage.delete(saved_name)
            os.unlink(temp_file_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_model_storage():
    """Probar storage en modelo"""
    print("\n📝 PROBANDO STORAGE EN MODELO")
    print("=" * 50)
    
    try:
        from categorias.models import CategoriaProducto
        
        # Crear categoría de prueba
        categoria = CategoriaProducto.objects.create(
            nombre="Test Storage Config",
            descripcion="Prueba de configuración de storage",
            orden=998
        )
        
        print(f"✅ Categoría creada: {categoria.nombre}")
        
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 150), color='green')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.text((50, 60), "MODEL", fill='white')
        draw.text((30, 90), "TEST", fill='white')
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Crear archivo temporal
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(buffer.getvalue())
            temp_file_path = temp_file.name
        
        # Subir imagen
        with open(temp_file_path, 'rb') as f:
            django_file = File(f, name='test_model_storage.png')
            categoria.imagen.save('test_model_storage.png', django_file, save=True)
        
        print(f"📁 Imagen guardada: {categoria.imagen.name}")
        print(f"🔗 URL: {categoria.imagen.url}")
        
        # Verificar si está en Cloudinary
        if 'cloudinary.com' in categoria.imagen.url:
            print("☁️ ¡Imagen subida a Cloudinary!")
        else:
            print("📁 Imagen guardada localmente")
        
        # Limpiar
        os.unlink(temp_file_path)
        categoria.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DE STORAGE")
    print("=" * 60)
    
    # Probar configuración
    test_storage_config()
    
    # Probar subida
    test_upload_to_storage()
    
    # Probar modelo
    test_model_storage()
    
    print("\n✅ Verificación completada")

if __name__ == "__main__":
    main() 