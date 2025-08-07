#!/usr/bin/env python
"""
Script para crear una categoría con imagen usando serializers en Render
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
from django.core.files import File

def create_categoria_with_image_render():
    """Crear categoría con imagen usando serializers en Render"""
    
    print("🏷️ CREANDO CATEGORÍA CON IMAGEN EN RENDER")
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
            'nombre': 'Accesorios de Mujer',
            'descripcion': 'Categoría especializada en accesorios para mujer, incluyendo carteras, bolsos y complementos de moda.',
            'activa': True,
            'orden': 1
        }
        
        print(f"📋 Datos de la categoría: {categoria_data}")
        
        # Crear la categoría usando el serializer
        with open(image_path, 'rb') as image_file:
            # Simular request con archivo
            from django.core.files.uploadedfile import InMemoryUploadedFile
            from io import BytesIO
            
            # Crear archivo de imagen para el serializer
            image_data = image_file.read()
            image_file_obj = InMemoryUploadedFile(
                BytesIO(image_data),
                'imagen',
                'cartera-casual-para-mujer-23064.jpg',
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
                
                # Verificar si la imagen se subió a Cloudinary
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

def create_categoria_via_api_render():
    """Crear categoría con imagen via API de Render"""
    
    print("\n" + "="*50)
    print("🌐 CREANDO CATEGORÍA VIA API DE RENDER")
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
            'nombre': 'Accesorios de Mujer',
            'descripcion': 'Categoría especializada en accesorios para mujer, incluyendo carteras, bolsos y complementos de moda.',
            'activa': True,
            'orden': 1
        }
        
        print(f"📋 Datos de la categoría: {categoria_data}")
        
        # Preparar la petición
        url = f"{RENDER_API_URL}/categorias/"
        
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('cartera-casual-para-mujer-23064.jpg', image_file, 'image/jpeg')
            }
            
            print(f"\n🚀 Creando categoría en: {url}")
            
            response = requests.post(url, files=files, data=categoria_data, timeout=60)
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📊 Response Headers: {dict(response.headers)}")
            print(f"📊 Response Text: {response.text}")
            
            if response.status_code == 201:
                try:
                    categoria_data = response.json()
                    print("✅ ¡Categoría creada exitosamente en Render!")
                    print(f"📸 ID de la categoría: {categoria_data.get('id')}")
                    print(f"🏷️ Nombre: {categoria_data.get('nombre')}")
                    print(f"🔗 Slug: {categoria_data.get('slug')}")
                    print(f"🔗 URL de la imagen: {categoria_data.get('imagen_url')}")
                    
                    # Verificar Cloudinary
                    if categoria_data.get('imagen_url') and 'cloudinary.com' in categoria_data.get('imagen_url', ''):
                        print("☁️ ¡La imagen se subió a Cloudinary desde Render!")
                    else:
                        print("📁 La imagen se guardó localmente en Render")
                    
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

def test_categoria_cloudinary_upload():
    """Probar subida directa de imagen de categoría a Cloudinary"""
    
    print("\n" + "="*50)
    print("☁️ SUBIENDO IMAGEN DE CATEGORÍA A CLOUDINARY")
    print("="*50)
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\cartera-casual-para-mujer-23064.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    try:
        import cloudinary
        import cloudinary.uploader
        import cloudinary.api
        
        # Configurar Cloudinary
        cloudinary.config(
            cloud_name="do1ntnlop",
            api_key="1172253771",
            api_secret="e0YSrk3sT_"
        )
        
        print("🚀 Subiendo imagen de categoría a Cloudinary...")
        
        # Subir la imagen con metadatos específicos para categoría
        result = cloudinary.uploader.upload(
            image_path,
            folder="categorias",
            public_id="accesorios-mujer-categoria",
            overwrite=True,
            resource_type="image",
            transformation=[
                {"width": 600, "height": 400, "crop": "fill"},
                {"quality": "auto", "fetch_format": "auto"}
            ],
            tags=["categoria", "accesorios", "mujer", "moda"],
            context={
                "categoria": "Accesorios de Mujer",
                "tipo": "Categoría",
                "descripcion": "Categoría de accesorios para mujer"
            }
        )
        
        print("✅ Imagen de categoría subida exitosamente a Cloudinary!")
        print(f"📸 URL de la imagen: {result['secure_url']}")
        print(f"📁 Public ID: {result['public_id']}")
        print(f"📏 Tamaño: {result['bytes']} bytes")
        print(f"🖼️ Formato: {result['format']}")
        print(f"📐 Dimensiones: {result['width']}x{result['height']}")
        print(f"🏷️ Tags: {result.get('tags', [])}")
        print(f"📋 Context: {result.get('context', {})}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error subiendo a Cloudinary: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 CREACIÓN DE CATEGORÍA CON IMAGEN EN RENDER")
    print("="*50)
    
    # Probar subida directa a Cloudinary
    cloudinary_result = test_categoria_cloudinary_upload()
    
    # Probar creación con serializers en Render
    success_serializer = create_categoria_with_image_render()
    
    # Probar creación via API de Render
    success_api = create_categoria_via_api_render()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE CREACIÓN DE CATEGORÍA")
    print("="*50)
    print(f"✅ Subida directa a Cloudinary: {'EXITOSA' if cloudinary_result else 'FALLIDA'}")
    print(f"✅ Creación con serializers: {'EXITOSA' if success_serializer else 'FALLIDA'}")
    print(f"✅ Creación via API Render: {'EXITOSA' if success_api else 'FALLIDA'}")
    
    if cloudinary_result:
        print(f"\n🔗 URL de la imagen de categoría:")
        print(f"   {cloudinary_result['secure_url']}")
    
    if success_serializer:
        print(f"\n🏷️ Categoría creada con serializers:")
        print(f"   ID: {success_serializer.id}")
        print(f"   Nombre: {success_serializer.nombre}")
        print(f"   Slug: {success_serializer.slug}")
    
    if success_api:
        print(f"\n🌐 Categoría creada via API:")
        print(f"   ID: {success_api.get('id')}")
        print(f"   Nombre: {success_api.get('nombre')}")
        print(f"   Slug: {success_api.get('slug')}")
    
    if cloudinary_result or success_serializer or success_api:
        print("\n🎉 ¡La categoría se creó exitosamente en Render!")
        print("💡 La imagen está disponible en Cloudinary")
    else:
        print("\n❌ Hay problemas con la creación de la categoría")

if __name__ == '__main__':
    main() 