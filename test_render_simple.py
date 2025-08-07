#!/usr/bin/env python
"""
Script simple para probar la subida desde Render
"""
import os
import sys
import requests
import json

def test_render_api_simple():
    """Probar la API de Render de forma simple"""
    
    print("🌐 PROBANDO API DE RENDER")
    print("="*50)
    
    # URL del backend en Render
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # Probar conexión básica
        print("🔍 Probando conexión a Render...")
        response = requests.get(f"{RENDER_API_URL}/productos/")
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            productos = response.json()
            print(f"✅ Conexión exitosa! Productos obtenidos: {len(productos)}")
            
            if productos:
                producto = productos[0]
                print(f"🎯 Primer producto: {producto.get('nombre', 'N/A')} (ID: {producto.get('id', 'N/A')})")
                
                # Probar obtener colores
                producto_id = producto.get('id')
                if producto_id:
                    print(f"\n🔍 Obteniendo colores del producto {producto_id}...")
                    response = requests.get(f"{RENDER_API_URL}/productos/{producto_id}/colores/")
                    
                    if response.status_code == 200:
                        colores = response.json()
                        print(f"✅ Colores obtenidos: {len(colores)}")
                        
                        if colores:
                            color = colores[0]
                            color_id = color.get('id')
                            print(f"🎨 Primer color: {color.get('nombre', 'N/A')} (ID: {color_id})")
                            
                            # Probar obtener imágenes
                            if color_id:
                                print(f"\n🔍 Obteniendo imágenes del color {color_id}...")
                                response = requests.get(f"{RENDER_API_URL}/productos/{producto_id}/colores/{color_id}/imagenes/")
                                
                                if response.status_code == 200:
                                    imagenes = response.json()
                                    print(f"✅ Imágenes obtenidas: {len(imagenes)}")
                                    
                                    for i, imagen in enumerate(imagenes):
                                        print(f"📸 Imagen {i+1}:")
                                        print(f"  ID: {imagen.get('id', 'N/A')}")
                                        print(f"  URL: {imagen.get('imagen', 'N/A')}")
                                        print(f"  Principal: {imagen.get('es_principal', 'N/A')}")
                                        
                                        # Verificar si es Cloudinary
                                        if 'cloudinary.com' in imagen.get('imagen', ''):
                                            print(f"  ☁️ Cloudinary: ✅")
                                        else:
                                            print(f"  📁 Local: ✅")
                                else:
                                    print(f"❌ Error obteniendo imágenes: {response.status_code}")
                            else:
                                print("❌ No hay color_id válido")
                        else:
                            print("❌ No hay colores disponibles")
                    else:
                        print(f"❌ Error obteniendo colores: {response.status_code}")
                else:
                    print("❌ No hay producto_id válido")
            else:
                print("❌ No hay productos disponibles")
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor de Render")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    return True

def test_render_upload_simple():
    """Probar subida simple a Render"""
    
    print("\n" + "="*50)
    print("🚀 PROBANDO SUBIDA SIMPLE A RENDER")
    print("="*50)
    
    # URL del backend en Render
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    # Ruta de la imagen
    image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: La imagen no existe en {image_path}")
        return False
    
    print(f"📁 Imagen encontrada: {image_path}")
    
    try:
        # Obtener productos
        response = requests.get(f"{RENDER_API_URL}/productos/")
        if response.status_code != 200:
            print(f"❌ Error obteniendo productos: {response.status_code}")
            return False
        
        productos = response.json()
        if not productos:
            print("❌ No hay productos disponibles")
            return False
        
        # Usar el primer producto
        producto = productos[0]
        producto_id = producto.get('id')
        print(f"🎯 Usando producto: {producto.get('nombre')} (ID: {producto_id})")
        
        # Obtener colores
        response = requests.get(f"{RENDER_API_URL}/productos/{producto_id}/colores/")
        if response.status_code != 200:
            print(f"❌ Error obteniendo colores: {response.status_code}")
            return False
        
        colores = response.json()
        if not colores:
            print("❌ El producto no tiene colores")
            return False
        
        # Usar el primer color
        color = colores[0]
        color_id = color.get('id')
        print(f"🎨 Usando color: {color.get('nombre')} (ID: {color_id})")
        
        # Preparar subida
        url = f"{RENDER_API_URL}/productos/{producto_id}/colores/{color_id}/imagenes/"
        
        with open(image_path, 'rb') as image_file:
            files = {
                'imagen': ('Bolso-BWXXNG-NEGRO_1.jpg', image_file, 'image/jpeg')
            }
            
            data = {
                'orden': 1,
                'es_principal': True
            }
            
            print(f"\n🚀 Subiendo imagen a: {url}")
            
            response = requests.post(url, files=files, data=data)
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📊 Response: {response.text}")
            
            if response.status_code == 201:
                print("✅ ¡Imagen subida exitosamente desde Render!")
                
                imagen_data = response.json()
                print(f"📸 Imagen creada con ID: {imagen_data.get('id')}")
                print(f"🔗 URL: {imagen_data.get('imagen')}")
                
                # Verificar Cloudinary
                if 'cloudinary.com' in imagen_data.get('imagen', ''):
                    print("☁️ ¡La imagen se subió a Cloudinary desde Render!")
                else:
                    print("📁 La imagen se guardó localmente en Render")
                
                return True
            else:
                print("❌ Error al subir la imagen")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA SIMPLE DE RENDER")
    print("="*50)
    
    # Probar API de Render
    success_api = test_render_api_simple()
    
    # Probar subida a Render
    success_upload = test_render_upload_simple()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS RENDER")
    print("="*50)
    print(f"✅ API de Render: {'EXITOSA' if success_api else 'FALLIDA'}")
    print(f"✅ Subida a Render: {'EXITOSA' if success_upload else 'FALLIDA'}")
    
    if success_api and success_upload:
        print("\n🎉 ¡Render está funcionando correctamente!")
        print("💡 Las imágenes se suben exitosamente desde Render")
    else:
        print("\n❌ Hay problemas con Render")

if __name__ == '__main__':
    main() 