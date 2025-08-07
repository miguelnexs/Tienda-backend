#!/usr/bin/env python
"""
Script para verificar si Render está usando render_settings.py
"""
import requests
import json
import time

def check_render_settings():
    """Verificar configuración de Render"""
    
    print("🔍 VERIFICANDO CONFIGURACIÓN DE RENDER")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # 1. Verificar si el servicio responde
        print("📋 1. Verificando respuesta del servicio...")
        
        response = requests.get(f"{RENDER_API_URL}/categorias/", timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ El servicio está respondiendo")
            
            # 2. Verificar configuración de CORS
            cors_header = response.headers.get('Access-Control-Allow-Origin')
            print(f"🌐 CORS Header: {cors_header}")
            
            # 3. Verificar si hay categorías
            try:
                categorias = response.json()
                print(f"📊 Número de categorías: {len(categorias)}")
                
                # 4. Verificar URLs de imágenes
                cloudinary_count = 0
                local_count = 0
                
                for categoria in categorias:
                    if isinstance(categoria, dict) and categoria.get('imagen_url'):
                        if 'cloudinary.com' in categoria['imagen_url']:
                            cloudinary_count += 1
                        elif 'onrender.com/media' in categoria['imagen_url']:
                            local_count += 1
                
                print(f"☁️ Imágenes en Cloudinary: {cloudinary_count}")
                print(f"📁 Imágenes locales: {local_count}")
                
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                print(f"📊 Response Text: {response.text[:200]}...")
        
        # 5. Probar crear una categoría para ver la configuración actual
        print("\n📋 2. Probando crear categoría para verificar configuración...")
        
        # Buscar imagen de prueba
        from pathlib import Path
        imagen_path = Path("D:/usuario/Downloads/bolso/cartera-casual-para-mujer-23064.jpg")
        
        if imagen_path.exists():
            # Preparar datos
            data = {
                'nombre': 'Check Render Settings',
                'descripcion': 'Verificación de configuración de Render',
                'activa': True,
                'orden': 989
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
                        print("☁️ ¡EXCELENTE! Usando Cloudinary")
                        print("✅ El servicio está usando render_settings.py")
                        return True
                    else:
                        print("📁 Usando almacenamiento local")
                        print("⚠️ El servicio NO está usando render_settings.py")
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

def check_environment_variables():
    """Verificar variables de entorno"""
    
    print("\n" + "="*50)
    print("🔧 VERIFICANDO VARIABLES DE ENTORNO")
    print("="*50)
    
    print("📋 Variables de entorno que deberían estar en Render:")
    print("  DJANGO_SETTINGS_MODULE=Backend.render_settings ✅")
    print("  RENDER=true ✅")
    print("  CLOUDINARY_API_KEY=117225377115856 ✅")
    print("  CLOUDINARY_API_SECRET=e0YSrk3sT_70-ijM6mwdFBIWP9w ✅")
    print("  CLOUDINARY_CLOUD_NAME=do1ntnlop ✅")
    print("  DATABASE_URL=postgresql://... ✅")
    print("  DEBUG=False ✅")
    
    print("\n💡 Si las imágenes siguen guardándose localmente:")
    print("1. Verificar que el servicio se haya reiniciado completamente")
    print("2. Revisar los logs de Render en el dashboard")
    print("3. Verificar que no hay errores en el build")
    print("4. Confirmar que DJANGO_SETTINGS_MODULE está configurado correctamente")

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DE RENDER")
    print("="*50)
    
    # Verificar configuración
    config_ok = check_render_settings()
    
    # Verificar variables de entorno
    check_environment_variables()
    
    print("\n" + "="*50)
    print("📊 RESUMEN")
    print("="*50)
    
    if config_ok:
        print("🎉 ¡PERFECTO! Render está usando render_settings.py")
        print("✅ Las imágenes se subirán a Cloudinary")
    else:
        print("⚠️ Render NO está usando render_settings.py")
        print("🔧 Las imágenes se guardan localmente")
        print("\n💡 ACCIONES NECESARIAS:")
        print("1. Verificar en Render que DJANGO_SETTINGS_MODULE=Backend.render_settings")
        print("2. Reiniciar el servicio en Render")
        print("3. Esperar unos minutos para que se apliquen los cambios")
        print("4. Verificar los logs de Render para errores")

if __name__ == '__main__':
    main() 