#!/usr/bin/env python
"""
Script para probar la subida de imagen a un producto existente
"""
import os
import sys
import django
import requests
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from productos.models import Producto, ColorProducto, ImagenProducto

def test_image_upload():
    """Probar la subida de imagen usando la API"""
    
    # URL base de la API
    API_BASE_URL = "http://localhost:8000/api"
    
    # Ruta de la imagen a subir
    image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
    
    # Verificar que la imagen existe
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    # Obtener productos existentes
    productos = Producto.objects.all()
    if not productos.exists():
        print("❌ No hay productos en la base de datos")
        return False
    
    # Mostrar productos disponibles
    print("\n📦 Productos disponibles:")
    for producto in productos[:5]:  # Mostrar solo los primeros 5
        print(f"  ID: {producto.id} - {producto.nombre} (SKU: {producto.sku})")
    
    # Usar el primer producto para la prueba
    producto = productos.first()
    print(f"\n🎯 Usando producto: {producto.nombre} (ID: {producto.id})")
    
    # Verificar si el producto tiene colores
    colores = producto.colores.all()
    if not colores.exists():
        print("❌ El producto no tiene colores configurados")
        print("💡 Primero necesitas crear un color para el producto")
        return False
    
    # Usar el primer color
    color = colores.first()
    print(f"🎨 Usando color: {color.nombre} (ID: {color.id})")
    
    # Preparar la petición para subir la imagen
    url = f"{API_BASE_URL}/productos/{producto.id}/colores/{color.id}/imagenes/"
    
    # Preparar los datos
    with open(image_path, 'rb') as image_file:
        files = {
            'imagen': ('Bolso-BWXXNG-NEGRO_1.jpg', image_file, 'image/jpeg')
        }
        
        data = {
            'orden': 1,
            'es_principal': True
        }
        
        print(f"\n🚀 Subiendo imagen a: {url}")
        print(f"📤 Datos: {data}")
        
        try:
            response = requests.post(url, files=files, data=data)
            
            print(f"\n📊 Respuesta del servidor:")
            print(f"  Status Code: {response.status_code}")
            print(f"  Response: {response.text}")
            
            if response.status_code == 201:
                print("✅ ¡Imagen subida exitosamente!")
                
                # Obtener la imagen creada
                imagen_data = response.json()
                print(f"📸 Imagen creada con ID: {imagen_data.get('id')}")
                print(f"🔗 URL de la imagen: {imagen_data.get('imagen')}")
                
                return True
            else:
                print("❌ Error al subir la imagen")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se puede conectar al servidor")
            print("💡 Asegúrate de que el servidor esté corriendo en http://localhost:8000")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False

def test_direct_upload():
    """Probar la subida directa usando Django ORM"""
    
    print("\n" + "="*50)
    print("🔄 PROBANDO SUBIDA DIRECTA CON DJANGO ORM")
    print("="*50)
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    # Obtener un producto y color
    try:
        producto = Producto.objects.first()
        if not producto:
            print("❌ No hay productos en la base de datos")
            return False
        
        color = producto.colores.first()
        if not color:
            print("❌ El producto no tiene colores")
            return False
        
        print(f"🎯 Producto: {producto.nombre}")
        print(f"🎨 Color: {color.nombre}")
        
        # Crear la imagen directamente
        from django.core.files import File
        
        with open(image_path, 'rb') as image_file:
            imagen = ImagenProducto.objects.create(
                color=color,
                imagen=File(image_file, name='Bolso-BWXXNG-NEGRO_1.jpg'),
                orden=1,
                es_principal=True
            )
            
            print("✅ Imagen creada exitosamente con Django ORM")
            print(f"📸 ID de la imagen: {imagen.id}")
            print(f"🔗 URL de la imagen: {imagen.imagen.url}")
            print(f"📁 Ruta del archivo: {imagen.imagen.path}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al crear la imagen: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA DE SUBIDA DE IMAGEN")
    print("="*50)
    
    # Probar subida directa primero
    success_direct = test_direct_upload()
    
    # Probar subida por API
    success_api = test_image_upload()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    print(f"✅ Subida directa (Django ORM): {'EXITOSA' if success_direct else 'FALLIDA'}")
    print(f"✅ Subida por API: {'EXITOSA' if success_api else 'FALLIDA'}")
    
    if success_direct or success_api:
        print("\n🎉 ¡Al menos una prueba fue exitosa!")
    else:
        print("\n❌ Todas las pruebas fallaron")

if __name__ == '__main__':
    main() 