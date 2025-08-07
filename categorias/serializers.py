import os
from rest_framework import serializers
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import CategoriaProducto


class CategoriaProductoSerializer(serializers.ModelSerializer):
    """
    Serializer para categorías de productos con manejo mejorado de imágenes
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

    def validate_imagen(self, value):
        """
        Validar imagen antes de procesarla
        """
        if value is None:
            return value
            
        # Validar tipo de archivo
        allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/svg+xml']
        if hasattr(value, 'content_type') and value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Tipo de archivo no permitido. Use JPEG, PNG, WEBP, GIF o SVG"
            )
        
        # Validar extensión
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg']
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(
                "Formato de imagen no soportado. Use JPG, PNG, WEBP, GIF o SVG"
            )
        
        # Validar tamaño (máximo 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError(
                "La imagen es demasiado grande. Máximo 10MB"
            )
        
        return value

    def validate(self, attrs):
        """
        Validación personalizada para el serializer
        """
        # Remover slug de la validación si está presente
        attrs.pop('slug', None)
        return attrs

    def create(self, validated_data):
        """
        Crear categoría con manejo mejorado de imágenes
        """
        # Remover slug si está presente para que se genere automáticamente
        validated_data.pop('slug', None)
        
        # Procesar imagen si está presente
        imagen = validated_data.pop('imagen', None)
        
        # Crear la categoría
        categoria = super().create(validated_data)
        
        # Guardar imagen si se proporcionó
        if imagen:
            self._save_imagen(categoria, imagen)
        
        return categoria

    def update(self, instance, validated_data):
        """
        Actualizar categoría con manejo mejorado de imágenes
        """
        # Remover slug si está presente para que se genere automáticamente
        validated_data.pop('slug', None)
        
        # Procesar imagen si está presente
        imagen = validated_data.pop('imagen', None)
        
        # Actualizar la categoría
        categoria = super().update(instance, validated_data)
        
        # Guardar imagen si se proporcionó
        if imagen:
            self._save_imagen(categoria, imagen)
        
        return categoria

    def _save_imagen(self, categoria, imagen):
        """
        Guardar imagen usando el storage configurado (Cloudinary en producción)
        """
        try:
            # Si es un InMemoryUploadedFile, convertirlo a ContentFile
            if isinstance(imagen, InMemoryUploadedFile):
                # Leer el contenido del archivo
                imagen.seek(0)  # Ir al inicio del archivo
                content = imagen.read()
                
                # Crear ContentFile
                content_file = ContentFile(content, name=imagen.name)
                
                # Guardar usando el campo del modelo (esto usará el storage configurado)
                categoria.imagen.save(imagen.name, content_file, save=True)
            else:
                # Para otros tipos de archivo, guardar directamente
                categoria.imagen.save(imagen.name, imagen, save=True)
            
            print(f"✅ Imagen guardada exitosamente para categoría: {categoria.nombre}")
            print(f"📁 Ruta de la imagen: {categoria.imagen.name}")
            print(f"🔗 URL de la imagen: {categoria.imagen.url}")
            
        except Exception as e:
            print(f"❌ Error al guardar imagen: {str(e)}")
            raise serializers.ValidationError({
                "imagen": f"Error al procesar la imagen: {str(e)}"
            })

    def get_imagen_url(self, obj):
        """
        Obtiene la URL de la imagen con manejo mejorado
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

    def to_representation(self, instance):
        """
        Personalizar la representación del serializer
        """
        data = super().to_representation(instance)
        
        # Asegurar que la URL de la imagen esté disponible
        if instance.imagen:
            try:
                request = self.context.get('request')
                if request is not None:
                    data['imagen_url'] = request.build_absolute_uri(instance.imagen.url)
                else:
                    data['imagen_url'] = instance.imagen.url
            except Exception as e:
                print(f"Error generando URL para imagen: {str(e)}")
                data['imagen_url'] = None
        else:
            data['imagen_url'] = None
        
        return data