"""
Configuración forzada de Cloudinary para producción
"""
import os

# Configuración forzada de Cloudinary
CLOUDINARY = {
    'cloud_name': 'do1ntnlop',
    'api_key': '117225377115856',
    'api_secret': 'e0YSrk3sT_70-ijM6mwdFBIWP9w',
}

# Configurar Cloudinary inmediatamente
import cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY['cloud_name'],
    api_key=CLOUDINARY['api_key'],
    api_secret=CLOUDINARY['api_secret']
)

print("🚀 FORZANDO CONFIGURACIÓN DE CLOUDINARY")
print(f"  Cloud Name: {CLOUDINARY['cloud_name']}")
print(f"  API Key: {CLOUDINARY['api_key'][:10]}...")
print("✅ Cloudinary configurado forzadamente") 