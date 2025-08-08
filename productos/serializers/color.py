import os
from rest_framework import serializers
from productos.models import ColorProducto, ImagenProducto


class ImagenProductoSerializer(serializers.ModelSerializer):
    """
    Serializer para imágenes de productos
    """
    url_imagen = serializers.SerializerMethodField()
    
    class Meta:
        model = ImagenProducto
        fields = [
            'id', 'imagen', 'orden', 'es_principal', 
            'fecha_creacion', 'url_imagen'
        ]
        read_only_fields = ['fecha_creacion']

    def get_url_imagen(self, obj):
        """
        Obtiene la URL de la imagen
        """
        if obj.imagen:
            try:
                # Obtener la URL de la imagen
                url = obj.imagen.url
                
                # Si es una URL de Cloudinary, devolverla tal como está
                if 'cloudinary.com' in url:
                    return url
                
                # Si es una URL local, construir la URL completa
                request = self.context.get('request')
                if request is not None:
                    return request.build_absolute_uri(url)
                return url
                
            except Exception as e:
                print(f"Error generando URL para imagen {obj.id}: {str(e)}")
                return None
        return None

    def validate(self, data):
        """
        Validación personalizada para imágenes
        """
        color = data.get('color')
        es_principal = data.get('es_principal', False)
        
        # Si se marca como principal, verificar que no haya otra principal
        if es_principal and color:
            imagenes_principales = ImagenProducto.objects.filter(
                color=color, es_principal=True
            ).exclude(id=self.instance.id if self.instance else None)
            
            if imagenes_principales.exists():
                raise serializers.ValidationError(
                    "Ya existe una imagen principal para este color"
                )
        
        return data

    def create(self, validated_data):
        """
        Crear imagen con manejo seguro
        """
        try:
            # Verificar que la imagen no esté vacía
            imagen = validated_data.get('imagen')
            if not imagen or imagen.size == 0:
                raise serializers.ValidationError("La imagen está vacía")
            
            # Generar nombre único para la imagen
            import uuid
            from django.utils.text import slugify
            
            color = validated_data.get('color')
            producto_nombre = color.producto.nombre if color and color.producto else 'producto'
            color_nombre = color.nombre if color else 'color'
            
            # Obtener extensión del archivo original
            ext = os.path.splitext(imagen.name)[1].lower()
            
            # Crear nombre único
            unique_name = f"productos/colores/{slugify(producto_nombre)}_{slugify(color_nombre)}_{uuid.uuid4().hex}{ext}"
            
            print(f"📤 Procesando imagen para color {color_nombre} de producto {producto_nombre}")
            print(f"📁 Nombre único: {unique_name}")
            
            # Crear la instancia pero no guardar aún
            instance = ImagenProducto(**validated_data)
            
            # Guardar la imagen con el nombre único
            instance.imagen.save(unique_name, imagen, save=False)
            
            # Ahora guardar la instancia
            instance.save()
            
            print(f"✅ Imagen guardada exitosamente")
            print(f"📁 Ruta de la imagen: {instance.imagen.name}")
            
            # Verificar si se guardó en Cloudinary
            if hasattr(instance.imagen, 'url'):
                print(f"🔗 URL de la imagen: {instance.imagen.url}")
                if 'cloudinary.com' in instance.imagen.url:
                    print("☁️ ¡La imagen se subió a Cloudinary!")
                else:
                    print("📁 La imagen se guardó localmente")
                    print("⚠️ Verificar configuración de DEFAULT_FILE_STORAGE")
            
            return instance
            
        except Exception as e:
            print(f"❌ Error al procesar imagen: {str(e)}")
            raise serializers.ValidationError(f"Error al procesar la imagen: {str(e)}")


class ColorProductoSerializer(serializers.ModelSerializer):
    """
    Serializer para colores de productos
    """
    imagenes = ImagenProductoSerializer(many=True, read_only=True)
    cantidad_imagenes = serializers.ReadOnlyField()
    
    class Meta:
        model = ColorProducto
        fields = [
            'id', 'nombre', 'hex_code', 'stock', 'orden', 'activo',
            'fecha_creacion', 'fecha_actualizacion',
            'imagenes', 'cantidad_imagenes'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

    def validate_hex_code(self, value):
        """
        Validar formato de código hexadecimal
        """
        if value and not value.startswith('#'):
            raise serializers.ValidationError(
                "El código hexadecimal debe comenzar con #"
            )
        
        if value and len(value) != 7:
            raise serializers.ValidationError(
                "El código hexadecimal debe tener 7 caracteres (#RRGGBB)"
            )
        
        return value

    def validate_stock(self, value):
        """
        ✅ Validar que el stock no sea negativo
        """
        if value < 0:
            raise serializers.ValidationError(
                "El stock no puede ser negativo"
            )
        return value

    def validate(self, data):
        """
        Validación personalizada para colores
        """
        producto = data.get('producto')
        nombre = data.get('nombre')
        
        # Verificar que no exista otro color con el mismo nombre para el producto
        if producto and nombre:
            existing_color = ColorProducto.objects.filter(
                producto=producto, nombre=nombre
            ).exclude(id=self.instance.id if self.instance else None)
            
            if existing_color.exists():
                raise serializers.ValidationError(
                    f"Ya existe un color con el nombre '{nombre}' para este producto"
                )
        
        return data


class ColorProductoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear colores con imágenes
    """
    imagenes = ImagenProductoSerializer(many=True, required=False)
    
    class Meta:
        model = ColorProducto
        fields = [
            'id', 'nombre', 'hex_code', 'stock', 'orden', 'activo', 'imagenes'
        ]

    def validate_stock(self, value):
        """
        ✅ Validar que el stock no sea negativo
        """
        if value < 0:
            raise serializers.ValidationError(
                "El stock no puede ser negativo"
            )
        return value

    def create(self, validated_data):
        """
        Crear color con sus imágenes
        """
        imagenes_data = validated_data.pop('imagenes', [])
        color = ColorProducto.objects.create(**validated_data)
        
        for imagen_data in imagenes_data:
            ImagenProducto.objects.create(color=color, **imagen_data)
        
        return color

    def update(self, instance, validated_data):
        """
        Actualizar color con sus imágenes
        """
        imagenes_data = validated_data.pop('imagenes', [])
        
        # Actualizar color
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Actualizar imágenes si se proporcionan
        if imagenes_data:
            # Eliminar imágenes existentes
            instance.imagenes.all().delete()
            
            # Crear nuevas imágenes
            for imagen_data in imagenes_data:
                ImagenProducto.objects.create(color=instance, **imagen_data)
        
        return instance


class ColorProductoListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar colores
    """
    imagen_principal_url = serializers.SerializerMethodField()
    cantidad_imagenes = serializers.ReadOnlyField()
    
    class Meta:
        model = ColorProducto
        fields = [
            'id', 'nombre', 'hex_code', 'stock', 'orden', 'activo',
            'imagen_principal_url', 'cantidad_imagenes'
        ]
    
    def get_imagen_principal_url(self, obj):
        """
        Obtener URL de la imagen principal del color
        """
        imagen_principal = obj.imagenes.filter(es_principal=True).first()
        if imagen_principal:
            try:
                # Obtener la URL de la imagen
                url = imagen_principal.imagen.url
                
                # Si es una URL de Cloudinary, devolverla tal como está
                if 'cloudinary.com' in url:
                    return url
                
                # Si es una URL local, construir la URL completa
                request = self.context.get('request')
                if request is not None:
                    return request.build_absolute_uri(url)
                return url
                
            except Exception as e:
                print(f"Error generando URL para imagen de color {obj.nombre}: {str(e)}")
                return None
        
        # Si no hay imagen principal, devolver la primera
        primera_imagen = obj.imagenes.first()
        if primera_imagen:
            try:
                # Obtener la URL de la imagen
                url = primera_imagen.imagen.url
                
                # Si es una URL de Cloudinary, devolverla tal como está
                if 'cloudinary.com' in url:
                    return url
                
                # Si es una URL local, construir la URL completa
                request = self.context.get('request')
                if request is not None:
                    return request.build_absolute_uri(url)
                return url
                
            except Exception as e:
                print(f"Error generando URL para imagen de color {obj.nombre}: {str(e)}")
                return None
        
        return None 