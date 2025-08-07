"""
Configuración forzada para Cloudinary
Este archivo se importa en settings.py para forzar el uso de Cloudinary
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Configurar Cloudinary con credenciales hardcodeadas
cloudinary.config(
    cloud_name="do1ntnlop",
    api_key="117225377115856",
    api_secret="e0YSrk3sT_70-ijM6mwdFBIWP9w"
)

print("🔧 Cloudinary configurado en force_cloudinary_settings.py")
print(f"  Cloud Name: do1ntnlop")
print(f"  API Key: 117225377115856")
print(f"  API Secret: e0YSrk3sT_70-ijM6mwdFBIWP9w") 