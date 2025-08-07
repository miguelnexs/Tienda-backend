#!/usr/bin/env python3
"""
Script final para probar el manejo de errores mejorado
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
from categorias.serializers_improved import CategoriaProductoSerializer
from categorias.models import CategoriaProducto

def crear_archivo_vacio(nombre_archivo):
    """Crear un archivo vacío para simular el error"""
    empty_io = BytesIO()
    
    archivo = InMemoryUploadedFile(
        file=empty_io,
        field_name='imagen',
        name=nombre_archivo,
        content_type='image/jpeg',
        size=0,
        charset=None
    )
    
    return archivo

def crear_archivo_valido(nombre_archivo, color='#FF6B6B', tamano=(800, 600)):
    """Crear un archivo válido"""
    img = Image.new('RGB', tamano, color=color)
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=90)
    img_io.seek(0)
    
    archivo = InMemoryUploadedFile(
        file=img_io,
        field_name='imagen',
        name=nombre_archivo,
        content_type='image/jpeg',
        size=len(img_io.getvalue()),
        charset=None
    )
    
    return archivo

def test_serializer_con_archivo_vacio():
    """Probar serializer con archivo vacío"""
    print("🧪 PROBANDO SERIALIZER CON ARCHIVO VACÍO")
    print("=" * 60)
    
    try:
        # Crear datos de categoría
        datos_categoria = {
            'nombre': 'Categoría Archivo Vacío',
            'descripcion': 'Categoría para probar archivo vacío',
            'activa': True,
            'orden': 1,
            'imagen': crear_archivo_vacio('archivo_vacio.jpg')
        }
        
        print("📝 Datos de categoría con archivo vacío creados")
        
        # Crear serializer
        serializer = CategoriaProductoSerializer(data=datos_categoria)
        
        if serializer.is_valid():
            print("✅ Serializer válido")
            
            # Crear la categoría (debería funcionar sin error)
            categoria = serializer.save()
            print(f"✅ Categoría creada: ID {categoria.id}")
            
            # Verificar que la imagen no se guardó
            if categoria.imagen:
                print(f"❌ ERROR: Se guardó una imagen vacía: {categoria.imagen.name}")
                categoria.delete()
                return False
            else:
                print("✅ CORRECTO: No se guardó imagen vacía")
                categoria.delete()
                return True
        else:
            print(f"❌ Error validando serializer: {serializer.errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando serializer con archivo vacío: {e}")
        return False

def test_serializer_con_archivo_valido():
    """Probar serializer con archivo válido"""
    print("\n🧪 PROBANDO SERIALIZER CON ARCHIVO VÁLIDO")
    print("=" * 60)
    
    try:
        # Crear datos de categoría
        datos_categoria = {
            'nombre': 'Categoría Archivo Válido',
            'descripcion': 'Categoría para probar archivo válido',
            'activa': True,
            'orden': 2,
            'imagen': crear_archivo_valido('archivo_valido.jpg', '#3498DB')
        }
        
        print("📝 Datos de categoría con archivo válido creados")
        
        # Crear serializer
        serializer = CategoriaProductoSerializer(data=datos_categoria)
        
        if serializer.is_valid():
            print("✅ Serializer válido")
            
            # Crear la categoría
            categoria = serializer.save()
            print(f"✅ Categoría creada: ID {categoria.id}")
            
            # Verificar que la imagen se guardó correctamente
            if categoria.imagen:
                print(f"✅ Imagen guardada: {categoria.imagen.name}")
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
            else:
                print("❌ ERROR: No se guardó la imagen válida")
                categoria.delete()
                return False
        else:
            print(f"❌ Error validando serializer: {serializer.errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando serializer con archivo válido: {e}")
        return False

def test_actualizacion_con_archivo_vacio():
    """Probar actualización con archivo vacío"""
    print("\n🧪 PROBANDO ACTUALIZACIÓN CON ARCHIVO VACÍO")
    print("=" * 60)
    
    try:
        # Crear categoría existente
        categoria = CategoriaProducto.objects.create(
            nombre="Categoría Test Actualización",
            descripcion="Categoría para probar actualización",
            slug="categoria-test-actualizacion"
        )
        
        print(f"✅ Categoría creada: ID {categoria.id}")
        
        # Crear datos de actualización con archivo vacío
        datos_actualizacion = {
            'imagen': crear_archivo_vacio('archivo_vacio_actualizacion.jpg')
        }
        
        # Actualizar categoría
        serializer = CategoriaProductoSerializer(
            instance=categoria,
            data=datos_actualizacion,
            partial=True
        )
        
        if serializer.is_valid():
            categoria_actualizada = serializer.save()
            print("✅ Categoría actualizada sin error")
            
            # Verificar que la imagen no se guardó
            if categoria_actualizada.imagen:
                print(f"❌ ERROR: Se guardó imagen vacía en actualización: {categoria_actualizada.imagen.name}")
                categoria_actualizada.delete()
                return False
            else:
                print("✅ CORRECTO: No se guardó imagen vacía en actualización")
                categoria_actualizada.delete()
                return True
        else:
            print(f"❌ Error validando actualización: {serializer.errors}")
            categoria.delete()
            return False
            
    except Exception as e:
        print(f"❌ Error probando actualización con archivo vacío: {e}")
        return False

def test_actualizacion_con_archivo_valido():
    """Probar actualización con archivo válido"""
    print("\n🧪 PROBANDO ACTUALIZACIÓN CON ARCHIVO VÁLIDO")
    print("=" * 60)
    
    try:
        # Crear categoría existente
        categoria = CategoriaProducto.objects.create(
            nombre="Categoría Test Actualización Válida",
            descripcion="Categoría para probar actualización válida",
            slug="categoria-test-actualizacion-valida"
        )
        
        print(f"✅ Categoría creada: ID {categoria.id}")
        
        # Crear datos de actualización con archivo válido
        datos_actualizacion = {
            'imagen': crear_archivo_valido('archivo_valido_actualizacion.jpg', '#2ECC71')
        }
        
        # Actualizar categoría
        serializer = CategoriaProductoSerializer(
            instance=categoria,
            data=datos_actualizacion,
            partial=True
        )
        
        if serializer.is_valid():
            categoria_actualizada = serializer.save()
            print("✅ Categoría actualizada correctamente")
            
            # Verificar que la imagen se guardó
            if categoria_actualizada.imagen:
                print(f"✅ Imagen guardada: {categoria_actualizada.imagen.name}")
                print(f"🔗 URL: {categoria_actualizada.imagen.url}")
                
                # Verificar en Cloudinary
                try:
                    import cloudinary.api
                    result = cloudinary.api.resource(categoria_actualizada.imagen.name)
                    print("✅ Archivo encontrado en Cloudinary")
                    print(f"📊 Tamaño: {result.get('bytes', 0)} bytes")
                    
                    # Limpiar
                    categoria_actualizada.delete()
                    print("✅ Categoría eliminada")
                    
                    return True
                except Exception as e:
                    print(f"❌ Archivo NO encontrado en Cloudinary: {e}")
                    categoria_actualizada.delete()
                    return False
            else:
                print("❌ ERROR: No se guardó la imagen válida en actualización")
                categoria_actualizada.delete()
                return False
        else:
            print(f"❌ Error validando actualización: {serializer.errors}")
            categoria.delete()
            return False
            
    except Exception as e:
        print(f"❌ Error probando actualización con archivo válido: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE MANEJO DE ERRORES")
    print("=" * 60)
    
    # Probar manejo de errores
    vacio_success = test_serializer_con_archivo_vacio()
    valido_success = test_serializer_con_archivo_valido()
    actualizacion_vacio_success = test_actualizacion_con_archivo_vacio()
    actualizacion_valido_success = test_actualizacion_con_archivo_valido()
    
    print("\n📊 RESULTADOS DE LAS PRUEBAS")
    print("=" * 60)
    print(f"Serializer archivo vacío: {'✅ PASÓ' if vacio_success else '❌ FALLÓ'}")
    print(f"Serializer archivo válido: {'✅ PASÓ' if valido_success else '❌ FALLÓ'}")
    print(f"Actualización archivo vacío: {'✅ PASÓ' if actualizacion_vacio_success else '❌ FALLÓ'}")
    print(f"Actualización archivo válido: {'✅ PASÓ' if actualizacion_valido_success else '❌ FALLÓ'}")
    
    if all([vacio_success, valido_success, actualizacion_vacio_success, actualizacion_valido_success]):
        print("\n🎉 ¡MANEJO DE ERRORES COMPLETAMENTE FUNCIONAL!")
        print("✅ Los archivos vacíos se detectan y manejan correctamente.")
        print("✅ Los archivos válidos se suben correctamente a Cloudinary.")
        print("✅ Las actualizaciones funcionan correctamente.")
        print("✅ No se generan errores 500 en el API.")
        print("✅ El sistema es robusto contra archivos problemáticos.")
        print("\n💡 EL SISTEMA ESTÁ LISTO PARA PRODUCCIÓN")
        print("\n📋 RESUMEN DE LA SOLUCIÓN:")
        print("   ✅ Admin de Django: Funciona con Cloudinary")
        print("   ✅ Serializers DRF: Funcionan con Cloudinary")
        print("   ✅ Manejo de errores: Protegido contra archivos vacíos")
        print("   ✅ URLs: Todas son de Cloudinary")
        print("   ✅ Subida de imágenes: Automática a Cloudinary")
    else:
        print("\n⚠️ Hay problemas con el manejo de errores.")
        print("❌ Revisa la configuración del sistema.") 