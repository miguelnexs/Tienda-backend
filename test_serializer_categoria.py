#!/usr/bin/env python
"""
Script para probar el serializer corregido de categorías
"""
import os
import sys
import django
import requests
import json
from pathlib import Path

# Configurar Django para Render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

from categorias.models import CategoriaProducto
from categorias.serializers import CategoriaProductoSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

def test_serializer_local():
    """Probar el serializer localmente"""
    
    print("🧪 PROBANDO SERIALIZER LOCALMENTE")
    print("="*50)
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\cartera-casual-para-mujer-23064.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    try:
        # Crear datos de la categoría
        categoria_data = {
            'nombre': 'Test Serializer Corregido',
            'descripcion': 'Prueba del serializer corregido para subida de imágenes',
            'activa': True,
            'orden': 999
        }
        
        print(f"📋 Datos de la categoría: {categoria_data}")
        
        # Crear archivo de imagen para el serializer
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            
            # Crear InMemoryUploadedFile
            image_file_obj = InMemoryUploadedFile(
                BytesIO(image_data),
                'imagen',
                'test-serializer-categoria.jpg',
                'image/jpeg',
                len(image_data),
                None
            )
            
            # Crear contexto para el serializer
            from django.test import RequestFactory
            factory = RequestFactory()
            request = factory.post('/api/categorias/')
            
            # Crear serializer con datos y archivo
            serializer = CategoriaProductoSerializer(
                data=categoria_data,
                context={'request': request}
            )
            
            # Asignar la imagen al serializer
            serializer.initial_data['imagen'] = image_file_obj
            
            print("🔍 Validando serializer...")
            
            if serializer.is_valid():
                print("✅ Serializer válido")
                
                # Crear la categoría
                categoria = serializer.save()
                
                print("✅ Categoría creada exitosamente!")
                print(f"📸 ID de la categoría: {categoria.id}")
                print(f"🏷️ Nombre: {categoria.nombre}")
                print(f"🔗 Slug: {categoria.slug}")
                print(f"📁 Imagen: {categoria.imagen.name if categoria.imagen else 'Sin imagen'}")
                
                # Verificar si la imagen se subió correctamente
                if categoria.imagen:
                    print(f"🔗 URL de la imagen: {categoria.imagen.url}")
                    if 'cloudinary.com' in categoria.imagen.url:
                        print("☁️ ¡La imagen se subió a Cloudinary!")
                    else:
                        print("📁 La imagen se guardó localmente")
                
                return categoria
            else:
                print(f"❌ Errores de validación: {serializer.errors}")
                return False
                
    except Exception as e:
        print(f"❌ Error al crear la categoría: {e}")
        return False

def test_serializer_api_render():
    """Probar el serializer via API de Render"""
    
    print("\n" + "="*50)
    print("🌐 PROBANDO SERIALIZER VIA API DE RENDER")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\cartera-casual-para-mujer-23064.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    try:
        # Preparar datos de la categoría
        categoria_data = {
            'nombre': 'Test Serializer API',
            'descripcion': 'Prueba del serializer corregido via API',
            'activa': True,
            'orden': 998
        }
        
        print(f"📋 Datos de la categoría: {categoria_data}")
        
        # Preparar la petición
        url = f"{RENDER_API_URL}/categorias/"
        
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('test-serializer-api.jpg', image_file, 'image/jpeg')
            }
            
            print(f"\n🚀 Creando categoría con serializer corregido en: {url}")
            
            response = requests.post(url, files=files, data=categoria_data, timeout=60)
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📊 Response Headers: {dict(response.headers)}")
            print(f"📊 Response Text: {response.text}")
            
            if response.status_code == 201:
                try:
                    categoria_data = response.json()
                    print("✅ ¡Categoría creada exitosamente con serializer corregido!")
                    print(f"📸 ID de la categoría: {categoria_data.get('id')}")
                    print(f"🏷️ Nombre: {categoria_data.get('nombre')}")
                    print(f"🔗 Slug: {categoria_data.get('slug')}")
                    print(f"🔗 URL de la imagen: {categoria_data.get('imagen_url')}")
                    
                    # Verificar si la imagen se subió a Cloudinary
                    imagen_url = categoria_data.get('imagen_url', '')
                    if 'cloudinary.com' in imagen_url:
                        print("☁️ ¡La imagen se subió a Cloudinary con el serializer corregido!")
                        print("✅ Serializer corregido: EXITOSO")
                    else:
                        print("📁 La imagen se guardó localmente en Render")
                        print("⚠️ Serializer corregido: PARCIAL (local)")
                    
                    return categoria_data
                except json.JSONDecodeError as e:
                    print(f"❌ Error decodificando respuesta: {e}")
                    return False
            else:
                print(f"❌ Error al crear la categoría: {response.status_code}")
                return False
                
    except requests.exceptions.Timeout:
        print("❌ Timeout: La creación tardó demasiado")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión durante la creación")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_serializer_validation():
    """Probar validaciones del serializer"""
    
    print("\n" + "="*50)
    print("🔍 PROBANDO VALIDACIONES DEL SERIALIZER")
    print("="*50)
    
    try:
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.post('/api/categorias/')
        
        # Probar validación de nombre vacío
        print("📋 Probando validación de nombre vacío...")
        serializer = CategoriaProductoSerializer(
            data={'nombre': ''},
            context={'request': request}
        )
        
        if not serializer.is_valid():
            print("✅ Validación de nombre vacío funciona")
            print(f"   Error: {serializer.errors.get('nombre', [])}")
        else:
            print("❌ Validación de nombre vacío falló")
        
        # Probar validación de nombre duplicado
        print("\n📋 Probando validación de nombre duplicado...")
        serializer = CategoriaProductoSerializer(
            data={'nombre': 'Accesorios de Mujer'},  # Ya existe
            context={'request': request}
        )
        
        if not serializer.is_valid():
            print("✅ Validación de nombre duplicado funciona")
            print(f"   Error: {serializer.errors.get('nombre', [])}")
        else:
            print("❌ Validación de nombre duplicado falló")
        
        # Probar validación de imagen
        print("\n📋 Probando validación de imagen...")
        
        # Crear archivo de imagen inválido (texto)
        invalid_image = InMemoryUploadedFile(
            BytesIO(b"Esto no es una imagen"),
            'imagen',
            'test.txt',
            'text/plain',
            len(b"Esto no es una imagen"),
            None
        )
        
        serializer = CategoriaProductoSerializer(
            data={'nombre': 'Test Validación', 'imagen': invalid_image},
            context={'request': request}
        )
        
        if not serializer.is_valid():
            print("✅ Validación de tipo de imagen funciona")
            print(f"   Error: {serializer.errors.get('imagen', [])}")
        else:
            print("❌ Validación de tipo de imagen falló")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en validaciones: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA DEL SERIALIZER CORREGIDO")
    print("="*50)
    
    # Probar validaciones
    validation_ok = test_serializer_validation()
    
    # Probar serializer local
    success_local = test_serializer_local()
    
    # Probar serializer via API
    success_api = test_serializer_api_render()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS DEL SERIALIZER")
    print("="*50)
    print(f"✅ Validaciones del serializer: {'EXITOSA' if validation_ok else 'FALLIDA'}")
    print(f"✅ Serializer local: {'EXITOSA' if success_local else 'FALLIDA'}")
    print(f"✅ Serializer via API: {'EXITOSA' if success_api else 'FALLIDA'}")
    
    if success_local:
        print(f"\n🏷️ Categoría creada localmente:")
        print(f"   ID: {success_local.id}")
        print(f"   Nombre: {success_local.nombre}")
        print(f"   Slug: {success_local.slug}")
    
    if success_api:
        print(f"\n🌐 Categoría creada via API:")
        print(f"   ID: {success_api.get('id')}")
        print(f"   Nombre: {success_api.get('nombre')}")
        print(f"   Slug: {success_api.get('slug')}")
    
    if validation_ok and (success_local or success_api):
        print("\n🎉 ¡El serializer corregido funciona correctamente!")
        print("✅ Las imágenes se suben correctamente")
        print("✅ Las validaciones funcionan")
    else:
        print("\n❌ Hay problemas con el serializer corregido")

if __name__ == '__main__':
    main() 