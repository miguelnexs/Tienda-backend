#!/usr/bin/env python3
"""
Script de prueba para verificar que los modelos Django funcionan con Cloudinary
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

from django.core.files.base import ContentFile
from django.core.files import File

def test_producto_model():
    """Probar el modelo Producto con Cloudinary storage"""
    print("🧪 Probando modelo Producto con Cloudinary...")
    
    try:
        from productos.models import Producto
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (200, 200), color='blue')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear un producto de prueba
        producto = Producto(
            nombre="Producto Test Cloudinary",
            descripcion_corta="Producto para probar Cloudinary",
            descripcion_larga="Producto creado para probar la funcionalidad de Cloudinary",
            precio=100.00,
            costo=50.00,
            stock=10,
            estado='publicado',
            sku='TEST-CLOUD-001'
        )
        
        # Guardar el producto
        producto.save()
        print(f"✅ Producto creado: {producto.id}")
        
        # Crear archivo de imagen
        django_file = File(img_io, name='test_producto.jpg')
        
        # Asignar imagen al producto
        producto.imagen_principal.save('test_producto.jpg', django_file, save=True)
        print(f"✅ Imagen asignada al producto")
        print(f"  Nombre del archivo: {producto.imagen_principal.name}")
        print(f"  URL: {producto.imagen_principal.url}")
        
        # Verificar que la imagen existe
        if hasattr(producto.imagen_principal, 'storage'):
            exists = producto.imagen_principal.storage.exists(producto.imagen_principal.name)
            print(f"  Existe en storage: {exists}")
        
        # Limpiar
        producto.delete()
        print("✅ Producto eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando modelo Producto: {e}")
        return False

def test_categoria_model():
    """Probar el modelo CategoriaProducto con Cloudinary storage"""
    print("\n🧪 Probando modelo CategoriaProducto con Cloudinary...")
    
    try:
        from categorias.models import CategoriaProducto
        
        # Crear una imagen de prueba
        img = Image.new('RGB', (150, 150), color='green')
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        # Crear una categoría de prueba
        categoria = CategoriaProducto(
            nombre="Categoría Test Cloudinary",
            descripcion="Categoría para probar Cloudinary",
            slug="categoria-test-cloudinary"
        )
        
        # Guardar la categoría
        categoria.save()
        print(f"✅ Categoría creada: {categoria.id}")
        
        # Crear archivo de imagen
        django_file = File(img_io, name='test_categoria.png')
        
        # Asignar imagen a la categoría
        categoria.imagen.save('test_categoria.png', django_file, save=True)
        print(f"✅ Imagen asignada a la categoría")
        print(f"  Nombre del archivo: {categoria.imagen.name}")
        print(f"  URL: {categoria.imagen.url}")
        
        # Verificar que la imagen existe
        if hasattr(categoria.imagen, 'storage'):
            exists = categoria.imagen.storage.exists(categoria.imagen.name)
            print(f"  Existe en storage: {exists}")
        
        # Limpiar
        categoria.delete()
        print("✅ Categoría eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando modelo CategoriaProducto: {e}")
        return False

def test_api_endpoints():
    """Probar endpoints de la API"""
    print("\n🧪 Probando endpoints de la API...")
    
    try:
        from django.test import Client
        
        client = Client()
        
        # Probar endpoint de productos
        response = client.get('/api/productos/')
        if response.status_code == 200:
            print("✅ Endpoint de productos accesible")
            data = response.json()
            print(f"  Productos encontrados: {len(data.get('results', []))}")
        else:
            print(f"⚠️ Endpoint de productos: {response.status_code}")
        
        # Probar endpoint de categorías
        response = client.get('/api/categorias/')
        if response.status_code == 200:
            print("✅ Endpoint de categorías accesible")
            data = response.json()
            print(f"  Categorías encontradas: {len(data.get('results', []))}")
        else:
            print(f"⚠️ Endpoint de categorías: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando endpoints: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DE MODELOS DJANGO CON CLOUDINARY")
    print("=" * 60)
    
    tests = [
        ("Modelo Producto", test_producto_model),
        ("Modelo CategoriaProducto", test_categoria_model),
        ("Endpoints API", test_api_endpoints),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results[test_name] = False
    
    # Resumen de resultados
    print("\n📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO FINAL: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! Los modelos funcionan correctamente con Cloudinary.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 