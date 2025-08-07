import os
from rest_framework import serializers
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import CategoriaProducto

class CategoriaProductoSerializer(serializers.ModelSerializer):
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
        Validar que el nombre no esté vacío y no sea duplicado
        """
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        
        # Obtener la instancia actual si estamos actualizando
        instance = getattr(self, 'instance', None)
        
        # Verificar si ya existe una categoría con el mismo nombre
        # Excluir la instancia actual si estamos actualizando
        queryset = CategoriaProducto.objects.filter(nombre__iexact=value.strip())
        if instance:
            queryset = queryset.exclude(pk=instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("Ya existe una categoría con este nombre")
        
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
        Validación general del serializer
        """
        # Remover slug si está presente para que se genere automáticamente
        attrs.pop('slug', None)
        return attrs

    def create(self, validated_data):
        """
        Crear categoría con manejo simplificado de imágenes
        """
        # Remover slug si está presente
        validated_data.pop('slug', None)
        
        # Obtener la imagen si existe
        imagen = validated_data.pop('imagen', None)
        
        # Crear la categoría
        categoria = super().create(validated_data)
        
        # Procesar imagen si se proporcionó
        if imagen:
            self._process_image(categoria, imagen)
        
        return categoria

    def update(self, instance, validated_data):
        """
        Actualizar categoría con manejo simplificado de imágenes
        """
        # Remover slug si está presente
        validated_data.pop('slug', None)
        
        # Obtener la imagen si existe
        imagen = validated_data.pop('imagen', None)
        
        # Actualizar la categoría
        categoria = super().update(instance, validated_data)
        
        # Procesar imagen si se proporcionó
        if imagen:
            self._process_image(categoria, imagen)
        
        return categoria

    def _process_image(self, categoria, imagen):
        """
        Procesar y guardar imagen de manera simplificada
        """
        try:
            # Verificar que la imagen no esté vacía
            if not imagen or imagen.size == 0:
                print(f"⚠️ Imagen vacía para categoría: {categoria.nombre}")
                return
            
            # Verificar si la imagen ya fue procesada (ya tiene URL)
            if categoria.imagen and categoria.imagen.url:
                print(f"✅ Imagen ya procesada para categoría: {categoria.nombre}")
                return
            
            # Generar nombre único para la imagen
            import uuid
            import os
            from django.utils.text import slugify
            
            # Obtener extensión del archivo original
            ext = os.path.splitext(imagen.name)[1].lower()
            
            # Crear nombre único
            unique_name = f"categorias/{slugify(categoria.nombre)}_{uuid.uuid4().hex}{ext}"
            
            print(f"📤 Procesando imagen para categoría: {categoria.nombre}")
            print(f"📁 Nombre único: {unique_name}")
            
            # Guardar la imagen directamente sin leerla primero
            categoria.imagen.save(unique_name, imagen, save=True)
            
            print(f"✅ Imagen guardada exitosamente para categoría: {categoria.nombre}")
            print(f"📁 Ruta de la imagen: {categoria.imagen.name}")
            
            # Verificar si se guardó en Cloudinary
            if hasattr(categoria.imagen, 'url'):
                print(f"🔗 URL de la imagen: {categoria.imagen.url}")
                if 'cloudinary.com' in categoria.imagen.url:
                    print("☁️ ¡La imagen se subió a Cloudinary!")
                else:
                    print("📁 La imagen se guardó localmente")
                    print("⚠️ Verificar configuración de DEFAULT_FILE_STORAGE")
            
        except Exception as e:
            print(f"❌ Error al procesar imagen: {str(e)}")
            # No lanzar excepción para no interrumpir la creación de la categoría
            # Solo registrar el error y continuar
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error al procesar imagen para categoría {categoria.nombre}: {str(e)}")
            # No lanzar la excepción para evitar error 500
            return

    def get_imagen_url(self, obj):
        """
        Obtener URL de la imagen
        """
        if obj.imagen:
            try:
                # Obtener la URL de la imagen
                if hasattr(obj.imagen, 'url'):
                    url = obj.imagen.url
                    
                    # Si es una URL de Cloudinary, devolverla tal como está
                    if 'cloudinary.com' in url:
                        return url
                    
                    # Si es una URL local, construir la URL completa
                    request = self.context.get('request')
                    if request is not None:
                        return request.build_absolute_uri(url)
                    return url
                
                return None
            except Exception as e:
                print(f"Error generando URL para imagen de categoría {obj.nombre}: {str(e)}")
                return None
        return None

    def to_representation(self, instance):
        """
        Personalizar la representación del serializer
        """
        data = super().to_representation(instance)
        
        # Asegurar que imagen_url esté presente
        if instance.imagen:
            try:
                url = instance.imagen.url
                
                # Si es una URL de Cloudinary, usarla directamente
                if 'cloudinary.com' in url:
                    data['imagen_url'] = url
                    data['imagen'] = url  # También actualizar el campo imagen
                else:
                    # Para URLs locales, construir la URL completa
                    request = self.context.get('request')
                    if request is not None:
                        full_url = request.build_absolute_uri(url)
                        data['imagen_url'] = full_url
                        data['imagen'] = full_url
                    else:
                        data['imagen_url'] = url
                        data['imagen'] = url
            except Exception as e:
                print(f"Error generando URL para imagen: {str(e)}")
                data['imagen_url'] = None
                data['imagen'] = None
        else:
            data['imagen_url'] = None
            data['imagen'] = None
        
        return data