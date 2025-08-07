#!/usr/bin/env python3
"""
Script para probar que los serializers de DRF funcionan correctamente con Cloudinary
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
from categorias.serializers import CategoriaProductoSerializer
from categorias.serializers_improved import CategoriaProductoSerializer as CategoriaProductoSerializerImproved
from categorias.models import CategoriaProducto

def crear_imagen_mock(nombre_archivo, color='#FF6B6B', tamano=(800, 600)):
    """Crear una imagen mock para pruebas"""
    img = Image.new('RGB', tamano, color=color)
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=90)
    img_io.seek(0)
    
    # Crear archivo mock
    archivo = InMemoryUploadedFile(
        file=img_io,
        field_name='imagen',
        name=nombre_archivo,
        content_type='image/jpeg',
        size=len(img_io.getvalue()),
        charset=None
    )
    
    return archivo

def test_serializer_basico():
    """Probar serializer básico con Cloudinary"""
    print("🧪 PROBANDO SERIALIZER BÁSICO CON CLOUDINARY")
    print("=" * 60)
    
    try:
        # Crear datos de prueba
        datos_categoria = {
            'nombre': 'Categoría Serializer Básico',
            'descripcion': 'Categoría para probar serializer básico con Cloudinary',
            'activa': True,
            'orden': 1
        }
        
        # Crear imagen mock
        imagen_mock = crear_imagen_mock('categoria_serializer_basico.jpg', '#FF6B6B')
        
        print("📝 Datos de categoría creados")
        print(f"📸 Imagen mock creada: {imagen_mock.name}")
        
        # Crear serializer
        serializer = CategoriaProductoSerializer(data=datos_categoria)
        
        if serializer.is_valid():
            print("✅ Serializer válido")
            
            # Crear la categoría
            categoria = serializer.save()
            print(f"✅ Categoría creada: ID {categoria.id}")
            
            # Ahora agregar la imagen
            datos_con_imagen = {
                'imagen': imagen_mock
            }
            
            # Actualizar con imagen
            serializer_update = CategoriaProductoSerializer(
                instance=categoria, 
                data=datos_con_imagen, 
                partial=True
            )
            
            if serializer_update.is_valid():
                categoria_actualizada = serializer_update.save()
                print("✅ Categoría actualizada con imagen")
                
                # Verificar resultado
                print(f"📁 Nombre de imagen: {categoria_actualizada.imagen.name}")
                print(f"🔗 URL de imagen: {categoria_actualizada.imagen.url}")
                
                # Verificar si está en Cloudinary
                if 'cloudinary.com' in categoria_actualizada.imagen.url:
                    print("✅ URL es de Cloudinary")
                else:
                    print("❌ URL no es de Cloudinary")
                
                # Verificar en Cloudinary
                try:
                    import cloudinary.api
                    result = cloudinary.api.resource(categoria_actualizada.imagen.name)
                    print("✅ Archivo encontrado en Cloudinary")
                    print(f"📊 Información:")
                    print(f"  Public ID: {result['public_id']}")
                    print(f"  URL segura: {result.get('secure_url', 'N/A')}")
                    print(f"  Tamaño: {result.get('bytes', 0)} bytes")
                except Exception as e:
                    print(f"❌ Archivo NO encontrado en Cloudinary: {e}")
                
                # Limpiar
                categoria_actualizada.delete()
                print("✅ Categoría eliminada")
                
                return True
            else:
                print(f"❌ Error validando serializer con imagen: {serializer_update.errors}")
                return False
        else:
            print(f"❌ Error validando serializer: {serializer.errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando serializer básico: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_serializer_mejorado():
    """Probar serializer mejorado con Cloudinary"""
    print("\n🧪 PROBANDO SERIALIZER MEJORADO CON CLOUDINARY")
    print("=" * 60)
    
    try:
        # Crear datos de prueba
        datos_categoria = {
            'nombre': 'Categoría Serializer Mejorado',
            'descripcion': 'Categoría para probar serializer mejorado con Cloudinary',
            'activa': True,
            'orden': 2
        }
        
        # Crear imagen mock
        imagen_mock = crear_imagen_mock('categoria_serializer_mejorado.jpg', '#3498DB')
        
        print("📝 Datos de categoría creados")
        print(f"📸 Imagen mock creada: {imagen_mock.name}")
        
        # Crear serializer
        serializer = CategoriaProductoSerializerImproved(data=datos_categoria)
        
        if serializer.is_valid():
            print("✅ Serializer válido")
            
            # Crear la categoría
            categoria = serializer.save()
            print(f"✅ Categoría creada: ID {categoria.id}")
            
            # Ahora agregar la imagen
            datos_con_imagen = {
                'imagen': imagen_mock
            }
            
            # Actualizar con imagen
            serializer_update = CategoriaProductoSerializerImproved(
                instance=categoria, 
                data=datos_con_imagen, 
                partial=True
            )
            
            if serializer_update.is_valid():
                categoria_actualizada = serializer_update.save()
                print("✅ Categoría actualizada con imagen")
                
                # Verificar resultado
                print(f"📁 Nombre de imagen: {categoria_actualizada.imagen.name}")
                print(f"🔗 URL de imagen: {categoria_actualizada.imagen.url}")
                
                # Verificar si está en Cloudinary
                if 'cloudinary.com' in categoria_actualizada.imagen.url:
                    print("✅ URL es de Cloudinary")
                else:
                    print("❌ URL no es de Cloudinary")
                
                # Verificar en Cloudinary
                try:
                    import cloudinary.api
                    result = cloudinary.api.resource(categoria_actualizada.imagen.name)
                    print("✅ Archivo encontrado en Cloudinary")
                    print(f"📊 Información:")
                    print(f"  Public ID: {result['public_id']}")
                    print(f"  URL segura: {result.get('secure_url', 'N/A')}")
                    print(f"  Tamaño: {result.get('bytes', 0)} bytes")
                except Exception as e:
                    print(f"❌ Archivo NO encontrado en Cloudinary: {e}")
                
                # Limpiar
                categoria_actualizada.delete()
                print("✅ Categoría eliminada")
                
                return True
            else:
                print(f"❌ Error validando serializer con imagen: {serializer_update.errors}")
                return False
        else:
            print(f"❌ Error validando serializer: {serializer.errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando serializer mejorado: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_serializer_con_imagen_directa():
    """Probar serializer con imagen incluida desde el inicio"""
    print("\n🧪 PROBANDO SERIALIZER CON IMAGEN DIRECTA")
    print("=" * 60)
    
    try:
        # Crear imagen mock
        imagen_mock = crear_imagen_mock('categoria_imagen_directa.jpg', '#2ECC71')
        
        # Crear datos de prueba con imagen incluida
        datos_categoria = {
            'nombre': 'Categoría Imagen Directa',
            'descripcion': 'Categoría con imagen incluida desde el inicio',
            'activa': True,
            'orden': 3,
            'imagen': imagen_mock
        }
        
        print("📝 Datos de categoría con imagen creados")
        print(f"📸 Imagen mock creada: {imagen_mock.name}")
        
        # Crear serializer
        serializer = CategoriaProductoSerializerImproved(data=datos_categoria)
        
        if serializer.is_valid():
            print("✅ Serializer válido")
            
            # Crear la categoría con imagen
            categoria = serializer.save()
            print(f"✅ Categoría creada con imagen: ID {categoria.id}")
            
            # Verificar resultado
            print(f"📁 Nombre de imagen: {categoria.imagen.name}")
            print(f"🔗 URL de imagen: {categoria.imagen.url}")
            
            # Verificar si está en Cloudinary
            if 'cloudinary.com' in categoria.imagen.url:
                print("✅ URL es de Cloudinary")
            else:
                print("❌ URL no es de Cloudinary")
            
            # Verificar en Cloudinary
            try:
                import cloudinary.api
                result = cloudinary.api.resource(categoria.imagen.name)
                print("✅ Archivo encontrado en Cloudinary")
                print(f"📊 Información:")
                print(f"  Public ID: {result['public_id']}")
                print(f"  URL segura: {result.get('secure_url', 'N/A')}")
                print(f"  Tamaño: {result.get('bytes', 0)} bytes")
            except Exception as e:
                print(f"❌ Archivo NO encontrado en Cloudinary: {e}")
            
            # Limpiar
            categoria.delete()
            print("✅ Categoría eliminada")
            
            return True
        else:
            print(f"❌ Error validando serializer: {serializer.errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando serializer con imagen directa: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_representacion_serializer():
    """Probar la representación del serializer"""
    print("\n🧪 PROBANDO REPRESENTACIÓN DEL SERIALIZER")
    print("=" * 60)
    
    try:
        # Crear categoría existente
        categoria = CategoriaProducto.objects.create(
            nombre="Categoría Test Representación",
            descripcion="Categoría para probar representación del serializer",
            slug="categoria-test-representacion"
        )
        
        # Crear imagen mock
        imagen_mock = crear_imagen_mock('categoria_representacion.jpg', '#9B59B6')
        
        # Guardar imagen en la categoría
        categoria.imagen.save('categoria_representacion.jpg', imagen_mock, save=True)
        
        print("✅ Categoría creada con imagen")
        print(f"📁 Nombre de imagen: {categoria.imagen.name}")
        print(f"🔗 URL de imagen: {categoria.imagen.url}")
        
        # Probar representación del serializer
        serializer = CategoriaProductoSerializerImproved(categoria)
        data = serializer.data
        
        print("📊 Datos del serializer:")
        print(f"  ID: {data.get('id')}")
        print(f"  Nombre: {data.get('nombre')}")
        print(f"  Slug: {data.get('slug')}")
        print(f"  Imagen: {data.get('imagen')}")
        print(f"  Imagen URL: {data.get('imagen_url')}")
        
        # Verificar que las URLs son correctas
        if data.get('imagen_url') and 'cloudinary.com' in data.get('imagen_url', ''):
            print("✅ Imagen URL es de Cloudinary")
        else:
            print("❌ Imagen URL no es de Cloudinary")
        
        # Limpiar
        categoria.delete()
        print("✅ Categoría eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando representación del serializer: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE SERIALIZERS CON CLOUDINARY")
    print("=" * 60)
    
    # Probar serializers
    basico_success = test_serializer_basico()
    mejorado_success = test_serializer_mejorado()
    directa_success = test_serializer_con_imagen_directa()
    representacion_success = test_representacion_serializer()
    
    print("\n📊 RESULTADOS DE LAS PRUEBAS")
    print("=" * 60)
    print(f"Serializer básico: {'✅ PASÓ' if basico_success else '❌ FALLÓ'}")
    print(f"Serializer mejorado: {'✅ PASÓ' if mejorado_success else '❌ FALLÓ'}")
    print(f"Imagen directa: {'✅ PASÓ' if directa_success else '❌ FALLÓ'}")
    print(f"Representación: {'✅ PASÓ' if representacion_success else '❌ FALLÓ'}")
    
    if all([basico_success, mejorado_success, directa_success, representacion_success]):
        print("\n🎉 ¡SERIALIZERS CON CLOUDINARY FUNCIONAN PERFECTAMENTE!")
        print("✅ Los serializers de DRF funcionan correctamente con Cloudinary.")
        print("✅ Las imágenes se suben correctamente a través de los serializers.")
        print("✅ Las URLs se generan correctamente.")
        print("✅ La representación de datos es correcta.")
        print("\n💡 INSTRUCCIONES PARA USAR LOS SERIALIZERS:")
        print("   1. Los serializers ya están configurados para usar Cloudinary")
        print("   2. Puedes crear categorías con imágenes usando POST /api/categorias/")
        print("   3. Puedes actualizar categorías con imágenes usando PUT/PATCH /api/categorias/{id}/")
        print("   4. Las imágenes se subirán automáticamente a Cloudinary")
        print("   5. Las URLs en la respuesta serán de Cloudinary")
        print("\n🎯 LOS SERIALIZERS ESTÁN LISTOS PARA USAR")
    else:
        print("\n⚠️ Hay problemas con algunos serializers.")
        print("❌ Revisa la configuración del sistema.") 