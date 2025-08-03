#!/usr/bin/env python
"""
Script para verificar el estado del despliegue en Render
"""

import requests
import time

def check_render_status():
    """Verificar el estado de la API en Render"""
    print("🔍 Verificando estado de Render...")
    
    api_url = "https://tienda-backend-ap-api.onrender.com/api/productos/productos/"
    
    try:
        # Hacer una petición simple para verificar el estado
        response = requests.get(api_url, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ API funcionando correctamente")
            
            # Verificar si hay headers específicos de Render
            headers = dict(response.headers)
            if 'rndr-id' in headers:
                print(f"🆔 Render ID: {headers['rndr-id']}")
            if 'x-render-origin-server' in headers:
                print(f"🖥️  Server: {headers['x-render-origin-server']}")
                
        else:
            print(f"❌ API no responde correctamente: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error al verificar Render: {e}")

def check_environment_variables():
    """Verificar si las variables de entorno están activas"""
    print("\n🔧 Verificando variables de entorno...")
    
    # Hacer una petición a un endpoint que nos dé información sobre la configuración
    try:
        # Intentar obtener información de configuración
        response = requests.get("https://tienda-backend-ap-api.onrender.com/api/", timeout=10)
        
        if response.status_code == 200:
            print("✅ API responde correctamente")
            print("📝 Nota: Las variables de entorno solo se pueden verificar desde el servidor")
            print("🔍 Para verificar si Cloudinary está configurado, necesitamos crear un producto nuevo")
        else:
            print(f"❌ Error al verificar configuración: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def force_redeploy_check():
    """Verificar si hay un redespliegue en progreso"""
    print("\n🔄 Verificando si hay redespliegue en progreso...")
    
    # Hacer múltiples peticiones para ver si hay cambios
    for i in range(3):
        try:
            response = requests.get("https://tienda-backend-ap-api.onrender.com/api/productos/productos/", timeout=5)
            print(f"📡 Petición {i+1}: Status {response.status_code}")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Error en petición {i+1}: {e}")

if __name__ == "__main__":
    check_render_status()
    check_environment_variables()
    force_redeploy_check()
    
    print("\n📋 Instrucciones para forzar redespliegue:")
    print("1. Ve a tu dashboard de Render")
    print("2. Selecciona tu servicio 'tienda-backend-api'")
    print("3. Ve a la pestaña 'Manual Deploy'")
    print("4. Haz clic en 'Deploy latest commit'")
    print("5. Espera a que termine el despliegue")
    print("6. Ejecuta nuevamente el script de prueba") 