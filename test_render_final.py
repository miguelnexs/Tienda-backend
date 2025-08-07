#!/usr/bin/env python
"""
Script final para probar Render con mejor manejo de errores
"""
import os
import sys
import requests
import json
import traceback

def test_render_connection():
    """Probar conexión básica a Render"""
    
    print("🌐 PROBANDO CONEXIÓN A RENDER")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        print("🔍 Probando conexión básica...")
        response = requests.get(f"{RENDER_API_URL}/productos/", timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                productos = response.json()
                print(f"✅ Conexión exitosa! Productos obtenidos: {len(productos)}")
                return True
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando JSON: {e}")
                print(f"Response text: {response.text[:200]}...")
                return False
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: El servidor de Render no responde")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se puede conectar a Render")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_render_upload():
    """Probar subida a Render"""
    
    print("\n" + "="*50)
    print("🚀 PROBANDO SUBIDA A RENDER")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    try:
        # Obtener productos
        print("🔍 Obteniendo productos...")
        response = requests.get(f"{RENDER_API_URL}/productos/", timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Error obteniendo productos: {response.status_code}")
            return False
        
        productos = response.json()
        if not productos:
            print("❌ No hay productos disponibles")
            return False
        
        producto = productos[0]
        producto_id = producto.get('id')
        print(f"🎯 Producto: {producto.get('nombre')} (ID: {producto_id})")
        
        # Obtener colores
        print("🔍 Obteniendo colores...")
        response = requests.get(f"{RENDER_API_URL}/productos/{producto_id}/colores/", timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Error obteniendo colores: {response.status_code}")
            return False
        
        colores = response.json()
        if not colores:
            print("❌ El producto no tiene colores")
            return False
        
        color = colores[0]
        color_id = color.get('id')
        print(f"🎨 Color: {color.get('nombre')} (ID: {color_id})")
        
        # Preparar subida
        url = f"{RENDER_API_URL}/productos/{producto_id}/colores/{color_id}/imagenes/"
        
        print(f"\n🚀 Subiendo imagen a: {url}")
        
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('Bolso-BWXXNG-NEGRO_1.jpg', image_file, 'image/jpeg')
            }
            
            data = {
                'orden': 1,
                'es_principal': True
            }
            
            response = requests.post(url, files=files, data=data, timeout=60)
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📊 Response Headers: {dict(response.headers)}")
            
            if response.status_code == 201:
                try:
                    imagen_data = response.json()
                    print("✅ ¡Imagen subida exitosamente desde Render!")
                    print(f"📸 Imagen creada con ID: {imagen_data.get('id')}")
                    print(f"🔗 URL: {imagen_data.get('imagen')}")
                    
                    # Verificar Cloudinary
                    if 'cloudinary.com' in imagen_data.get('imagen', ''):
                        print("☁️ ¡La imagen se subió a Cloudinary desde Render!")
                    else:
                        print("📁 La imagen se guardó localmente en Render")
                    
                    return True
                except json.JSONDecodeError as e:
                    print(f"❌ Error decodificando respuesta: {e}")
                    print(f"Response text: {response.text}")
                    return False
            else:
                print(f"❌ Error al subir la imagen: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except requests.exceptions.Timeout:
        print("❌ Timeout: La subida tardó demasiado")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión durante la subida")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_render_images():
    """Probar acceso a imágenes en Render"""
    
    print("\n" + "="*50)
    print("🔍 PROBANDO ACCESO A IMÁGENES EN RENDER")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # Obtener productos
        response = requests.get(f"{RENDER_API_URL}/productos/", timeout=30)
        if response.status_code != 200:
            print("❌ Error obteniendo productos")
            return False
        
        productos = response.json()
        if not productos:
            print("❌ No hay productos")
            return False
        
        producto = productos[0]
        producto_id = producto.get('id')
        
        # Obtener colores
        response = requests.get(f"{RENDER_API_URL}/productos/{producto_id}/colores/", timeout=30)
        if response.status_code != 200:
            print("❌ Error obteniendo colores")
            return False
        
        colores = response.json()
        if not colores:
            print("❌ No hay colores")
            return False
        
        color = colores[0]
        color_id = color.get('id')
        
        # Obtener imágenes
        response = requests.get(f"{RENDER_API_URL}/productos/{producto_id}/colores/{color_id}/imagenes/", timeout=30)
        
        if response.status_code == 200:
            try:
                imagenes = response.json()
                print(f"✅ Imágenes obtenidas: {len(imagenes)}")
                
                for i, imagen in enumerate(imagenes):
                    print(f"\n📸 Imagen {i+1}:")
                    print(f"  ID: {imagen.get('id')}")
                    print(f"  URL: {imagen.get('imagen')}")
                    print(f"  Principal: {imagen.get('es_principal')}")
                    
                    # Verificar Cloudinary
                    if 'cloudinary.com' in imagen.get('imagen', ''):
                        print(f"  ☁️ Cloudinary: ✅")
                    else:
                        print(f"  📁 Local: ✅")
                
                return True
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando imágenes: {e}")
                return False
        else:
            print(f"❌ Error obteniendo imágenes: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA FINAL DE RENDER")
    print("="*50)
    
    # Probar conexión
    success_connection = test_render_connection()
    
    # Probar subida
    success_upload = test_render_upload()
    
    # Probar acceso a imágenes
    success_images = test_render_images()
    
    print("\n" + "="*50)
    print("📊 RESUMEN FINAL DE RENDER")
    print("="*50)
    print(f"✅ Conexión a Render: {'EXITOSA' if success_connection else 'FALLIDA'}")
    print(f"✅ Subida a Render: {'EXITOSA' if success_upload else 'FALLIDA'}")
    print(f"✅ Acceso a imágenes: {'EXITOSA' if success_images else 'FALLIDA'}")
    
    if success_connection and success_upload and success_images:
        print("\n🎉 ¡Render está funcionando perfectamente!")
        print("💡 Las imágenes se suben exitosamente desde Render")
    elif success_connection:
        print("\n⚠️ Render está conectado pero hay problemas con la subida")
    else:
        print("\n❌ Hay problemas de conexión con Render")

if __name__ == '__main__':
    main() 