import os
from rest_framework import serializers
from productos.models import ColorProducto, ImagenProducto


class ImagenProductoSerializer(serializers.ModelSerializer):
    """
    Serializer para imágenes de productos con mejor manejo de Cloudinary
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
        Obtiene la URL de la imagen con mejor manejo de Cloudinary
        """
        if obj.imagen:
            try:
                # Construir URL absoluta
                request = self.context.get('request')
                if request is not None:
                    return request.build_absolute_uri(obj.imagen.url)
                return obj.imagen.url
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


class ColorProductoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer mejorado para crear colores con imágenes
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
        Crear color con sus imágenes - Versión mejorada
        """
        imagenes_data = validated_data.pop('imagenes', [])
        color = ColorProducto.objects.create(**validated_data)
        
        print(f"🔄 Creando color: {color.nombre} (stock: {color.stock})")
        
        # Crear imágenes si se proporcionan
        for i, imagen_data in enumerate(imagenes_data):
            try:
                # Asegurar que la primera imagen sea principal si no hay ninguna
                if i == 0 and not any(img.get('es_principal', False) for img in imagenes_data):
                    imagen_data['es_principal'] = True
                
                imagen = ImagenProducto.objects.create(color=color, **imagen_data)
                print(f"✅ Imagen {i+1} creada: {imagen.imagen.name}")
                print(f"   URL: {imagen.imagen.url}")
                
            except Exception as e:
                print(f"❌ Error creando imagen {i+1}: {e}")
                # Continuar con las demás imágenes
        
        return color

    def update(self, instance, validated_data):
        """
        Actualizar color con sus imágenes - Versión mejorada
        """
        imagenes_data = validated_data.pop('imagenes', [])
        
        # Actualizar color
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        print(f"🔄 Actualizando color: {instance.nombre}")
        
        # Actualizar imágenes si se proporcionan
        if imagenes_data:
            # Eliminar imágenes existentes
            instance.imagenes.all().delete()
            print(f"🗑️ Imágenes anteriores eliminadas")
            
            # Crear nuevas imágenes
            for i, imagen_data in enumerate(imagenes_data):
                try:
                    # Asegurar que la primera imagen sea principal si no hay ninguna
                    if i == 0 and not any(img.get('es_principal', False) for img in imagenes_data):
                        imagen_data['es_principal'] = True
                    
                    imagen = ImagenProducto.objects.create(color=instance, **imagen_data)
                    print(f"✅ Imagen {i+1} actualizada: {imagen.imagen.name}")
                    print(f"   URL: {imagen.imagen.url}")
                    
                except Exception as e:
                    print(f"❌ Error actualizando imagen {i+1}: {e}")
                    # Continuar con las demás imágenes
        
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
                request = self.context.get('request')
                if request is not None:
                    # Construir URL absoluta
                    return request.build_absolute_uri(imagen_principal.imagen.url)
                return imagen_principal.imagen.url
            except Exception as e:
                print(f"Error generando URL para imagen de color {obj.nombre}: {str(e)}")
                return None
        
        # Si no hay imagen principal, devolver la primera
        primera_imagen = obj.imagenes.first()
        if primera_imagen:
            try:
                request = self.context.get('request')
                if request is not None:
                    # Construir URL absoluta
                    return request.build_absolute_uri(primera_imagen.imagen.url)
                return primera_imagen.imagen.url
            except Exception as e:
                print(f"Error generando URL para imagen de color {obj.nombre}: {str(e)}")
                return None
        
        return None 