"""
Configuración específica para Cloudinary
"""

import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

def configure_cloudinary():
    """
    Configura Cloudinary con las variables de entorno
    """
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
    api_key = os.environ.get('CLOUDINARY_API_KEY')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
    
    if all([cloud_name, api_key, api_secret]):
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        return True
    return False

def is_cloudinary_configured():
    """
    Verifica si Cloudinary está configurado correctamente
    """
    return bool(os.environ.get('CLOUDINARY_CLOUD_NAME'))

def get_cloudinary_url(image_field):
    """
    Obtiene la URL de Cloudinary para un campo de imagen
    """
    if image_field and hasattr(image_field, 'url'):
        return image_field.url
    return None

def upload_to_cloudinary(file, folder="productos"):
    """
    Sube un archivo directamente a Cloudinary
    """
    if not is_cloudinary_configured():
        return None
    
    try:
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type="auto"
        )
        return result.get('secure_url')
    except Exception as e:
        print(f"Error subiendo a Cloudinary: {e}")
        return None 