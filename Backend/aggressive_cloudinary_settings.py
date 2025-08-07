"""
Configuración agresiva de Cloudinary para forzar su uso
"""
import os
import sys

# Configuración agresiva de Cloudinary
CLOUDINARY_CONFIG = {
    'cloud_name': 'do1ntnlop',
    'api_key': '117225377115856',
    'api_secret': 'e0YSrk3sT_70-ijM6mwdFBIWP9w',
}

# Configurar Cloudinary inmediatamente
import cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CONFIG['cloud_name'],
    api_key=CLOUDINARY_CONFIG['api_key'],
    api_secret=CLOUDINARY_CONFIG['api_secret']
)

print("🚀 CONFIGURACIÓN AGRESIVA DE CLOUDINARY ACTIVADA")
print(f"  Cloud Name: {CLOUDINARY_CONFIG['cloud_name']}")
print(f"  API Key: {CLOUDINARY_CONFIG['api_key'][:10]}...")
print("✅ Cloudinary configurado agresivamente")

# Forzar configuración de Django
os.environ['CLOUDINARY_CLOUD_NAME'] = CLOUDINARY_CONFIG['cloud_name']
os.environ['CLOUDINARY_API_KEY'] = CLOUDINARY_CONFIG['api_key']
os.environ['CLOUDINARY_API_SECRET'] = CLOUDINARY_CONFIG['api_secret']
os.environ['RENDER'] = 'true'

print("🔧 Variables de entorno forzadas") 