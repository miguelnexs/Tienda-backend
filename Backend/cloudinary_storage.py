"""
Storage personalizado para Cloudinary
Configurado para desarrollo local sin .env
"""
import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
import cloudinary
import cloudinary.uploader
import cloudinary.api

class CloudinaryStorage(Storage):
    """
    Storage personalizado para Cloudinary
    Configurado para desarrollo local sin variables de entorno
    """
    
    def __init__(self):
        # Configuración para Cloudinary real
        self._cloud_name = "do1ntnlop"
        self._api_key = "117225377115856"
        self._api_secret = "e0YSrk3sT_70-ijM6mwdFBIWP9w"
        
        # Configurar Cloudinary
        cloudinary.config(
            cloud_name=self._cloud_name,
            api_key=self._api_key,
            api_secret=self._api_secret
        )
        
        print(f"🔧 CloudinaryStorage inicializado:")
        print(f"  Cloud Name: {self._cloud_name}")
        print(f"  API Key: {self._api_key[:10]}...")
        print(f"  API Secret: {self._api_secret[:10]}...")
    
    def _open(self, name, mode='rb'):
        """Abrir archivo desde Cloudinary"""
        try:
            # Intentar obtener la URL del archivo
            result = cloudinary.api.resource(name)
            return ContentFile(result['url'])
        except:
            # Si no existe, devolver una URL dummy
            return ContentFile(f"https://res.cloudinary.com/{self._cloud_name}/image/upload/{name}")
    
    def _save(self, name, content):
        """Guardar archivo en Cloudinary"""
        try:
            print(f"📤 Subiendo a Cloudinary: {name}")
            print(f"📁 Tipo de contenido: {type(content)}")
            
            # Leer el contenido y resetear posición
            content_data = content.read()
            print(f"📁 Tamaño del contenido: {len(content_data)} bytes")
            content.seek(0)  # Resetear posición del archivo
            
            # Determinar el tipo de recurso basado en la extensión
            resource_type = "auto"
            if hasattr(content, 'name') and content.name:
                import os
                ext = os.path.splitext(content.name)[1].lower()
                print(f"📁 Extensión del archivo: {ext}")
                if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']:
                    resource_type = "image"
                elif ext in ['.mp4', '.avi', '.mov', '.wmv']:
                    resource_type = "video"
                elif ext in ['.mp3', '.wav', '.ogg']:
                    resource_type = "audio"
                elif ext in ['.txt', '.pdf', '.doc', '.docx']:
                    resource_type = "raw"
            else:
                # Si no hay nombre, intentar determinar por contenido
                if len(content_data) > 0:
                    # Para archivos de texto, usar raw
                    resource_type = "raw"
                else:
                    resource_type = "image"  # Por defecto
            
            print(f"📁 Tipo de recurso: {resource_type}")
            
            # Subir a Cloudinary
            result = cloudinary.uploader.upload(
                content,
                public_id=name,
                resource_type=resource_type,
                overwrite=True,
                invalidate=True
            )
            
            print(f"✅ Subido a Cloudinary:")
            print(f"  Public ID: {result['public_id']}")
            print(f"  URL: {result['secure_url']}")
            print(f"  Tamaño: {result.get('bytes', 0)} bytes")
            
            # Devolver el public_id (nombre del archivo en Cloudinary)
            return result['public_id']
            
        except Exception as e:
            print(f"❌ Error subiendo a Cloudinary: {e}")
            print(f"❌ Tipo de error: {type(e).__name__}")
            # Si falla, intentar con configuración más básica
            try:
                print(f"🔄 Intentando subida básica...")
                content.seek(0)  # Resetear posición del archivo
                result = cloudinary.uploader.upload(
                    content,
                    public_id=name,
                    resource_type="raw",  # Usar raw como fallback
                    overwrite=True
                )
                print(f"✅ Subida exitosa en segundo intento: {result['public_id']}")
                return result['public_id']
            except Exception as e2:
                print(f"❌ Error en segundo intento: {e2}")
                print(f"❌ Tipo de error: {type(e2).__name__}")
                raise
    
    def url(self, name):
        """Obtener URL del archivo en Cloudinary"""
        try:
            # El name aquí es el public_id devuelto por _save
            # Intentar obtener información del archivo para determinar el tipo de recurso
            try:
                result = cloudinary.api.resource(name)
                resource_type = result.get('resource_type', 'image')
            except:
                # Si no se puede obtener, usar image por defecto
                resource_type = 'image'
            
            # Generar URL de Cloudinary con el tipo de recurso correcto
            url = f"https://res.cloudinary.com/{self._cloud_name}/{resource_type}/upload/{name}"
            print(f"🔗 URL generada: {url}")
            return url
        except Exception as e:
            print(f"❌ Error generando URL: {e}")
            return f"/media/{name}"
    
    def exists(self, name):
        """Verificar si el archivo existe en Cloudinary"""
        try:
            # Intentar obtener el recurso
            result = cloudinary.api.resource(name)
            return True
        except Exception as e:
            print(f"⚠️ Archivo no encontrado en Cloudinary: {name} - {e}")
            return False
    
    def delete(self, name):
        """Eliminar archivo de Cloudinary"""
        try:
            cloudinary.uploader.destroy(name)
            print(f"🗑️ Archivo eliminado: {name}")
            return True
        except Exception as e:
            print(f"❌ Error eliminando archivo: {e}")
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
        try:
            result = cloudinary.api.resource(name)
            return result.get('created_at')
        except:
            return None
    
    def get_modified_time(self, name):
        """Obtener tiempo de modificación"""
        return self.get_created_time(name) 