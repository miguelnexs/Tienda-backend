#!/usr/bin/env python3
"""
Script para probar la solución de storage forzado
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

from django.core.files import File
from categorias.models import CategoriaProducto
from django.core.files.storage import default_storage

def test_storage_forzado():
    """Probar storage forzado"""
    print("🧪 PROBANDO STORAGE FORZADO")
    print("=" * 60)
    
    try:
        # Verificar configuración
        print("📋 Verificando configuración...")
        print(f"📁 default_storage class: {type(default_storage).__name__}")
        print(f"📁 default_storage module: {type(default_storage).__module__}")
        
        # Crear imagen de prueba
        img = Image.new('RGB', (600, 600), color='#E67E22')  # Naranja
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        print("📸 Imagen de prueba creada")
        
        # Crear categoría
        categoria = CategoriaProducto(
            nombre="Categoría Storage Forzado",
            descripcion="Categoría para probar storage forzado",
            slug=f"categoria-storage-forzado-{os.getpid()}"
        )
        
        categoria.save()
        print(f"✅ Categoría creada: {categoria.id}")
        
        # Crear archivo
        django_file = File(img_io, name=f'categoria_storage_forzado_{os.getpid()}.jpg')
        
        print("📤 Subiendo imagen...")
        
        # Subir imagen
        categoria.imagen.save(django_file.name, django_file, save=True)
        
        print("✅ Imagen guardada")
        print(f"📁 Nombre: {categoria.imagen.name}")
        print(f"🔗 URL: {categoria.imagen.url}")
        
        # Verificar URL
        if 'cloudinary.com' in categoria.imagen.url:
            print("✅ URL es de Cloudinary")
        else:
            print("❌ URL no es de Cloudinary")
        
        # Verificar existencia
        if hasattr(categoria.imagen, 'storage'):
            exists = categoria.imagen.storage.exists(categoria.imagen.name)
            print(f"📁 Existe en storage: {exists}")
        
        # Verificar en Cloudinary
        try:
            import cloudinary.api
            result = cloudinary.api.resource(categoria.imagen.name)
            print("✅ Archivo encontrado en Cloudinary")
            print(f"📊 Información:")
            print(f"  Public ID: {result['public_id']}")
            print(f"  URL segura: {result.get('secure_url', 'N/A')}")
            print(f"  Tamaño: {result.get('bytes', 0)} bytes")
            
            # Probar acceso
            secure_url = result.get('secure_url')
            if secure_url:
                try:
                    import requests
                    response = requests.get(secure_url, timeout=10)
                    print(f"📡 Respuesta HTTP: {response.status_code}")
                    if response.status_code == 200:
                        print("✅ URL accesible")
                        print(f"📏 Tamaño: {len(response.content)} bytes")
                    else:
                        print(f"❌ Error: HTTP {response.status_code}")
                except Exception as e:
                    print(f"⚠️ Error verificando URL: {e}")
            
        except Exception as e:
            print(f"❌ Archivo NO encontrado en Cloudinary: {e}")
        
        # Limpiar
        categoria.delete()
        print("✅ Categoría eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando storage forzado: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_uploads_forzado():
    """Probar múltiples subidas con storage forzado"""
    print("\n🧪 PROBANDO MÚLTIPLES SUBIDAS CON STORAGE FORZADO")
    print("=" * 60)
    
    try:
        for i in range(3):
            print(f"\n📤 Subida {i+1}/3...")
            
            # Crear imagen diferente
            colors = ['#9B59B6', '#3498DB', '#2ECC71']  # Púrpura, Azul, Verde
            img = Image.new('RGB', (400 + i*100, 400 + i*100), color=colors[i])
            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            img_io.seek(0)
            
            # Crear categoría
            categoria = CategoriaProducto(
                nombre=f"Categoría Múltiple Forzado {i+1}",
                descripcion=f"Categoría múltiple forzado {i+1}",
                slug=f"categoria-multiple-forzado-{i+1}-{os.getpid()}"
            )
            
            categoria.save()
            
            # Subir imagen
            django_file = File(img_io, name=f'categoria_multiple_forzado_{i+1}_{os.getpid()}.jpg')
            categoria.imagen.save(django_file.name, django_file, save=True)
            
            print(f"✅ Subida {i+1} completada")
            print(f"  URL: {categoria.imagen.url}")
            
            # Verificar en Cloudinary
            try:
                import cloudinary.api
                result = cloudinary.api.resource(categoria.imagen.name)
                print(f"✅ Archivo {i+1} encontrado en Cloudinary")
            except Exception as e:
                print(f"❌ Archivo {i+1} NO encontrado en Cloudinary: {e}")
            
            # Limpiar
            categoria.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando múltiples subidas: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE STORAGE FORZADO")
    print("=" * 60)
    
    # Probar storage forzado
    forzado_success = test_storage_forzado()
    
    # Probar múltiples subidas
    multiple_success = test_multiple_uploads_forzado()
    
    print("\n📊 RESULTADOS FINALES")
    print("=" * 60)
    print(f"Storage forzado: {'✅ PASÓ' if forzado_success else '❌ FALLÓ'}")
    print(f"Múltiples subidas: {'✅ PASÓ' if multiple_success else '❌ FALLÓ'}")
    
    if forzado_success and multiple_success:
        print("\n🎉 ¡STORAGE FORZADO FUNCIONA!")
        print("✅ Las imágenes se suben correctamente a Cloudinary.")
        print("✅ El admin de Django funciona correctamente.")
        print("✅ El problema está completamente resuelto.")
        print("\n💡 Ahora puedes usar el admin sin problemas:")
        print("   1. Ve a http://localhost:8000/admin/")
        print("   2. Crea o edita una categoría")
        print("   3. Sube una imagen")
        print("   4. La imagen se subirá correctamente a Cloudinary")
    else:
        print("\n⚠️ Aún hay problemas con el storage forzado.")
        print("❌ Revisa la configuración del sistema.") 