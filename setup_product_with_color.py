#!/usr/bin/env python
"""
Script para configurar un producto con color y subir imagen
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from productos.models import Producto, ColorProducto, ImagenProducto
from django.core.files import File

def setup_product_with_color():
    """Configurar un producto con color y subir imagen"""
    
    print("🔧 CONFIGURANDO PRODUCTO CON COLOR")
    print("="*50)
    
    # Obtener el primer producto
    producto = Producto.objects.first()
    if not producto:
        print("❌ No hay productos en la base de datos")
        return False
    
    print(f"🎯 Producto seleccionado: {producto.nombre} (ID: {producto.id})")
    
    # Verificar si ya tiene colores
    colores_existentes = producto.colores.all()
    if colores_existentes.exists():
        print("✅ El producto ya tiene colores:")
        for color in colores_existentes:
            print(f"  - {color.nombre} (ID: {color.id})")
        color = colores_existentes.first()
    else:
        # Crear un color para el producto
        print("🎨 Creando color 'Negro' para el producto...")
        color = ColorProducto.objects.create(
            producto=producto,
            nombre="Negro",
            hex_code="#000000",
            stock=10,
            orden=1,
            activo=True
        )
        print(f"✅ Color creado: {color.nombre} (ID: {color.id})")
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    # Verificar si ya tiene imágenes
    imagenes_existentes = color.imagenes.all()
    if imagenes_existentes.exists():
        print("✅ El color ya tiene imágenes:")
        for imagen in imagenes_existentes:
            print(f"  - {imagen.imagen.name} (ID: {imagen.id})")
        
        # Preguntar si quiere agregar otra imagen
        print("\n💡 El color ya tiene imágenes. ¿Quieres agregar otra?")
        return True
    
    # Crear la imagen
    print("📸 Subiendo imagen al color...")
    try:
        with open(image_path, 'rb') as image_file:
            imagen = ImagenProducto.objects.create(
                color=color,
                imagen=File(image_file, name='Bolso-BWXXNG-NEGRO_1.jpg'),
                orden=1,
                es_principal=True
            )
            
            print("✅ Imagen subida exitosamente!")
            print(f"📸 ID de la imagen: {imagen.id}")
            print(f"🔗 URL de la imagen: {imagen.imagen.url}")
            print(f"📁 Ruta del archivo: {imagen.imagen.path}")
            
            # Verificar que se guardó correctamente
            if os.path.exists(imagen.imagen.path):
                print("✅ Archivo guardado correctamente en el sistema")
            else:
                print("⚠️  El archivo no se encuentra en el sistema de archivos")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al subir la imagen: {e}")
        return False

def test_image_access():
    """Probar el acceso a las imágenes subidas"""
    
    print("\n" + "="*50)
    print("🔍 PROBANDO ACCESO A IMÁGENES")
    print("="*50)
    
    # Obtener todas las imágenes
    imagenes = ImagenProducto.objects.all()
    
    if not imagenes.exists():
        print("❌ No hay imágenes en la base de datos")
        return False
    
    print(f"📸 Total de imágenes: {imagenes.count()}")
    
    for imagen in imagenes:
        print(f"\n📸 Imagen ID: {imagen.id}")
        print(f"  🎨 Color: {imagen.color.nombre}")
        print(f"  📦 Producto: {imagen.color.producto.nombre}")
        print(f"  🔗 URL: {imagen.imagen.url}")
        print(f"  📁 Path: {imagen.imagen.path}")
        print(f"  ⭐ Principal: {imagen.es_principal}")
        print(f"  📊 Orden: {imagen.orden}")
        
        # Verificar si el archivo existe
        if os.path.exists(imagen.imagen.path):
            print(f"  ✅ Archivo existe en el sistema")
            # Obtener tamaño del archivo
            file_size = os.path.getsize(imagen.imagen.path)
            print(f"  📏 Tamaño: {file_size} bytes ({file_size/1024:.1f} KB)")
        else:
            print(f"  ❌ Archivo NO existe en el sistema")
    
    return True

def main():
    """Función principal"""
    print("🧪 CONFIGURACIÓN Y PRUEBA DE SUBIDA DE IMAGEN")
    print("="*50)
    
    # Configurar producto con color
    success_setup = setup_product_with_color()
    
    # Probar acceso a imágenes
    success_access = test_image_access()
    
    print("\n" + "="*50)
    print("📊 RESUMEN")
    print("="*50)
    print(f"✅ Configuración de producto: {'EXITOSA' if success_setup else 'FALLIDA'}")
    print(f"✅ Acceso a imágenes: {'EXITOSA' if success_access else 'FALLIDA'}")
    
    if success_setup and success_access:
        print("\n🎉 ¡Todo configurado correctamente!")
        print("💡 Ahora puedes probar la subida por API ejecutando:")
        print("   python test_image_upload.py")
    else:
        print("\n❌ Hubo problemas en la configuración")

if __name__ == '__main__':
    main() 