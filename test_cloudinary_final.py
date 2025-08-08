#!/usr/bin/env python3
"""
Script para verificar la configuración final de Cloudinary
"""
import os
import sys
import django
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.core.files.base import ContentFile

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
    print("✅ Django configurado correctamente")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

from django.core.files.storage import default_storage
from Backend.cloudinary_storage_fixed_urls import CloudinaryStorageFixedURLs
from productos.models import Producto, ColorProducto, ImagenProducto
from categorias.models import CategoriaProducto

def test_cloudinary_config():
    """Verificar configuración de Cloudinary"""
    print("\n🧪 VERIFICANDO CONFIGURACIÓN DE CLOUDINARY")
    print("=" * 60)
    
    try:
        # Verificar credenciales
        config = cloudinary.config()
        print(f"✅ Credenciales configuradas:")
        print(f"  Cloud Name: {config.cloud_name}")
        print(f"  API Key: {config.api_key[:10]}...")
        
        # Verificar storage
        if isinstance(default_storage, CloudinaryStorageFixedURLs):
            print("✅ Storage configurado correctamente")
            print(f"  Tipo: {type(default_storage).__name__}")
        else:
            print("❌ Storage NO configurado correctamente")
            print(f"  Tipo actual: {type(default_storage).__name__}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando configuración: {e}")
        return False

def test_categoria_upload():
    """Probar subida de imagen en categoría"""
    print("\n🧪 PROBANDO SUBIDA DE IMAGEN EN CATEGORÍA")
    print("=" * 60)
    
    try:
        # Crear contenido de prueba
        content = ContentFile(b"test content", name="test_categoria.jpg")
        
        # Crear categoría
        categoria = CategoriaProducto.objects.create(
            nombre="Categoría de prueba",
            descripcion="Descripción de prueba"
        )
        
        # Guardar imagen
        categoria.imagen.save("test_categoria.jpg", content)
        
        # Verificar URL
        url = categoria.imagen.url
        print(f"✅ Imagen guardada exitosamente")
        print(f"🔗 URL: {url}")
        
        # Verificar que sea URL de Cloudinary
        if 'cloudinary.com' in url:
            print("✅ URL de Cloudinary generada correctamente")
            return True
        else:
            print("❌ URL no es de Cloudinary")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de categoría: {e}")
        return False
    finally:
        # Limpiar
        try:
            categoria.delete()
        except:
            pass

def test_producto_upload():
    """Probar subida de imagen en producto"""
    print("\n🧪 PROBANDO SUBIDA DE IMAGEN EN PRODUCTO")
    print("=" * 60)
    
    try:
        # Crear contenido de prueba
        content = ContentFile(b"test content", name="test_producto.jpg")
        
        # Crear producto
        producto = Producto.objects.create(
            nombre="Producto de prueba",
            sku="TEST001",
            descripcion_corta="Descripción corta",
            descripcion_larga="Descripción larga",
            precio=100,
            costo=50
        )
        
        # Guardar imagen
        producto.imagen_principal.save("test_producto.jpg", content)
        
        # Verificar URL
        url = producto.imagen_principal.url
        print(f"✅ Imagen guardada exitosamente")
        print(f"🔗 URL: {url}")
        
        # Verificar que sea URL de Cloudinary
        if 'cloudinary.com' in url:
            print("✅ URL de Cloudinary generada correctamente")
            return True
        else:
            print("❌ URL no es de Cloudinary")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de producto: {e}")
        return False
    finally:
        # Limpiar
        try:
            producto.delete()
        except:
            pass

def test_color_upload():
    """Probar subida de imagen en color de producto"""
    print("\n🧪 PROBANDO SUBIDA DE IMAGEN EN COLOR")
    print("=" * 60)
    
    try:
        # Crear contenido de prueba
        content = ContentFile(b"test content", name="test_color.jpg")
        
        # Crear producto
        producto = Producto.objects.create(
            nombre="Producto de prueba",
            sku="TEST002",
            descripcion_corta="Descripción corta",
            descripcion_larga="Descripción larga",
            precio=100,
            costo=50
        )
        
        # Crear color
        color = ColorProducto.objects.create(
            producto=producto,
            nombre="Color de prueba",
            hex_code="#FF0000"
        )
        
        # Crear imagen
        imagen = ImagenProducto.objects.create(
            color=color,
            es_principal=True
        )
        
        # Guardar imagen
        imagen.imagen.save("test_color.jpg", content)
        
        # Verificar URL
        url = imagen.imagen.url
        print(f"✅ Imagen guardada exitosamente")
        print(f"🔗 URL: {url}")
        
        # Verificar que sea URL de Cloudinary
        if 'cloudinary.com' in url:
            print("✅ URL de Cloudinary generada correctamente")
            return True
        else:
            print("❌ URL no es de Cloudinary")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de color: {e}")
        return False
    finally:
        # Limpiar
        try:
            producto.delete()
        except:
            pass

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS FINALES DE CLOUDINARY")
    print("=" * 60)
    
    # Ejecutar pruebas
    config_ok = test_cloudinary_config()
    categoria_ok = test_categoria_upload()
    producto_ok = test_producto_upload()
    color_ok = test_color_upload()
    
    # Mostrar resultados
    print("\n📊 RESULTADOS FINALES")
    print("=" * 60)
    print(f"Configuración: {'✅ PASÓ' if config_ok else '❌ FALLÓ'}")
    print(f"Categorías: {'✅ PASÓ' if categoria_ok else '❌ FALLÓ'}")
    print(f"Productos: {'✅ PASÓ' if producto_ok else '❌ FALLÓ'}")
    print(f"Colores: {'✅ PASÓ' if color_ok else '❌ FALLÓ'}")
    
    if all([config_ok, categoria_ok, producto_ok, color_ok]):
        print("\n🎉 ¡TODO CONFIGURADO CORRECTAMENTE!")
        print("✅ Cloudinary está funcionando en todas las secciones")
        print("✅ Las URLs se generan correctamente")
        print("✅ El sistema está listo para usar")
    else:
        print("\n⚠️ HAY PROBLEMAS EN LA CONFIGURACIÓN")
        print("❌ Revisa los errores antes de continuar") 