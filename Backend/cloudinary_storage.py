"""
Storage personalizado para Cloudinary
"""
import os
import cloudinary
import cloudinary.uploader
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings

class CloudinaryStorage(Storage):
    """
    Storage personalizado para Cloudinary
    """
    
    def __init__(self):
        # Configurar Cloudinary
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', 'do1ntnlop'),
            api_key=os.environ.get('CLOUDINARY_API_KEY', '117225377115856'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET', 'e0YSrk3sT_70-ijM6mwdFBIWP9w')
        )
    
    def _open(self, name, mode='rb'):
        """Abrir archivo desde Cloudinary"""
        # Para archivos en Cloudinary, devolver URL
        return ContentFile(f"https://res.cloudinary.com/{cloudinary.config().cloud_name}/image/upload/{name}")
    
    def _save(self, name, content):
        """Guardar archivo en Cloudinary"""
        try:
            # Determinar el tipo de recurso basado en la extensión
            resource_type = "auto"
            if hasattr(content, 'name'):
                ext = os.path.splitext(content.name)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']:
                    resource_type = "image"
                elif ext in ['.mp4', '.avi', '.mov', '.wmv']:
                    resource_type = "video"
                elif ext in ['.mp3', '.wav', '.ogg']:
                    resource_type = "audio"
            
            # Subir a Cloudinary
            result = cloudinary.uploader.upload(
                content,
                public_id=name,
                resource_type=resource_type,
                overwrite=True,
                invalidate=True
            )
            
            # Devolver el public_id (nombre del archivo en Cloudinary)
            return result['public_id']
            
        except Exception as e:
            print(f"❌ Error subiendo a Cloudinary: {e}")
            # Si falla, intentar con configuración más básica
            try:
                result = cloudinary.uploader.upload(
                    content,
                    public_id=name,
                    overwrite=True
                )
                return result['public_id']
            except Exception as e2:
                print(f"❌ Error en segundo intento: {e2}")
                raise
    
    def url(self, name):
        """Obtener URL del archivo en Cloudinary"""
        try:
            cloud_name = cloudinary.config().cloud_name
            return f"https://res.cloudinary.com/{cloud_name}/image/upload/{name}"
        except:
            return f"/media/{name}"
    
    def exists(self, name):
        """Verificar si el archivo existe en Cloudinary"""
        try:
            result = cloudinary.api.resource(name)
            return True
        except:
            return False
    
    def delete(self, name):
        """Eliminar archivo de Cloudinary"""
        try:
            cloudinary.uploader.destroy(name)
            return True
        except:
            return False
    
    def size(self, name):
        """Obtener tamaño del archivo"""
        try:
            result = cloudinary.api.resource(name)
            return result.get('bytes', 0)
        except:
            return 0
    
    def get_accessed_time(self, name):
        """Obtener tiempo de acceso"""
        return None
    
    def get_created_time(self, name):
        """Obtener tiempo de creación"""
        return None
    
    def get_modified_time(self, name):
        """Obtener tiempo de modificación"""
        return None 