"""
Storage simple y directo para Cloudinary
"""
import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile

class SimpleCloudinaryStorage(Storage):
    """
    Storage simple para Cloudinary
    """
    
    def __init__(self):
        self._cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'do1ntnlop')
        self._api_key = os.environ.get('CLOUDINARY_API_KEY', '117225377115856')
        self._api_secret = os.environ.get('CLOUDINARY_API_SECRET', 'e0YSrk3sT_70-ijM6mwdFBIWP9w')
        
        # Configurar Cloudinary inmediatamente
        import cloudinary
        cloudinary.config(
            cloud_name=self._cloud_name,
            api_key=self._api_key,
            api_secret=self._api_secret
        )
        
        print(f"🔧 SimpleCloudinaryStorage inicializado:")
        print(f"  Cloud Name: {self._cloud_name}")
        print(f"  API Key: {self._api_key[:10]}...")
    
    def _open(self, name, mode='rb'):
        """Abrir archivo desde Cloudinary"""
        return ContentFile(f"https://res.cloudinary.com/{self._cloud_name}/image/upload/{name}")
    
    def _save(self, name, content):
        """Guardar archivo en Cloudinary"""
        try:
            import cloudinary.uploader
            
            print(f"📤 Subiendo a Cloudinary: {name}")
            
            # Subir a Cloudinary
            result = cloudinary.uploader.upload(
                content,
                public_id=name,
                overwrite=True,
                invalidate=True
            )
            
            print(f"✅ Subido a Cloudinary:")
            print(f"  Public ID: {result['public_id']}")
            print(f"  URL: {result['secure_url']}")
            
            # Devolver el public_id
            return result['public_id']
            
        except Exception as e:
            print(f"❌ Error subiendo a Cloudinary: {e}")
            raise
    
    def url(self, name):
        """Obtener URL del archivo en Cloudinary"""
        try:
            url = f"https://res.cloudinary.com/{self._cloud_name}/image/upload/{name}"
            print(f"🔗 URL generada: {url}")
            return url
        except Exception as e:
            print(f"❌ Error generando URL: {e}")
            return f"/media/{name}"
    
    def exists(self, name):
        """Verificar si el archivo existe en Cloudinary"""
        try:
            import cloudinary.api
            result = cloudinary.api.resource(name)
            return True
        except:
            return False
    
    def delete(self, name):
        """Eliminar archivo de Cloudinary"""
        try:
            import cloudinary.uploader
            cloudinary.uploader.destroy(name)
            return True
        except:
            return False
    
    def size(self, name):
        """Obtener tamaño del archivo"""
        try:
            import cloudinary.api
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