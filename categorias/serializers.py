import os
from rest_framework import serializers
from .models import CategoriaProducto


class CategoriaProductoSerializer(serializers.ModelSerializer):
    """
    Serializer para categorías de productos
    """
    imagen_url = serializers.SerializerMethodField()
    cantidad_productos = serializers.ReadOnlyField()
    
    class Meta:
        model = CategoriaProducto
        fields = [
            'id', 'nombre', 'slug', 'descripcion', 'imagen', 'imagen_url',
            'activa', 'orden', 'fecha_creacion', 'fecha_actualizacion',
            'cantidad_productos'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

    def get_imagen_url(self, obj):
        """
        Obtiene la URL de la imagen con manejo de Cloudinary
        """
        if obj.imagen:
            try:
                # Si estamos en producción (Render) o tenemos Cloudinary configurado
                if 'RENDER' in os.environ or os.environ.get('CLOUDINARY_CLOUD_NAME'):
                    # Usar URL directa de Cloudinary
                    return obj.imagen.url
                else:
                    # En desarrollo, construir URL absoluta
                    request = self.context.get('request')
                    if request is not None:
                        return request.build_absolute_uri(obj.imagen.url)
                    return obj.imagen.url
            except Exception as e:
                print(f"Error generando URL para imagen de categoría {obj.nombre}: {str(e)}")
                return None
        return None