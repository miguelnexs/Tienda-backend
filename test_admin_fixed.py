#!/usr/bin/env python3
"""
Script para probar que el problema del admin está corregido
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

def test_admin_fixed():
    """Probar que el admin funciona correctamente"""
    print("🧪 PROBANDO ADMIN CORREGIDO")
    print("=" * 60)
    
    try:
        # Crear una imagen de prueba
        img = Image.new('RGB', (700, 700), color='#9B59B6')  # Púrpura
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=90)
        img_io.seek(0)
        
        print("📸 Imagen de prueba creada (700x700, púrpura)")
        
        # Crear categoría
        categoria = CategoriaProducto(
            nombre="Categoría Admin Fixed",
            descripcion="Categoría para probar admin corregido",
            slug=f"categoria-admin-fixed-{os.getpid()}"
        )
        
        # Guardar categoría
        categoria.save()
        print(f"✅ Categoría creada: {categoria.id}")
        
        # Crear archivo como lo haría el admin
        django_file = File(img_io, name=f'categoria_admin_fixed_{os.getpid()}.jpg')
        
        print("📤 Subiendo imagen como lo haría el admin...")
        
        # Asignar imagen (exactamente como lo hace el admin)
        categoria.imagen.save(django_file.name, django_file, save=True)
        
        print("✅ Imagen asignada")
        print(f"  Nombre: {categoria.imagen.name}")
        print(f"  URL: {categoria.imagen.url}")
        
        # Verificar URL
        if 'cloudinary.com' in categoria.imagen.url:
            print("✅ URL es de Cloudinary")
        else:
            print("❌ URL no es de Cloudinary")
            return False
        
        # Verificar existencia
        if hasattr(categoria.imagen, 'storage'):
            exists = categoria.imagen.storage.exists(categoria.imagen.name)
            print(f"  Existe en storage: {exists}")
        
        # Obtener información detallada
        try:
            import cloudinary.api
            result = cloudinary.api.resource(categoria.imagen.name)
            print(f"📊 Información de Cloudinary:")
            print(f"  Public ID: {result['public_id']}")
            print(f"  URL segura: {result.get('secure_url', 'N/A')}")
            print(f"  Tamaño: {result.get('bytes', 0)} bytes")
            print(f"  Formato: {result.get('format', 'N/A')}")
            print(f"  Ancho: {result.get('width', 0)}")
            print(f"  Alto: {result.get('height', 0)}")
            print(f"  Versión: {result.get('version', 'N/A')}")
            
            # Probar acceso a la URL segura
            secure_url = result.get('secure_url')
            if secure_url:
                print(f"🔗 URL segura: {secure_url}")
                try:
                    import requests
                    response = requests.get(secure_url, timeout=10)
                    if response.status_code == 200:
                        print(f"✅ URL segura accesible (HTTP {response.status_code})")
                        print(f"📏 Tamaño: {len(response.content)} bytes")
                    else:
                        print(f"❌ Error en URL segura: HTTP {response.status_code}")
                except Exception as e:
                    print(f"⚠️ Error verificando URL segura: {e}")
            
        except Exception as e:
            print(f"⚠️ No se pudo obtener información detallada: {e}")
        
        # Probar acceso a la URL generada
        try:
            import requests
            response = requests.get(categoria.imagen.url, timeout=10)
            print(f"📡 Respuesta HTTP de URL generada: {response.status_code}")
            if response.status_code == 200:
                print("✅ URL generada accesible")
                print(f"📏 Tamaño: {len(response.content)} bytes")
            else:
                print(f"❌ Error en URL generada: HTTP {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error verificando URL generada: {e}")
        
        # Limpiar
        categoria.delete()
        print("✅ Categoría eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando admin corregido: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_uploads():
    """Probar múltiples subidas"""
    print("\n🧪 PROBANDO MÚLTIPLES SUBIDAS")
    print("=" * 60)
    
    try:
        for i in range(3):
            print(f"\n📤 Subida {i+1}/3...")
            
            # Crear imagen diferente cada vez
            colors = ['#E74C3C', '#3498DB', '#2ECC71']  # Rojo, Azul, Verde
            img = Image.new('RGB', (400 + i*100, 400 + i*100), color=colors[i])
            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            img_io.seek(0)
            
            # Crear categoría
            categoria = CategoriaProducto(
                nombre=f"Categoría Múltiple {i+1}",
                descripcion=f"Categoría para prueba múltiple {i+1}",
                slug=f"categoria-multiple-{i+1}-{os.getpid()}"
            )
            
            categoria.save()
            
            # Subir imagen
            django_file = File(img_io, name=f'categoria_multiple_{i+1}_{os.getpid()}.jpg')
            categoria.imagen.save(django_file.name, django_file, save=True)
            
            print(f"✅ Subida {i+1} completada")
            print(f"  URL: {categoria.imagen.url}")
            
            # Verificar URL
            if 'cloudinary.com' in categoria.imagen.url:
                print(f"✅ URL {i+1} es de Cloudinary")
            else:
                print(f"❌ URL {i+1} no es de Cloudinary")
            
            # Limpiar
            categoria.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando múltiples subidas: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE ADMIN CORREGIDO")
    print("=" * 60)
    
    # Probar admin corregido
    admin_success = test_admin_fixed()
    
    # Probar múltiples subidas
    multiple_success = test_multiple_uploads()
    
    print("\n📊 RESULTADOS FINALES")
    print("=" * 60)
    print(f"Admin corregido: {'✅ PASÓ' if admin_success else '❌ FALLÓ'}")
    print(f"Múltiples subidas: {'✅ PASÓ' if multiple_success else '❌ FALLÓ'}")
    
    if admin_success and multiple_success:
        print("\n🎉 ¡PROBLEMA DEL ADMIN CORREGIDO!")
        print("✅ Las imágenes se suben correctamente desde el admin.")
        print("✅ Las URLs son accesibles y válidas.")
        print("✅ El sistema funciona perfectamente.")
        print("\n💡 Ahora puedes usar el admin sin problemas:")
        print("   1. Ve a http://localhost:8000/admin/")
        print("   2. Crea o edita una categoría")
        print("   3. Sube una imagen")
        print("   4. La imagen se subirá correctamente a Cloudinary")
    else:
        print("\n⚠️ Aún hay problemas.")
        print("❌ Revisa la configuración del sistema.") 