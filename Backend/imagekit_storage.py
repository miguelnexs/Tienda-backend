"""
Storage personalizado para ImageKit.io
"""
import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

class ImageKitStorage(Storage):
    """
    Storage personalizado para ImageKit.io
    """
    
    def __init__(self):
        self._public_key = os.environ.get('IMAGEKIT_PUBLIC_KEY')
        self._private_key = os.environ.get('IMAGEKIT_PRIVATE_KEY')
        self._url_endpoint = os.environ.get('IMAGEKIT_URL_ENDPOINT')
        
        # Configurar ImageKit inmediatamente
        self._imagekit = ImageKit(
            private_key=self._private_key,
            public_key=self._public_key,
            url_endpoint=self._url_endpoint
        )
        
        print(f"🔧 ImageKitStorage inicializado:")
        print(f"  Public Key: {self._public_key[:10] if self._public_key else 'NO ENCONTRADA'}...")
        print(f"  URL Endpoint: {self._url_endpoint}")
    
    def _open(self, name, mode='rb'):
        """Abrir archivo desde ImageKit"""
        return ContentFile(f"{self._url_endpoint}/{name}")
    
    def _save(self, name, content):
        """Guardar archivo en ImageKit"""
        try:
            print(f"📤 Subiendo a ImageKit: {name}")
            
            # Configurar opciones de subida
            options = UploadFileRequestOptions(
                use_unique_file_name=False,
                tags=["django-upload"],
                response_fields=["is_private_file", "tags"],
                folder="/productos/"
            )
            
            # Subir a ImageKit
            result = self._imagekit.upload_file(
                file=content,
                file_name=name,
                options=options
            )
            
            print(f"✅ Subido a ImageKit:")
            print(f"  File ID: {result.file_id}")
            print(f"  URL: {result.url}")
            
            # Devolver el nombre del archivo
            return name
            
        except Exception as e:
            print(f"❌ Error subiendo a ImageKit: {e}")
            raise
    
    def url(self, name):
        """Obtener URL del archivo en ImageKit"""
        try:
            url = f"{self._url_endpoint}/{name}"
            print(f"🔗 URL generada: {url}")
            return url
        except Exception as e:
            print(f"❌ Error generando URL: {e}")
            return f"/media/{name}"
    
    def exists(self, name):
        """Verificar si el archivo existe en ImageKit"""
        try:
            # Buscar archivo por nombre
            result = self._imagekit.list_files()
            # Buscar el archivo en la lista
            for file in result.list:
                if file.name == name.split('/')[-1]:
                    return True
            return False
        except:
            return False
    
    def delete(self, name):
        """Eliminar archivo de ImageKit"""
        try:
            # Primero buscar el archivo para obtener su ID
            result = self._imagekit.list_files()
            
            # Buscar el archivo en la lista
            for file in result.list:
                if file.name == name.split('/')[-1]:
                    self._imagekit.delete_file(file.file_id)
                    print(f"🗑️ Archivo eliminado: {name}")
                    return True
            return False
        except Exception as e:
            print(f"❌ Error eliminando archivo: {e}")
            return False
    
    def size(self, name):
        """Obtener tamaño del archivo"""
        try:
            result = self._imagekit.list_files()
            # Buscar el archivo en la lista
            for file in result.list:
                if file.name == name.split('/')[-1]:
                    return file.size
            return 0
        except:
            return 0
    
    def get_accessed_time(self, name):
        """Obtener tiempo de acceso"""
        return None
    
    def get_created_time(self, name):
        """Obtener tiempo de creación"""
        try:
            result = self._imagekit.list_files()
            # Buscar el archivo en la lista
            for file in result.list:
                if file.name == name.split('/')[-1]:
                    return file.created_at
            return None
        except:
            return None
    
    def get_modified_time(self, name):
        """Obtener tiempo de modificación"""
        return self.get_created_time(name) 