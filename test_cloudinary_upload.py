#!/usr/bin/env python3
"""
Script para probar la subida de imágenes a Cloudinary
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

from PIL import Image
import io
from django.core.files import File
from categorias.models import CategoriaProducto
from categorias.serializers import CategoriaProductoSerializer

def create_test_image():
    """Crear una imagen de prueba"""
    img = Image.new('RGB', (300, 200), color='blue')
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.text((80, 80), "CLOUDINARY", fill='white')
    draw.text((60, 120), "TEST UPLOAD", fill='white')
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer

def test_cloudinary_upload():
    """Probar subida a Cloudinary"""
    print("🚀 PROBANDO SUBIDA A CLOUDINARY")
    print("=" * 50)
    
    try:
        # Crear imagen de prueba
        buffer = create_test_image()
        
        # Crear archivo temporal
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(buffer.getvalue())
            temp_file_path = temp_file.name
        
        # Crear categoría de prueba
        categoria = CategoriaProducto.objects.create(
            nombre="Test Cloudinary Upload",
            descripcion="Prueba de subida a Cloudinary",
            orden=999
        )
        
        print(f"✅ Categoría creada: {categoria.nombre}")
        
        # Subir imagen
        with open(temp_file_path, 'rb') as f:
            django_file = File(f, name='test_cloudinary_upload.png')
            categoria.imagen.save('test_cloudinary_upload.png', django_file, save=True)
        
        print(f"📁 Imagen guardada: {categoria.imagen.name}")
        print(f"🔗 URL de la imagen: {categoria.imagen.url}")
        
        # Verificar si está en Cloudinary
        if 'cloudinary.com' in categoria.imagen.url:
            print("✅ ¡La imagen se subió a Cloudinary!")
        else:
            print("❌ La imagen se guardó localmente")
        
        # Probar serializer
        serializer = CategoriaProductoSerializer(categoria, context={'request': None})
        data = serializer.data
        
        print(f"\n📊 Datos del serializer:")
        print(f"  imagen: {data.get('imagen')}")
        print(f"  imagen_url: {data.get('imagen_url')}")
        
        # Limpiar
        os.unlink(temp_file_path)
        categoria.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_existing_categories():
    """Probar categorías existentes"""
    print("\n🔍 VERIFICANDO CATEGORÍAS EXISTENTES")
    print("=" * 50)
    
    try:
        categorias = CategoriaProducto.objects.all()
        
        for categoria in categorias:
            print(f"\n📋 Categoría: {categoria.nombre}")
            if categoria.imagen:
                print(f"  📁 Ruta: {categoria.imagen.name}")
                print(f"  🔗 URL: {categoria.imagen.url}")
                
                if 'cloudinary.com' in categoria.imagen.url:
                    print("  ✅ En Cloudinary")
                else:
                    print("  ❌ Local")
            else:
                print("  ⚠️ Sin imagen")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN DE CLOUDINARY")
    print("=" * 60)
    
    # Probar subida
    test_cloudinary_upload()
    
    # Verificar existentes
    test_existing_categories()
    
    print("\n✅ Verificación completada")

if __name__ == "__main__":
    main() 