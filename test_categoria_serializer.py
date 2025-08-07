#!/usr/bin/env python
"""
Script para probar el serializers de categorías
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

def test_categoria_serializer():
    """Probar el serializers de categorías"""
    
    print("🧪 PROBANDO SERIALIZER DE CATEGORÍAS")
    print("="*50)
    
    try:
        from categorias.serializers import CategoriaProductoSerializer
        from categorias.models import CategoriaProducto
        
        # Datos de prueba
        test_data = {
            'nombre': 'Test Categoría Serializer',
            'descripcion': 'Prueba del serializers corregido',
            'activa': True,
            'orden': 999
        }
        
        print("📋 Datos de prueba:")
        print(f"  Nombre: {test_data['nombre']}")
        print(f"  Descripción: {test_data['descripcion']}")
        print(f"  Activa: {test_data['activa']}")
        print(f"  Orden: {test_data['orden']}")
        
        # Crear serializer
        serializer = CategoriaProductoSerializer(data=test_data)
        
        print("\n🔍 Validando datos...")
        if serializer.is_valid():
            print("✅ Datos válidos")
            print("📊 Datos validados:")
            for field, value in serializer.validated_data.items():
                print(f"  {field}: {value}")
            
            # Crear categoría
            print("\n🚀 Creando categoría...")
            categoria = serializer.save()
            
            print("✅ Categoría creada exitosamente!")
            print(f"📋 ID: {categoria.id}")
            print(f"📋 Nombre: {categoria.nombre}")
            print(f"📋 Slug: {categoria.slug}")
            print(f"📋 Activa: {categoria.activa}")
            print(f"📋 Orden: {categoria.orden}")
            
            # Limpiar categoría de prueba
            categoria.delete()
            print("🧹 Categoría de prueba eliminada")
            
            return True
            
        else:
            print("❌ Datos inválidos")
            print("📊 Errores:")
            for field, errors in serializer.errors.items():
                print(f"  {field}: {errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba: {str(e)}")
        return False

def test_categoria_with_image():
    """Probar categoría con imagen"""
    
    print("\n" + "="*50)
    print("🖼️ PROBANDO CATEGORÍA CON IMAGEN")
    print("="*50)
    
    try:
        from categorias.serializers import CategoriaProductoSerializer
        from categorias.models import CategoriaProducto
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Crear imagen de prueba real (JPEG válido)
        # Datos de una imagen JPEG mínima válida
        jpeg_header = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
        
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            jpeg_header,
            content_type="image/jpeg"
        )
        
        # Datos de prueba con imagen
        test_data = {
            'nombre': 'Test Categoría con Imagen',
            'descripcion': 'Prueba del serializers con imagen',
            'activa': True,
            'orden': 998,
            'imagen': image_file
        }
        
        print("📋 Datos de prueba con imagen:")
        print(f"  Nombre: {test_data['nombre']}")
        print(f"  Imagen: {test_data['imagen'].name}")
        
        # Crear serializer
        serializer = CategoriaProductoSerializer(data=test_data)
        
        print("\n🔍 Validando datos con imagen...")
        if serializer.is_valid():
            print("✅ Datos válidos")
            
            # Crear categoría
            print("\n🚀 Creando categoría con imagen...")
            categoria = serializer.save()
            
            print("✅ Categoría con imagen creada exitosamente!")
            print(f"📋 ID: {categoria.id}")
            print(f"📋 Nombre: {categoria.nombre}")
            print(f"📋 Imagen: {categoria.imagen.name if categoria.imagen else 'Sin imagen'}")
            
            # Limpiar categoría de prueba
            categoria.delete()
            print("🧹 Categoría de prueba eliminada")
            
            return True
            
        else:
            print("❌ Datos inválidos")
            print("📊 Errores:")
            for field, errors in serializer.errors.items():
                print(f"  {field}: {errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba con imagen: {str(e)}")
        return False

def test_categoria_without_image():
    """Probar categoría sin imagen (caso más común)"""
    
    print("\n" + "="*50)
    print("📝 PROBANDO CATEGORÍA SIN IMAGEN")
    print("="*50)
    
    try:
        from categorias.serializers import CategoriaProductoSerializer
        from categorias.models import CategoriaProducto
        
        # Datos de prueba sin imagen
        test_data = {
            'nombre': 'Test Categoría Sin Imagen',
            'descripcion': 'Prueba del serializers sin imagen',
            'activa': True,
            'orden': 997
        }
        
        print("📋 Datos de prueba sin imagen:")
        print(f"  Nombre: {test_data['nombre']}")
        print(f"  Descripción: {test_data['descripcion']}")
        
        # Crear serializer
        serializer = CategoriaProductoSerializer(data=test_data)
        
        print("\n🔍 Validando datos sin imagen...")
        if serializer.is_valid():
            print("✅ Datos válidos")
            
            # Crear categoría
            print("\n🚀 Creando categoría sin imagen...")
            categoria = serializer.save()
            
            print("✅ Categoría sin imagen creada exitosamente!")
            print(f"📋 ID: {categoria.id}")
            print(f"📋 Nombre: {categoria.nombre}")
            print(f"📋 Slug: {categoria.slug}")
            print(f"📋 Imagen: {'Sí' if categoria.imagen else 'No'}")
            
            # Limpiar categoría de prueba
            categoria.delete()
            print("🧹 Categoría de prueba eliminada")
            
            return True
            
        else:
            print("❌ Datos inválidos")
            print("📊 Errores:")
            for field, errors in serializer.errors.items():
                print(f"  {field}: {errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba sin imagen: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA DEL SERIALIZER DE CATEGORÍAS")
    print("="*50)
    
    # Probar serializer básico
    basic_ok = test_categoria_serializer()
    
    # Probar serializer sin imagen
    no_image_ok = test_categoria_without_image()
    
    # Probar serializer con imagen
    image_ok = test_categoria_with_image()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    print(f"✅ Serializer básico: {'EXITOSA' if basic_ok else 'FALLIDA'}")
    print(f"✅ Serializer sin imagen: {'EXITOSA' if no_image_ok else 'FALLIDA'}")
    print(f"✅ Serializer con imagen: {'EXITOSA' if image_ok else 'FALLIDA'}")
    
    # Conclusión
    print("\n" + "="*50)
    print("🎯 CONCLUSIÓN")
    print("="*50)
    
    if basic_ok and no_image_ok and image_ok:
        print("🎉 ¡El serializers de categorías funciona perfectamente!")
        print("✅ Puede crear categorías básicas")
        print("✅ Puede crear categorías sin imagen")
        print("✅ Puede crear categorías con imagen")
        print("✅ El serializers está completamente corregido")
    elif basic_ok and no_image_ok:
        print("✅ El serializers básico funciona")
        print("✅ Puede crear categorías sin imagen")
        print("⚠️ Pero hay problemas con las imágenes")
    elif basic_ok:
        print("✅ El serializers básico funciona")
        print("❌ Pero hay problemas con las categorías")
    else:
        print("❌ Hay problemas fundamentales con el serializers")
        print("🔧 Revisar la configuración")

if __name__ == '__main__':
    main() 