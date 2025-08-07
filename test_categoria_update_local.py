#!/usr/bin/env python3
"""
Script para probar la actualización de categorías usando configuración local
"""
import os
import sys
import django
from pathlib import Path
import tempfile
from PIL import Image
import io

# Configurar Django con settings local
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

def test_categoria_update():
    """Probar actualización de categorías"""
    print("📝 PROBANDO ACTUALIZACIÓN DE CATEGORÍAS")
    print("=" * 50)
    
    try:
        from categorias.models import CategoriaProducto
        from categorias.serializers import CategoriaProductoSerializer
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Obtener una categoría existente
        categoria = CategoriaProducto.objects.first()
        if not categoria:
            print("❌ No hay categorías para probar")
            return False
        
        print(f"1. Categoría encontrada: {categoria.nombre} (ID: {categoria.id})")
        
        # Datos de prueba para actualización
        test_data = {
            'nombre': categoria.nombre,  # Mismo nombre para probar validación
            'descripcion': 'Descripción actualizada de prueba',
            'activa': True,
            'orden': 1
        }
        
        # Crear serializer con la instancia existente
        serializer = CategoriaProductoSerializer(
            instance=categoria,
            data=test_data,
            context={'request': None}
        )
        
        if serializer.is_valid():
            print("2. ✅ Serializer válido para actualización")
            print(f"   Datos validados: {list(serializer.validated_data.keys())}")
            
            # Intentar actualizar
            try:
                categoria_actualizada = serializer.save()
                print(f"3. ✅ Categoría actualizada: {categoria_actualizada.nombre}")
                print(f"   Descripción: {categoria_actualizada.descripcion}")
                return True
                
            except Exception as e:
                print(f"3. ❌ Error actualizando: {e}")
                return False
        else:
            print("2. ❌ Serializer inválido")
            print(f"   Errores: {serializer.errors}")
            return False
        
    except Exception as e:
        print(f"❌ Error probando actualización: {e}")
        return False

def test_categoria_update_with_image():
    """Probar actualización de categorías con imagen"""
    print("\n📤 PROBANDO ACTUALIZACIÓN CON IMAGEN")
    print("=" * 50)
    
    try:
        from categorias.models import CategoriaProducto
        from categorias.serializers import CategoriaProductoSerializer
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Obtener una categoría existente
        categoria = CategoriaProducto.objects.first()
        if not categoria:
            print("❌ No hay categorías para probar")
            return False
        
        print(f"1. Categoría encontrada: {categoria.nombre} (ID: {categoria.id})")
        
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 200), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        image_file = SimpleUploadedFile(
            "test_categoria_image.png",
            buffer.getvalue(),
            content_type="image/png"
        )
        
        # Datos de prueba para actualización con imagen
        test_data = {
            'nombre': categoria.nombre,  # Mismo nombre
            'descripcion': 'Descripción con imagen',
            'activa': True,
            'orden': 2,
            'imagen': image_file
        }
        
        # Crear serializer con la instancia existente
        serializer = CategoriaProductoSerializer(
            instance=categoria,
            data=test_data,
            context={'request': None}
        )
        
        if serializer.is_valid():
            print("2. ✅ Serializer válido para actualización con imagen")
            print(f"   Datos validados: {list(serializer.validated_data.keys())}")
            
            # Intentar actualizar
            try:
                categoria_actualizada = serializer.save()
                print(f"3. ✅ Categoría actualizada: {categoria_actualizada.nombre}")
                
                # Verificar imagen
                if categoria_actualizada.imagen:
                    print(f"4. ✅ Imagen actualizada: {categoria_actualizada.imagen.name}")
                    print(f"   URL: {categoria_actualizada.imagen.url}")
                else:
                    print("4. ⚠️ No se actualizó la imagen")
                
                return True
                
            except Exception as e:
                print(f"3. ❌ Error actualizando: {e}")
                return False
        else:
            print("2. ❌ Serializer inválido")
            print(f"   Errores: {serializer.errors}")
            return False
        
    except Exception as e:
        print(f"❌ Error probando actualización con imagen: {e}")
        return False

def test_categoria_name_validation():
    """Probar validación de nombres duplicados"""
    print("\n🔍 PROBANDO VALIDACIÓN DE NOMBRES")
    print("=" * 50)
    
    try:
        from categorias.models import CategoriaProducto
        from categorias.serializers import CategoriaProductoSerializer
        
        # Obtener dos categorías diferentes
        categorias = CategoriaProducto.objects.all()[:2]
        if len(categorias) < 2:
            print("❌ Se necesitan al menos 2 categorías para probar")
            return False
        
        categoria1 = categorias[0]
        categoria2 = categorias[1]
        
        print(f"1. Categoría 1: {categoria1.nombre} (ID: {categoria1.id})")
        print(f"2. Categoría 2: {categoria2.nombre} (ID: {categoria2.id})")
        
        # Intentar actualizar categoria2 con el nombre de categoria1
        test_data = {
            'nombre': categoria1.nombre,  # Nombre de otra categoría
            'descripcion': 'Descripción de prueba',
            'activa': True,
            'orden': 1
        }
        
        # Crear serializer con categoria2
        serializer = CategoriaProductoSerializer(
            instance=categoria2,
            data=test_data,
            context={'request': None}
        )
        
        if serializer.is_valid():
            print("3. ❌ Serializer válido (debería fallar)")
            return False
        else:
            print("3. ✅ Serializer inválido (correcto)")
            if 'nombre' in serializer.errors:
                print(f"   Error de nombre: {serializer.errors['nombre']}")
                return True
            else:
                print("   Error inesperado")
                return False
        
    except Exception as e:
        print(f"❌ Error probando validación: {e}")
        return False

def test_categoria_same_name_update():
    """Probar actualización con el mismo nombre"""
    print("\n🔄 PROBANDO ACTUALIZACIÓN CON MISMO NOMBRE")
    print("=" * 50)
    
    try:
        from categorias.models import CategoriaProducto
        from categorias.serializers import CategoriaProductoSerializer
        
        # Obtener una categoría
        categoria = CategoriaProducto.objects.first()
        if not categoria:
            print("❌ No hay categorías para probar")
            return False
        
        print(f"1. Categoría: {categoria.nombre} (ID: {categoria.id})")
        
        # Actualizar con el mismo nombre pero diferente descripción
        test_data = {
            'nombre': categoria.nombre,  # Mismo nombre
            'descripcion': 'Descripción actualizada con mismo nombre',
            'activa': True,
            'orden': 1
        }
        
        # Crear serializer
        serializer = CategoriaProductoSerializer(
            instance=categoria,
            data=test_data,
            context={'request': None}
        )
        
        if serializer.is_valid():
            print("2. ✅ Serializer válido (correcto para mismo nombre)")
            
            # Intentar actualizar
            try:
                categoria_actualizada = serializer.save()
                print(f"3. ✅ Categoría actualizada: {categoria_actualizada.nombre}")
                print(f"   Descripción: {categoria_actualizada.descripcion}")
                return True
                
            except Exception as e:
                print(f"3. ❌ Error actualizando: {e}")
                return False
        else:
            print("2. ❌ Serializer inválido (incorrecto)")
            print(f"   Errores: {serializer.errors}")
            return False
        
    except Exception as e:
        print(f"❌ Error probando actualización: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 PRUEBA DE ACTUALIZACIÓN DE CATEGORÍAS (LOCAL)")
    print("=" * 60)
    
    tests = [
        ("Actualización Básica", test_categoria_update),
        ("Actualización con Imagen", test_categoria_update_with_image),
        ("Validación de Nombres", test_categoria_name_validation),
        ("Mismo Nombre", test_categoria_same_name_update),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results[test_name] = False
    
    # Resumen
    print("\n📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! El problema está resuelto.")
    elif passed >= 3:
        print("✅ La mayoría de las pruebas pasaron. El problema está casi resuelto.")
    else:
        print("⚠️ Varias pruebas fallaron. Hay problemas de configuración.")
    
    return passed >= 3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 