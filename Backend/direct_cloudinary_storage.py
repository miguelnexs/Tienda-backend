"""
Storage directo para Cloudinary con credenciales hardcodeadas
"""
import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile

class DirectCloudinaryStorage(Storage):
    """
    Storage directo para Cloudinary
    """
    
    def __init__(self):
        # Credenciales hardcodeadas para asegurar funcionamiento
        self._cloud_name = 'do1ntnlop'
        self._api_key = '117225377115856'
        self._api_secret = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'
        
        # Configurar Cloudinary inmediatamente
        import cloudinary
        cloudinary.config(
            cloud_name=self._cloud_name,
            api_key=self._api_key,
            api_secret=self._api_secret
        )
        
        print(f"🔧 DirectCloudinaryStorage inicializado:")
        print(f"  Cloud Name: {self._cloud_name}")
        print(f"  API Key: {self._api_key[:10]}...")
        print("✅ Cloudinary configurado directamente")
    
    def _open(self, name, mode='rb'):
        """Abrir archivo desde Cloudinary"""
        return ContentFile(f"https://res.cloudinary.com/{self._cloud_name}/image/upload/{name}")
    
    def _save(self, name, content):
        """Guardar archivo en Cloudinary"""
        try:
            import cloudinary.uploader
            
            print(f"📤 SUBIENDO A CLOUDINARY: {name}")
            print(f"  Tamaño del archivo: {len(content.read())} bytes")
            content.seek(0)  # Resetear posición del archivo
            
            # Subir a Cloudinary
            result = cloudinary.uploader.upload(
                content,
                public_id=name,
                overwrite=True,
                invalidate=True
            )
            
            print(f"✅ SUBIDO A CLOUDINARY EXITOSAMENTE:")
            print(f"  Public ID: {result['public_id']}")
            print(f"  URL: {result['secure_url']}")
            print(f"  Tamaño: {result.get('bytes', 0)} bytes")
            
            # Devolver el public_id
            return result['public_id']
            
        except Exception as e:
            print(f"❌ ERROR SUBIENDO A CLOUDINARY: {e}")
            import traceback
            traceback.print_exc()
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