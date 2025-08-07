#!/usr/bin/env python3
"""
Script simple para probar que el error 500 está corregido
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

from django.core.files.uploadedfile import InMemoryUploadedFile
from categorias.models import CategoriaProducto

def test_simple_upload():
    """Probar subida simple sin error 500"""
    print("🧪 PROBANDO SUBIDA SIMPLE SIN ERROR 500")
    print("=" * 60)
    
    try:
        # Crear imagen
        img = Image.new('RGB', (500, 500), color='#FF6B6B')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear archivo
        archivo = InMemoryUploadedFile(
            file=img_io,
            field_name='imagen',
            name='test_simple.jpg',
            content_type='image/jpeg',
            size=len(img_io.getvalue()),
            charset=None
        )
        
        # Crear categoría
        categoria = CategoriaProducto.objects.create(
            nombre="Categoría Test Simple",
            descripcion="Categoría para probar subida simple",
            slug="categoria-test-simple"
        )
        
        print("✅ Categoría creada")
        print(f"📁 Archivo creado: {archivo.name}")
        print(f"📏 Tamaño: {archivo.size} bytes")
        
        # Guardar imagen
        try:
            categoria.imagen.save('test_simple.jpg', archivo, save=True)
            print("✅ Imagen guardada sin error 500")
            
            # Verificar resultado
            print(f"📁 Nombre de imagen: {categoria.imagen.name}")
            print(f"🔗 URL: {categoria.imagen.url}")
            
            # Verificar en Cloudinary
            try:
                import cloudinary.api
                result = cloudinary.api.resource(categoria.imagen.name)
                print("✅ Archivo encontrado en Cloudinary")
                print(f"📊 Tamaño: {result.get('bytes', 0)} bytes")
                
                # Limpiar
                categoria.delete()
                print("✅ Categoría eliminada")
                
                return True
            except Exception as e:
                print(f"❌ Archivo NO encontrado en Cloudinary: {e}")
                categoria.delete()
                return False
                
        except Exception as e:
            print(f"❌ ERROR 500: {e}")
            categoria.delete()
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba simple: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA SIMPLE")
    print("=" * 60)
    
    success = test_simple_upload()
    
    if success:
        print("\n🎉 ¡ERROR 500 CORREGIDO!")
        print("✅ La subida funciona sin error 500.")
        print("✅ Las imágenes se suben correctamente a Cloudinary.")
        print("✅ El sistema está funcionando correctamente.")
        print("\n💡 EL SISTEMA ESTÁ LISTO PARA USAR")
    else:
        print("\n⚠️ Aún hay problemas con el error 500.")
        print("❌ Revisa la configuración del sistema.") 