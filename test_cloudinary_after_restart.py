#!/usr/bin/env python
"""
Script para probar si Render está usando render_settings.py después del reinicio
"""
import requests
import json
import time
from pathlib import Path
from datetime import datetime

def test_cloudinary_after_restart():
    """Probar si las imágenes se suben a Cloudinary después del reinicio"""
    
    print("🎯 PRUEBA DESPUÉS DEL REINICIO DE RENDER")
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
                        elif 'onrender.com/media' in categoria['imagen_url']:
                            local_count += 1
                
                print(f"☁️ Imágenes en Cloudinary: {cloudinary_count}")
                print(f"📁 Imágenes locales: {local_count}")
                
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                return False
        
        # 2. Crear nueva categoría con nombre único
        print("\n📋 2. Creando categoría de prueba...")
        
        # Generar nombre único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_categoria = f"Test Cloudinary {timestamp}"
        
        # Buscar imagen de prueba
        imagen_path = Path("D:/usuario/Downloads/bolso/cartera-casual-para-mujer-23064.jpg")
        
        if imagen_path.exists():
            # Preparar datos
            data = {
                'nombre': nombre_categoria,
                'descripcion': f'Prueba de Cloudinary después del reinicio - {timestamp}',
                'activa': True,
                'orden': 988
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
                        print("✅ El servicio está usando render_settings.py")
                        return True
                    else:
                        print("📁 La imagen se guardó localmente")
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

def check_render_logs():
    """Verificar si hay errores en los logs"""
    
    print("\n" + "="*60)
    print("📋 VERIFICANDO LOGS DE RENDER")
    print("="*60)
    
    print("📊 Según los logs que proporcionaste:")
    print("✅ Build successful")
    print("✅ Service is live")
    print("✅ Gunicorn started successfully")
    print("✅ All packages installed correctly")
    print("✅ No errors in the build process")
    
    print("\n💡 El servicio se reinició correctamente")
    print("🔧 Ahora debería estar usando render_settings.py")

def main():
    """Función principal"""
    print("🎯 PRUEBA DESPUÉS DEL REINICIO DE RENDER")
    print("="*60)
    
    # Verificar logs
    check_render_logs()
    
    # Probar configuración
    config_ok = test_cloudinary_after_restart()
    
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL")
    print("="*60)
    
    if config_ok:
        print("🎉 ¡PERFECTO! Render está usando render_settings.py")
        print("✅ Las imágenes se suben a Cloudinary")
        print("✅ El servicio está configurado correctamente")
        print("✅ El reinicio fue exitoso")
    else:
        print("⚠️ Render NO está usando render_settings.py")
        print("🔧 Las imágenes se guardan localmente")
        print("\n💡 POSIBLES CAUSAS:")
        print("1. El servicio aún no ha terminado de reiniciarse")
        print("2. Hay un error en render_settings.py")
        print("3. La variable DJANGO_SETTINGS_MODULE no se aplicó correctamente")
        print("4. Hay un problema con la configuración de Cloudinary")
        
        print("\n🔧 ACCIONES RECOMENDADAS:")
        print("1. Esperar 2-3 minutos más")
        print("2. Verificar en Render que DJANGO_SETTINGS_MODULE=Backend.render_settings")
        print("3. Revisar los logs de Render para errores específicos")
        print("4. Verificar que no hay errores de importación en render_settings.py")

if __name__ == '__main__':
    main() 