#!/usr/bin/env python3
"""
Script de diagnóstico para el problema del storage
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

def check_environment():
    """Verificar variables de entorno"""
    print("🔧 VERIFICANDO VARIABLES DE ENTORNO")
    print("=" * 50)
    
    env_vars = {
        'RENDER': os.environ.get('RENDER'),
        'CLOUDINARY_CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'CLOUDINARY_API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'CLOUDINARY_API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }
    
    for var, value in env_vars.items():
        if value:
            if 'SECRET' in var or 'KEY' in var:
                display_value = f"{value[:10]}..."
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NO ENCONTRADA")
    
    return True

def check_settings():
    """Verificar configuración de Django"""
    print("\n⚙️ VERIFICANDO CONFIGURACIÓN DE DJANGO")
    print("=" * 50)
    
    print(f"📋 Configuración actual:")
    print(f"  DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    print(f"  MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'No configurado')}")
    print(f"  MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'No configurado')}")
    print(f"  RENDER en settings: {'RENDER' in os.environ}")
    
    return True

def check_storage_instance():
    """Verificar instancia del storage"""
    print("\n🔧 VERIFICANDO INSTANCIA DEL STORAGE")
    print("=" * 50)
    
    print(f"📋 Storage por defecto:")
    print(f"  Tipo: {type(default_storage).__name__}")
    print(f"  Clase: {default_storage.__class__.__name__}")
    print(f"  Módulo: {default_storage.__class__.__module__}")
    
    # Verificar si es CloudinaryStorage
    if 'CloudinaryStorage' in str(type(default_storage)):
        print("✅ Usando CloudinaryStorage")
        
        # Verificar configuración del storage
        if hasattr(default_storage, '_cloud_name'):
            print(f"  Cloud Name: {default_storage._cloud_name}")
        if hasattr(default_storage, '_api_key'):
            print(f"  API Key: {default_storage._api_key[:10]}...")
    else:
        print("❌ No usando CloudinaryStorage")
        print(f"  Storage actual: {default_storage}")
    
    return True

def test_direct_upload():
    """Probar subida directa"""
    print("\n📤 PROBANDO SUBIDA DIRECTA")
    print("=" * 50)
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 150), color='purple')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.text((50, 60), "DIRECT", fill='white')
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
        test_name = 'debug_test_direct.png'
        
        with open(temp_file_path, 'rb') as f:
            django_file = File(f, name=test_name)
            
            print(f"📤 Subiendo archivo: {test_name}")
            print(f"📁 Usando storage: {type(default_storage).__name__}")
            
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
            nombre="Debug Test Model",
            descripcion="Prueba de diagnóstico de storage",
            orden=997
        )
        
        print(f"✅ Categoría creada: {categoria.nombre}")
        
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 150), color='orange')
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
            django_file = File(f, name='debug_test_model.png')
            categoria.imagen.save('debug_test_model.png', django_file, save=True)
        
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
    print("🔍 DIAGNÓSTICO DEL PROBLEMA DE STORAGE")
    print("=" * 60)
    
    # Verificar entorno
    check_environment()
    
    # Verificar configuración
    check_settings()
    
    # Verificar storage
    check_storage_instance()
    
    # Probar subida directa
    test_direct_upload()
    
    # Probar modelo
    test_model_upload()
    
    print("\n✅ Diagnóstico completado")

if __name__ == "__main__":
    main() 