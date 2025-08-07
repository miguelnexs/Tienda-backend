#!/usr/bin/env python3
"""
Script de prueba para el storage simple de Cloudinary
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

def test_simple_storage():
    """Probar el storage simple"""
    print("🔧 PROBANDO STORAGE SIMPLE")
    print("=" * 50)
    
    # Verificar configuración
    print(f"📋 Configuración:")
    print(f"  DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    print(f"  Storage actual: {type(default_storage).__name__}")
    
    # Verificar si es SimpleCloudinaryStorage
    if 'SimpleCloudinaryStorage' in str(type(default_storage)):
        print("✅ Usando SimpleCloudinaryStorage")
    else:
        print("❌ No usando SimpleCloudinaryStorage")
        print(f"  Storage actual: {default_storage}")
    
    return True

def test_upload():
    """Probar subida"""
    print("\n📤 PROBANDO SUBIDA")
    print("=" * 50)
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 150), color='red')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.text((50, 60), "SIMPLE", fill='white')
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
        test_name = 'test_simple_storage.png'
        
        with open(temp_file_path, 'rb') as f:
            django_file = File(f, name=test_name)
            
            print(f"📤 Subiendo archivo: {test_name}")
            
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
                print("⚠️ PROBLEMA: No se está usando Cloudinary")
            
            # Verificar existencia
            exists = default_storage.exists(saved_name)
            print(f"  Existe: {exists}")
            
            # Limpiar
            try:
                default_storage.delete(saved_name)
                print("✅ Archivo eliminado")
            except:
                print("⚠️ No se pudo eliminar archivo")
            
            os.unlink(temp_file_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_upload():
    """Probar subida a través de modelo"""
    print("\n📝 PROBANDO SUBIDA A TRAVÉS DE MODELO")
    print("=" * 50)
    
    try:
        from categorias.models import CategoriaProducto
        
        # Crear categoría de prueba
        categoria = CategoriaProducto.objects.create(
            nombre="Test Simple Storage",
            descripcion="Prueba del storage simple",
            orden=996
        )
        
        print(f"✅ Categoría creada: {categoria.nombre}")
        
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 150), color='blue')
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
        
        print(f"📤 Subiendo imagen al modelo...")
        
        # Subir imagen
        with open(temp_file_path, 'rb') as f:
            django_file = File(f, name='test_simple_model.png')
            categoria.imagen.save('test_simple_model.png', django_file, save=True)
        
        print(f"📁 Imagen guardada: {categoria.imagen.name}")
        print(f"🔗 URL: {categoria.imagen.url}")
        
        # Verificar si está en Cloudinary
        if 'cloudinary.com' in categoria.imagen.url:
            print("☁️ ¡Imagen subida a Cloudinary!")
        else:
            print("📁 Imagen guardada localmente")
            print("⚠️ PROBLEMA: El modelo no está usando Cloudinary")
        
        # Limpiar
        os.unlink(temp_file_path)
        categoria.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🔍 PRUEBA DEL STORAGE SIMPLE")
    print("=" * 60)
    
    # Probar configuración
    test_simple_storage()
    
    # Probar subida directa
    test_upload()
    
    # Probar modelo
    test_model_upload()
    
    print("\n✅ Prueba completada")

if __name__ == "__main__":
    main() 