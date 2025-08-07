#!/usr/bin/env python
"""
Script corregido para probar Render con las URLs correctas
"""
import requests
import json

def test_render_correct():
    """Probar Render con las URLs correctas"""
    
    print("🌐 PROBANDO RENDER CON URLs CORRECTAS")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # Obtener las URLs de la API
        print("🔍 Obteniendo URLs de la API...")
        response = requests.get(f"{RENDER_API_URL}/productos/", timeout=30)
        
        if response.status_code == 200:
            api_urls = response.json()
            print(f"✅ URLs obtenidas: {api_urls}")
            
            # Usar la URL correcta para productos
            productos_url = api_urls.get('productos')
            if productos_url:
                print(f"\n🔍 Obteniendo productos desde: {productos_url}")
                
                response = requests.get(productos_url, timeout=30)
                
                if response.status_code == 200:
                    productos = response.json()
                    print(f"✅ Productos obtenidos: {len(productos) if isinstance(productos, list) else 'N/A'}")
                    
                    if isinstance(productos, list) and productos:
                        producto = productos[0]
                        producto_id = producto.get('id')
                        print(f"🎯 Producto: {producto.get('nombre')} (ID: {producto_id})")
                        
                        # Obtener colores del producto
                        colores_url = f"{RENDER_API_URL}/productos/{producto_id}/colores/"
                        print(f"\n🔍 Obteniendo colores desde: {colores_url}")
                        
                        response = requests.get(colores_url, timeout=30)
                        
                        if response.status_code == 200:
                            colores = response.json()
                            print(f"✅ Colores obtenidos: {len(colores) if isinstance(colores, list) else 'N/A'}")
                            
                            if isinstance(colores, list) and colores:
                                color = colores[0]
                                color_id = color.get('id')
                                print(f"🎨 Color: {color.get('nombre')} (ID: {color_id})")
                                
                                # Probar subida de imagen
                                imagenes_url = f"{RENDER_API_URL}/productos/{producto_id}/colores/{color_id}/imagenes/"
                                print(f"\n🚀 Subiendo imagen a: {imagenes_url}")
                                
                                # Ruta de la imagen
                                image_path = r"D:\usuario\Downloads\bolso\Bolso-BWXXNG-NEGRO_1.jpg"
                                
                                with open(image_path, 'rb') as image_file:
                                    files = {
                                        'imagen': ('Bolso-BWXXNG-NEGRO_1.jpg', image_file, 'image/jpeg')
                                    }
                                    
                                    data = {
                                        'orden': 1,
                                        'es_principal': True
                                    }
                                    
                                    response = requests.post(imagenes_url, files=files, data=data, timeout=60)
                                    
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
            else:
                print("❌ No se encontró la URL de productos")
        else:
            print(f"❌ Error obteniendo URLs: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_render_images_correct():
    """Probar acceso a imágenes con URLs correctas"""
    
    print("\n" + "="*50)
    print("🔍 PROBANDO ACCESO A IMÁGENES CON URLs CORRECTAS")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # Obtener URLs de la API
        response = requests.get(f"{RENDER_API_URL}/productos/", timeout=30)
        if response.status_code != 200:
            print("❌ Error obteniendo URLs")
            return False
        
        api_urls = response.json()
        productos_url = api_urls.get('productos')
        
        if not productos_url:
            print("❌ No se encontró la URL de productos")
            return False
        
        # Obtener productos
        response = requests.get(productos_url, timeout=30)
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
        colores_url = f"{RENDER_API_URL}/productos/{producto_id}/colores/"
        response = requests.get(colores_url, timeout=30)
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
        imagenes_url = f"{RENDER_API_URL}/productos/{producto_id}/colores/{color_id}/imagenes/"
        response = requests.get(imagenes_url, timeout=30)
        
        if response.status_code == 200:
            try:
                imagenes = response.json()
                print(f"✅ Imágenes obtenidas: {len(imagenes) if isinstance(imagenes, list) else 'N/A'}")
                
                if isinstance(imagenes, list):
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
    print("🧪 PRUEBA CORREGIDA DE RENDER")
    print("="*50)
    
    # Probar subida con URLs correctas
    success_upload = test_render_correct()
    
    # Probar acceso a imágenes con URLs correctas
    success_images = test_render_images_correct()
    
    print("\n" + "="*50)
    print("📊 RESUMEN CORREGIDO DE RENDER")
    print("="*50)
    print(f"✅ Subida a Render: {'EXITOSA' if success_upload else 'FALLIDA'}")
    print(f"✅ Acceso a imágenes: {'EXITOSA' if success_images else 'FALLIDA'}")
    
    if success_upload and success_images:
        print("\n🎉 ¡Render está funcionando correctamente!")
        print("💡 Las imágenes se suben exitosamente desde Render")
    else:
        print("\n❌ Hay problemas con Render")

if __name__ == '__main__':
    main() 