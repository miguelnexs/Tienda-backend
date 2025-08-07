#!/usr/bin/env python
"""
Script para debuggear la configuración de Render
"""
import requests
import json
import time

def debug_render_config():
    """Debuggear la configuración de Render"""
    
    print("🔍 DEBUGGEANDO CONFIGURACIÓN DE RENDER")
    print("="*60)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # 1. Verificar si el servicio responde
        print("📋 1. Verificando respuesta del servicio...")
        
        response = requests.get(f"{RENDER_API_URL}/categorias/", timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ El servicio está respondiendo")
            
            # 2. Verificar si hay errores en la respuesta
            try:
                categorias = response.json()
                print(f"📊 Número de categorías: {len(categorias)}")
                
                # 3. Verificar URLs de imágenes
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
                
                print(f"\n📊 RESUMEN:")
                print(f"☁️ Imágenes en Cloudinary: {cloudinary_count}")
                print(f"📁 Imágenes locales: {local_count}")
                
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                print(f"📊 Response Text: {response.text[:200]}...")
        
        # 4. Probar endpoint de configuración si existe
        print("\n📋 2. Probando endpoints de configuración...")
        
        # Intentar obtener información de configuración
        config_endpoints = [
            f"{RENDER_API_URL}/",
            f"{RENDER_API_URL}/admin/",
            f"{RENDER_API_URL}/api/",
        ]
        
        for endpoint in config_endpoints:
            try:
                response = requests.get(endpoint, timeout=10)
                print(f"📊 {endpoint}: {response.status_code}")
                if response.status_code == 200:
                    print(f"📊 Response: {response.text[:100]}...")
            except Exception as e:
                print(f"❌ Error en {endpoint}: {e}")
        
        # 5. Verificar si hay errores en los logs
        print("\n📋 3. Verificando posibles errores...")
        
        print("🔍 POSIBLES PROBLEMAS:")
        print("1. DJANGO_SETTINGS_MODULE no está configurado correctamente")
        print("2. Hay un error de importación en render_settings.py")
        print("3. El servicio está usando settings.py en lugar de render_settings.py")
        print("4. Hay un problema con la configuración de Cloudinary")
        print("5. El servicio no se reinició completamente")
        
        print("\n💡 ACCIONES DE DEBUG:")
        print("1. Verificar en Render Dashboard que DJANGO_SETTINGS_MODULE=Backend.render_settings")
        print("2. Revisar los logs de Render para errores específicos")
        print("3. Verificar que no hay errores de sintaxis en render_settings.py")
        print("4. Confirmar que el servicio se reinició después del cambio")
        
    except requests.exceptions.Timeout:
        print("❌ Timeout: La petición tardó demasiado")
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión durante la petición")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def check_environment_variables():
    """Verificar variables de entorno"""
    
    print("\n" + "="*60)
    print("🔧 VERIFICANDO VARIABLES DE ENTORNO")
    print("="*60)
    
    print("📋 Variables que deberían estar en Render:")
    print("  DJANGO_SETTINGS_MODULE=Backend.render_settings")
    print("  RENDER=true")
    print("  CLOUDINARY_API_KEY=117225377115856")
    print("  CLOUDINARY_API_SECRET=e0YSrk3sT_70-ijM6mwdFBIWP9w")
    print("  CLOUDINARY_CLOUD_NAME=do1ntnlop")
    print("  DATABASE_URL=postgresql://...")
    print("  DEBUG=False")
    
    print("\n🔍 VERIFICACIONES NECESARIAS:")
    print("1. Ir a https://dashboard.render.com")
    print("2. Seleccionar tu servicio web")
    print("3. Ir a la sección 'Environment'")
    print("4. Verificar que DJANGO_SETTINGS_MODULE=Backend.render_settings")
    print("5. Si no está así, cambiarlo y reiniciar")
    
    print("\n📊 LOGS A REVISAR:")
    print("1. Ir a la sección 'Logs' en Render")
    print("2. Buscar errores como:")
    print("   - ModuleNotFoundError: No module named 'Backend.render_settings'")
    print("   - ImportError")
    print("   - SettingsError")
    print("   - AttributeError")

def main():
    """Función principal"""
    print("🔍 DEBUG DE CONFIGURACIÓN DE RENDER")
    print("="*60)
    
    # Debuggear configuración
    debug_render_config()
    
    # Verificar variables de entorno
    check_environment_variables()
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE DEBUG")
    print("="*60)
    
    print("🔍 EL PROBLEMA ES:")
    print("El servicio está usando almacenamiento local en lugar de Cloudinary")
    print("Esto indica que NO está usando render_settings.py")
    
    print("\n🔧 SOLUCIÓN:")
    print("1. Verificar en Render que DJANGO_SETTINGS_MODULE=Backend.render_settings")
    print("2. Reiniciar el servicio en Render")
    print("3. Esperar 2-3 minutos para que se apliquen los cambios")
    print("4. Verificar los logs de Render para errores específicos")

if __name__ == '__main__':
    main() 