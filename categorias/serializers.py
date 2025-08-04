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
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'slug']

    def validate_nombre(self, value):
        """
        Validar que el nombre sea único
        """
        if not value or value.strip() == '':
            raise serializers.ValidationError("El nombre de la categoría es requerido")
        
        # Verificar si ya existe una categoría con el mismo nombre
        instance = getattr(self, 'instance', None)
        if CategoriaProducto.objects.filter(nombre__iexact=value.strip()).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("Ya existe una categoría con ese nombre")
        
        return value.strip()

    def create(self, validated_data):
        """
        Crear categoría con slug automático
        """
        # El slug se generará automáticamente en el modelo
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Actualizar categoría con slug automático
        """
        # El slug se generará automáticamente en el modelo si el nombre cambió
        return super().update(instance, validated_data)

    def get_imagen_url(self, obj):
        """
        Obtiene la URL de la imagen
        """
        if obj.imagen:
            try:
                # Construir URL absoluta
                request = self.context.get('request')
                if request is not None:
                    return request.build_absolute_uri(obj.imagen.url)
                return obj.imagen.url
            except Exception as e:
                print(f"Error generando URL para imagen de categoría {obj.nombre}: {str(e)}")
                return None
        return None