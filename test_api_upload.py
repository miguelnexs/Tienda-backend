#!/usr/bin/env python
"""
Script para probar la subida de imagen por API
"""
import os
import sys
import requests
import time

def test_api_upload():
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
    
    # Primero obtener los productos disponibles
    try:
        print("🔍 Obteniendo productos disponibles...")
        response = requests.get(f"{API_BASE_URL}/productos/")
        
        if response.status_code != 200:
            print(f"❌ Error al obtener productos: {response.status_code}")
            return False
        
        productos = response.json()
        print(f"✅ Productos obtenidos: {len(productos)}")
        
        if not productos:
            print("❌ No hay productos disponibles")
            return False
        
        # Usar el primer producto
        producto = productos[0]
        producto_id = producto['id']
        print(f"🎯 Usando producto: {producto['nombre']} (ID: {producto_id})")
        
        # Obtener colores del producto
        print("🔍 Obteniendo colores del producto...")
        response = requests.get(f"{API_BASE_URL}/productos/{producto_id}/colores/")
        
        if response.status_code != 200:
            print(f"❌ Error al obtener colores: {response.status_code}")
            return False
        
        colores = response.json()
        print(f"✅ Colores obtenidos: {len(colores)}")
        
        if not colores:
            print("❌ El producto no tiene colores")
            return False
        
        # Usar el primer color
        color = colores[0]
        color_id = color['id']
        print(f"🎨 Usando color: {color['nombre']} (ID: {color_id})")
        
        # Preparar la petición para subir la imagen
        url = f"{API_BASE_URL}/productos/{producto_id}/colores/{color_id}/imagenes/"
        
        # Preparar los datos
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('Bolso-BWXXNG-NEGRO_1.jpg', image_file, 'image/jpeg')
            }
            
            data = {
                'orden': 2,  # Usar orden 2 para no conflictuar con la imagen existente
                'es_principal': False
            }
            
            print(f"\n🚀 Subiendo imagen a: {url}")
            print(f"📤 Datos: {data}")
            
            response = requests.post(url, files=files, data=data)
            
            print(f"\n📊 Respuesta del servidor:")
            print(f"  Status Code: {response.status_code}")
            print(f"  Response: {response.text}")
            
            if response.status_code == 201:
                print("✅ ¡Imagen subida exitosamente por API!")
                
                # Obtener la imagen creada
                imagen_data = response.json()
                print(f"📸 Imagen creada con ID: {imagen_data.get('id')}")
                print(f"🔗 URL de la imagen: {imagen_data.get('imagen')}")
                
                return True
            else:
                print("❌ Error al subir la imagen por API")
                return False
                
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("💡 Asegúrate de que el servidor esté corriendo en http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_get_images():
    """Probar obtener las imágenes del color"""
    
    print("\n" + "="*50)
    print("🔍 PROBANDO OBTENCIÓN DE IMÁGENES")
    print("="*50)
    
    API_BASE_URL = "http://localhost:8000/api"
    
    try:
        # Obtener productos
        response = requests.get(f"{API_BASE_URL}/productos/")
        if response.status_code != 200:
            print("❌ Error al obtener productos")
            return False
        
        productos = response.json()
        if not productos:
            print("❌ No hay productos")
            return False
        
        producto = productos[0]
        producto_id = producto['id']
        
        # Obtener colores
        response = requests.get(f"{API_BASE_URL}/productos/{producto_id}/colores/")
        if response.status_code != 200:
            print("❌ Error al obtener colores")
            return False
        
        colores = response.json()
        if not colores:
            print("❌ No hay colores")
            return False
        
        color = colores[0]
        color_id = color['id']
        
        # Obtener imágenes del color
        response = requests.get(f"{API_BASE_URL}/productos/{producto_id}/colores/{color_id}/imagenes/")
        
        if response.status_code == 200:
            imagenes = response.json()
            print(f"✅ Imágenes obtenidas: {len(imagenes)}")
            
            for imagen in imagenes:
                print(f"📸 Imagen ID: {imagen['id']}")
                print(f"  🔗 URL: {imagen['imagen']}")
                print(f"  ⭐ Principal: {imagen['es_principal']}")
                print(f"  📊 Orden: {imagen['orden']}")
            
            return True
        else:
            print(f"❌ Error al obtener imágenes: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA DE SUBIDA DE IMAGEN POR API")
    print("="*50)
    
    # Esperar un poco para que el servidor esté listo
    print("⏳ Esperando que el servidor esté listo...")
    time.sleep(3)
    
    # Probar subida por API
    success_upload = test_api_upload()
    
    # Probar obtención de imágenes
    success_get = test_get_images()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS API")
    print("="*50)
    print(f"✅ Subida por API: {'EXITOSA' if success_upload else 'FALLIDA'}")
    print(f"✅ Obtención de imágenes: {'EXITOSA' if success_get else 'FALLIDA'}")
    
    if success_upload and success_get:
        print("\n🎉 ¡Todas las pruebas de API fueron exitosas!")
    else:
        print("\n❌ Algunas pruebas de API fallaron")

if __name__ == '__main__':
    main() 