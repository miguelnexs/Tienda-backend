#!/usr/bin/env python
"""
Script para probar el endpoint de debug en Render
"""

import requests
import json

def test_debug_endpoint():
    """Probar el endpoint de debug en Render"""
    print("🔍 Probando endpoint de debug en Render...")
    
    # URL del endpoint de debug
    debug_url = "https://tienda-backend-ap-api.onrender.com/api/productos/debug/environment/"
    
    try:
        # Hacer la petición GET
        response = requests.get(debug_url, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Endpoint de debug funcionando!")
            data = response.json()
            
            print("\n📋 Variables de entorno:")
            for key, value in data.get('variables_entorno', {}).items():
                print(f"   {key}: {value}")
            
            print("\n🎯 Condiciones:")
            for key, value in data.get('condiciones', {}).items():
                print(f"   {key}: {value}")
            
            print("\n🔧 Configuración de Django:")
            for key, value in data.get('configuracion_django', {}).items():
                print(f"   {key}: {value}")
            
            # Verificar si Cloudinary debería estar activo
            condition_total = data.get('condiciones', {}).get('condicion_total', False)
            if condition_total:
                print("\n✅ Cloudinary debería estar activo")
                print("🔧 Si no funciona, el problema está en la configuración de Django")
            else:
                print("\n❌ Cloudinary no debería estar activo")
                print("🔧 Las variables de entorno no están configuradas")
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error al probar endpoint: {e}")

if __name__ == "__main__":
    test_debug_endpoint() 