#!/usr/bin/env python
"""
Script final para probar la API de Render con subida a Cloudinary
"""
import requests
import json
from pathlib import Path
from datetime import datetime

def test_render_api_cloudinary():
    """Probar API de Render con subida a Cloudinary"""
    
    print("🌐 PRUEBA FINAL DE API DE RENDER CON CLOUDINARY")
    print("="*60)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # 1. Verificar respuesta del servicio
        print("📋 1. Verificando respuesta del servicio...")
        
        response = requests.get(f"{RENDER_API_URL}/categorias/", timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ El servicio está respondiendo")
            
            try:
                categorias = response.json()
                print(f"📊 Número de categorías: {len(categorias)}")
                
                # Verificar URLs de imágenes existentes
                cloudinary_count = 0
                local_count = 0
                
                for categoria in categorias:
                    if isinstance(categoria, dict) and categoria.get('imagen_url'):
                        if 'cloudinary.com' in categoria['imagen_url']:
                            cloudinary_count += 1
                            print(f"☁️ Cloudinary: {categoria['imagen_url']}")
                        elif 'onrender.com/media' in categoria['imagen_url']:
                            local_count += 1
                            print(f"📁 Local: {categoria['imagen_url']}")
                
                print(f"\n📊 RESUMEN DE IMÁGENES EXISTENTES:")
                print(f"☁️ Imágenes en Cloudinary: {cloudinary_count}")
                print(f"📁 Imágenes locales: {local_count}")
                
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                return False
        
        # 2. Crear nueva categoría con imagen
        print("\n📋 2. Creando categoría con imagen...")
        
        # Generar nombre único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_categoria = f"Test Final Cloudinary {timestamp}"
        
        # Buscar imagen de prueba
        imagen_path = Path("D:/usuario/Downloads/bolso/cartera-casual-para-mujer-23064.jpg")
        
        if imagen_path.exists():
            # Preparar datos
            data = {
                'nombre': nombre_categoria,
                'descripcion': f'Prueba final de Cloudinary - {timestamp}',
                'activa': True,
                'orden': 995
            }
            
            # Preparar archivo
            files = {
                'imagen': ('cartera-casual-para-mujer-23064.jpg', open(imagen_path, 'rb'), 'image/jpeg')
            }
            
            # Crear categoría
            response = requests.post(
                f"{RENDER_API_URL}/categorias/",
                data=data,
                files=files,
                timeout=30
            )
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 201:
                try:
                    categoria = response.json()
                    print("✅ ¡Categoría creada exitosamente!")
                    print(f"📸 ID: {categoria['id']}")
                    print(f"🏷️ Nombre: {categoria['nombre']}")
                    print(f"🔗 URL de la imagen: {categoria['imagen_url']}")
                    
                    # Verificar configuración
                    if 'cloudinary.com' in categoria['imagen_url']:
                        print("☁️ ¡EXCELENTE! La imagen se subió a Cloudinary")
                        print("✅ El servicio está usando Cloudinary correctamente")
                        return True
                    else:
                        print("📁 La imagen se guardó localmente")
                        print("⚠️ El servicio NO está usando Cloudinary")
                        return False
                        
                except json.JSONDecodeError as e:
                    print(f"❌ Error decodificando respuesta: {e}")
                    print(f"📊 Response Text: {response.text}")
                    return False
            else:
                print(f"❌ Error creando categoría: {response.status_code}")
                print(f"📊 Response: {response.text}")
                return False
        else:
            print("❌ No se encontró la imagen de prueba")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: La petición tardó demasiado")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión durante la petición")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 PRUEBA FINAL DE API DE RENDER")
    print("="*60)
    
    # Probar API de Render
    api_ok = test_render_api_cloudinary()
    
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL")
    print("="*60)
    print(f"✅ API de Render: {'EXITOSA' if api_ok else 'FALLIDA'}")
    
    if api_ok:
        print("🎉 ¡PERFECTO! La API de Render funciona con Cloudinary")
        print("✅ Las imágenes se suben a Cloudinary desde Render")
        print("✅ El problema está completamente resuelto")
        print("✅ Los serializers funcionan correctamente")
    else:
        print("❌ La API de Render no está usando Cloudinary")
        print("🔧 El problema persiste en Render")
        print("💡 Posibles causas:")
        print("1. Render no ha aplicado los cambios aún")
        print("2. Hay un error en la configuración de Render")
        print("3. El storage personalizado no se está cargando en Render")

if __name__ == '__main__':
    main() 