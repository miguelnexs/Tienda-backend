#!/usr/bin/env python
"""
Script para probar la API de categorías con el serializers corregido
"""
import os
import sys
import django
import requests
import json
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

def test_api_categorias_basic():
    """Probar API de categorías sin imagen"""
    
    print("🌐 PROBANDO API DE CATEGORÍAS SIN IMAGEN")
    print("="*50)
    
    try:
        # URL de la API
        url = "http://localhost:8000/api/categorias/"
        
        # Datos de prueba
        data = {
            'nombre': 'Test API Categoría',
            'descripcion': 'Prueba de la API con serializers corregido',
            'activa': True,
            'orden': 996
        }
        
        print("📋 Datos de prueba:")
        print(f"  URL: {url}")
        print(f"  Nombre: {data['nombre']}")
        print(f"  Descripción: {data['descripcion']}")
        
        # Realizar petición
        print("\n🚀 Enviando petición...")
        response = requests.post(url, json=data, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            try:
                categoria_data = response.json()
                print("✅ ¡Categoría creada exitosamente!")
                print(f"📋 ID: {categoria_data.get('id')}")
                print(f"📋 Nombre: {categoria_data.get('nombre')}")
                print(f"📋 Slug: {categoria_data.get('slug')}")
                print(f"📋 Activa: {categoria_data.get('activa')}")
                print(f"📋 Orden: {categoria_data.get('orden')}")
                
                # Limpiar categoría de prueba
                delete_url = f"{url}{categoria_data.get('id')}/"
                delete_response = requests.delete(delete_url)
                if delete_response.status_code == 204:
                    print("🧹 Categoría de prueba eliminada")
                else:
                    print("⚠️ No se pudo eliminar la categoría de prueba")
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                print(f"📄 Respuesta: {response.text}")
                return False
        else:
            print(f"❌ Error al crear la categoría: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: El servidor no está ejecutándose")
        print("💡 Ejecuta: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_api_categorias_with_image():
    """Probar API de categorías con imagen"""
    
    print("\n" + "="*50)
    print("🖼️ PROBANDO API DE CATEGORÍAS CON IMAGEN")
    print("="*50)
    
    try:
        # URL de la API
        url = "http://localhost:8000/api/categorias/"
        
        # Crear imagen de prueba
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Datos de una imagen JPEG mínima válida
        jpeg_header = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
        
        image_file = SimpleUploadedFile(
            "test_api_image.jpg",
            jpeg_header,
            content_type="image/jpeg"
        )
        
        # Datos de prueba
        data = {
            'nombre': 'Test API Categoría con Imagen',
            'descripcion': 'Prueba de la API con imagen',
            'activa': True,
            'orden': 995
        }
        
        files = {
            'imagen': image_file
        }
        
        print("📋 Datos de prueba:")
        print(f"  URL: {url}")
        print(f"  Nombre: {data['nombre']}")
        print(f"  Imagen: {files['imagen'].name}")
        
        # Realizar petición
        print("\n🚀 Enviando petición con imagen...")
        response = requests.post(url, data=data, files=files, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 201:
            try:
                categoria_data = response.json()
                print("✅ ¡Categoría con imagen creada exitosamente!")
                print(f"📋 ID: {categoria_data.get('id')}")
                print(f"📋 Nombre: {categoria_data.get('nombre')}")
                print(f"📋 Slug: {categoria_data.get('slug')}")
                print(f"📋 Imagen URL: {categoria_data.get('imagen_url')}")
                
                # Limpiar categoría de prueba
                delete_url = f"{url}{categoria_data.get('id')}/"
                delete_response = requests.delete(delete_url)
                if delete_response.status_code == 204:
                    print("🧹 Categoría de prueba eliminada")
                else:
                    print("⚠️ No se pudo eliminar la categoría de prueba")
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                print(f"📄 Respuesta: {response.text}")
                return False
        else:
            print(f"❌ Error al crear la categoría: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: El servidor no está ejecutándose")
        print("💡 Ejecuta: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_api_categorias_list():
    """Probar listado de categorías"""
    
    print("\n" + "="*50)
    print("📋 PROBANDO LISTADO DE CATEGORÍAS")
    print("="*50)
    
    try:
        # URL de la API
        url = "http://localhost:8000/api/categorias/"
        
        print("📋 Obteniendo listado de categorías...")
        response = requests.get(url, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                categorias_data = response.json()
                print("✅ ¡Listado obtenido exitosamente!")
                print(f"📊 Total de categorías: {len(categorias_data)}")
                
                # Mostrar algunas categorías
                for i, categoria in enumerate(categorias_data[:3]):
                    print(f"  {i+1}. {categoria.get('nombre')} (ID: {categoria.get('id')})")
                
                if len(categorias_data) > 3:
                    print(f"  ... y {len(categorias_data) - 3} más")
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                print(f"📄 Respuesta: {response.text}")
                return False
        else:
            print(f"❌ Error al obtener categorías: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: El servidor no está ejecutándose")
        print("💡 Ejecuta: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🌐 PRUEBA DE LA API DE CATEGORÍAS")
    print("="*50)
    
    # Probar listado de categorías
    list_ok = test_api_categorias_list()
    
    # Probar creación sin imagen
    basic_ok = test_api_categorias_basic()
    
    # Probar creación con imagen
    image_ok = test_api_categorias_with_image()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    print(f"✅ Listado de categorías: {'EXITOSA' if list_ok else 'FALLIDA'}")
    print(f"✅ Creación sin imagen: {'EXITOSA' if basic_ok else 'FALLIDA'}")
    print(f"✅ Creación con imagen: {'EXITOSA' if image_ok else 'FALLIDA'}")
    
    # Conclusión
    print("\n" + "="*50)
    print("🎯 CONCLUSIÓN")
    print("="*50)
    
    if list_ok and basic_ok and image_ok:
        print("🎉 ¡La API de categorías funciona perfectamente!")
        print("✅ Puede listar categorías")
        print("✅ Puede crear categorías sin imagen")
        print("✅ Puede crear categorías con imagen")
        print("✅ El serializers está completamente corregido")
    elif basic_ok and image_ok:
        print("✅ La API de creación funciona")
        print("⚠️ Pero hay problemas con el listado")
    elif basic_ok:
        print("✅ La API básica funciona")
        print("⚠️ Pero hay problemas con las imágenes")
    else:
        print("❌ Hay problemas con la API")
        print("🔧 Revisar la configuración del servidor")

if __name__ == '__main__':
    main() 