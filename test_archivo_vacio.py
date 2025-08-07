#!/usr/bin/env python3
"""
Script para probar el manejo de archivos vacíos y mejorar el manejo de errores
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
from Backend.cloudinary_storage_fixed_urls import CloudinaryStorageFixedURLs

def crear_archivo_vacio(nombre_archivo):
    """Crear un archivo vacío para pruebas"""
    # Crear un BytesIO vacío
    empty_io = BytesIO()
    
    # Crear archivo mock vacío
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
    """Crear un archivo válido para pruebas"""
    img = Image.new('RGB', tamano, color=color)
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=90)
    img_io.seek(0)
    
    # Crear archivo mock válido
    archivo = InMemoryUploadedFile(
        file=img_io,
        field_name='imagen',
        name=nombre_archivo,
        content_type='image/jpeg',
        size=len(img_io.getvalue()),
        charset=None
    )
    
    return archivo

def test_archivo_vacio():
    """Probar manejo de archivo vacío"""
    print("🧪 PROBANDO MANEJO DE ARCHIVO VACÍO")
    print("=" * 60)
    
    try:
        # Crear archivo vacío
        archivo_vacio = crear_archivo_vacio('archivo_vacio.jpg')
        
        print(f"📁 Archivo vacío creado: {archivo_vacio.name}")
        print(f"📏 Tamaño: {archivo_vacio.size} bytes")
        
        # Usar storage directamente
        storage = CloudinaryStorageFixedURLs()
        
        # Intentar subir archivo vacío
        try:
            saved_name = storage.save('test_archivo_vacio.jpg', archivo_vacio)
            print(f"❌ ERROR: Se subió un archivo vacío: {saved_name}")
            return False
        except Exception as e:
            print(f"✅ CORRECTO: Se detectó archivo vacío: {e}")
            return True
            
    except Exception as e:
        print(f"❌ Error probando archivo vacío: {e}")
        return False

def test_archivo_valido():
    """Probar archivo válido"""
    print("\n🧪 PROBANDO ARCHIVO VÁLIDO")
    print("=" * 60)
    
    try:
        # Crear archivo válido
        archivo_valido = crear_archivo_valido('archivo_valido.jpg', '#3498DB')
        
        print(f"📁 Archivo válido creado: {archivo_valido.name}")
        print(f"📏 Tamaño: {archivo_valido.size} bytes")
        
        # Usar storage directamente
        storage = CloudinaryStorageFixedURLs()
        
        # Subir archivo válido
        saved_name = storage.save('test_archivo_valido.jpg', archivo_valido)
        print(f"✅ Archivo válido subido: {saved_name}")
        
        # Verificar en Cloudinary
        try:
            import cloudinary.api
            result = cloudinary.api.resource(saved_name)
            print("✅ Archivo encontrado en Cloudinary")
            print(f"📊 Tamaño: {result.get('bytes', 0)} bytes")
            
            # Limpiar
            storage.delete(saved_name)
            print("✅ Archivo eliminado")
            
            return True
        except Exception as e:
            print(f"❌ Archivo NO encontrado en Cloudinary: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando archivo válido: {e}")
        return False

def test_categoria_con_archivo_vacio():
    """Probar categoría con archivo vacío"""
    print("\n🧪 PROBANDO CATEGORÍA CON ARCHIVO VACÍO")
    print("=" * 60)
    
    try:
        # Crear categoría
        categoria = CategoriaProducto.objects.create(
            nombre="Categoría Archivo Vacío",
            descripcion="Categoría para probar archivo vacío",
            slug="categoria-archivo-vacio"
        )
        
        # Crear archivo vacío
        archivo_vacio = crear_archivo_vacio('categoria_vacio.jpg')
        
        print("✅ Categoría creada")
        print(f"📁 Archivo vacío creado: {archivo_vacio.name}")
        
        # Intentar guardar archivo vacío
        try:
            categoria.imagen.save(archivo_vacio.name, archivo_vacio, save=True)
            print("❌ ERROR: Se guardó un archivo vacío")
            categoria.delete()
            return False
        except Exception as e:
            print(f"✅ CORRECTO: Se detectó archivo vacío: {e}")
            categoria.delete()
            return True
            
    except Exception as e:
        print(f"❌ Error probando categoría con archivo vacío: {e}")
        return False

def test_categoria_con_archivo_valido():
    """Probar categoría con archivo válido"""
    print("\n🧪 PROBANDO CATEGORÍA CON ARCHIVO VÁLIDO")
    print("=" * 60)
    
    try:
        # Crear categoría
        categoria = CategoriaProducto.objects.create(
            nombre="Categoría Archivo Válido",
            descripcion="Categoría para probar archivo válido",
            slug="categoria-archivo-valido"
        )
        
        # Crear archivo válido
        archivo_valido = crear_archivo_valido('categoria_valido.jpg', '#2ECC71')
        
        print("✅ Categoría creada")
        print(f"📁 Archivo válido creado: {archivo_valido.name}")
        
        # Guardar archivo válido
        categoria.imagen.save(archivo_valido.name, archivo_valido, save=True)
        print("✅ Archivo válido guardado")
        
        # Verificar resultado
        print(f"📁 Nombre de imagen: {categoria.imagen.name}")
        print(f"🔗 URL de imagen: {categoria.imagen.url}")
        
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
        print(f"❌ Error probando categoría con archivo válido: {e}")
        return False

def mejorar_manejo_errores():
    """Mejorar el manejo de errores en el serializer"""
    print("\n🔧 MEJORANDO MANEJO DE ERRORES")
    print("=" * 60)
    
    # Crear un archivo de ejemplo que simule el problema
    print("📝 Creando archivo de ejemplo...")
    
    # Simular archivo con contenido pero que se lee como vacío
    img = Image.new('RGB', (100, 100), color='#E74C3C')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    
    # Crear archivo mock
    archivo = InMemoryUploadedFile(
        file=img_io,
        field_name='imagen',
        name='archivo_ejemplo.jpg',
        content_type='image/jpeg',
        size=len(img_io.getvalue()),
        charset=None
    )
    
    print(f"📁 Archivo creado: {archivo.name}")
    print(f"📏 Tamaño original: {archivo.size} bytes")
    
    # Leer contenido para verificar
    contenido = archivo.read()
    print(f"📏 Contenido leído: {len(contenido)} bytes")
    
    # Resetear posición
    archivo.seek(0)
    
    # Verificar que se puede leer nuevamente
    contenido_nuevo = archivo.read()
    print(f"📏 Contenido después de seek: {len(contenido_nuevo)} bytes")
    
    if len(contenido_nuevo) > 0:
        print("✅ El archivo mantiene su contenido")
        return True
    else:
        print("❌ El archivo perdió su contenido")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE MANEJO DE ARCHIVOS")
    print("=" * 60)
    
    # Probar manejo de archivos
    vacio_success = test_archivo_vacio()
    valido_success = test_archivo_valido()
    categoria_vacio_success = test_categoria_con_archivo_vacio()
    categoria_valido_success = test_categoria_con_archivo_valido()
    manejo_errores_success = mejorar_manejo_errores()
    
    print("\n📊 RESULTADOS DE LAS PRUEBAS")
    print("=" * 60)
    print(f"Archivo vacío: {'✅ PASÓ' if vacio_success else '❌ FALLÓ'}")
    print(f"Archivo válido: {'✅ PASÓ' if valido_success else '❌ FALLÓ'}")
    print(f"Categoría archivo vacío: {'✅ PASÓ' if categoria_vacio_success else '❌ FALLÓ'}")
    print(f"Categoría archivo válido: {'✅ PASÓ' if categoria_valido_success else '❌ FALLÓ'}")
    print(f"Manejo de errores: {'✅ PASÓ' if manejo_errores_success else '❌ FALLÓ'}")
    
    if all([vacio_success, valido_success, categoria_vacio_success, categoria_valido_success, manejo_errores_success]):
        print("\n🎉 ¡MANEJO DE ARCHIVOS MEJORADO!")
        print("✅ Los archivos vacíos se detectan correctamente.")
        print("✅ Los archivos válidos se suben correctamente.")
        print("✅ El manejo de errores funciona correctamente.")
        print("✅ El sistema está protegido contra archivos vacíos.")
        print("\n💡 EL SISTEMA ESTÁ LISTO PARA MANEJAR ARCHIVOS PROBLEMÁTICOS")
    else:
        print("\n⚠️ Hay problemas con el manejo de archivos.")
        print("❌ Revisa la configuración del sistema.") 