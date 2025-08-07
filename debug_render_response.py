#!/usr/bin/env python
"""
Script para debuggear la respuesta de Render
"""
import requests
import json

def debug_render_response():
    """Debuggear la respuesta de Render"""
    
    print("🔍 DEBUGGEANDO RESPUESTA DE RENDER")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        print("🔍 Obteniendo productos...")
        response = requests.get(f"{RENDER_API_URL}/productos/", timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"📊 Content-Length: {response.headers.get('content-length', 'N/A')}")
        
        print(f"\n📄 Response Text (primeros 500 caracteres):")
        print(response.text[:500])
        
        print(f"\n📄 Response Text (completo):")
        print(response.text)
        
        print(f"\n🔍 Intentando parsear JSON...")
        try:
            data = response.json()
            print(f"✅ JSON parseado exitosamente")
            print(f"📊 Tipo de datos: {type(data)}")
            print(f"📊 Longitud: {len(data) if isinstance(data, (list, dict)) else 'N/A'}")
            
            if isinstance(data, list):
                print(f"📊 Es una lista con {len(data)} elementos")
                if data:
                    print(f"📊 Primer elemento: {data[0]}")
                    print(f"📊 Tipo del primer elemento: {type(data[0])}")
            elif isinstance(data, dict):
                print(f"📊 Es un diccionario con claves: {list(data.keys())}")
            else:
                print(f"📊 Es de tipo: {type(data)}")
                
        except json.JSONDecodeError as e:
            print(f"❌ Error parseando JSON: {e}")
            print(f"📄 Texto que causó el error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_render_upload_debug():
    """Probar subida con debug completo"""
    
    print("\n" + "="*50)
    print("🚀 PROBANDO SUBIDA CON DEBUG")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
    
    try:
        # Obtener productos
        print("🔍 Obteniendo productos...")
        response = requests.get(f"{RENDER_API_URL}/productos/", timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Productos obtenidos: {len(data) if isinstance(data, list) else 'N/A'}")
            
            if isinstance(data, list) and data:
                producto = data[0]
                producto_id = producto.get('id')
                print(f"🎯 Producto: {producto.get('nombre')} (ID: {producto_id})")
                
                # Obtener colores
                print("🔍 Obteniendo colores...")
                response = requests.get(f"{RENDER_API_URL}/productos/{producto_id}/colores/", timeout=30)
                
                if response.status_code == 200:
                    colores = response.json()
                    print(f"✅ Colores obtenidos: {len(colores) if isinstance(colores, list) else 'N/A'}")
                    
                    if isinstance(colores, list) and colores:
                        color = colores[0]
                        color_id = color.get('id')
                        print(f"🎨 Color: {color.get('nombre')} (ID: {color_id})")
                        
                        # Probar subida
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
                            print(f"📊 Response Text: {response.text}")
                            
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
                                    return False
                            else:
                                print(f"❌ Error al subir la imagen: {response.status_code}")
                                return False
                    else:
                        print("❌ No hay colores disponibles")
                else:
                    print(f"❌ Error obteniendo colores: {response.status_code}")
            else:
                print("❌ No hay productos disponibles")
        else:
            print(f"❌ Error obteniendo productos: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 DEBUG DE RENDER")
    print("="*50)
    
    # Debuggear respuesta
    debug_render_response()
    
    # Probar subida con debug
    test_render_upload_debug()

if __name__ == '__main__':
    main() 