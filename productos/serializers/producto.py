import os
from rest_framework import serializers
from productos.models import Producto, VarianteProducto, ColorProducto, ImagenProducto
from categorias.serializers import CategoriaProductoSerializer
from .color import ColorProductoSerializer, ImagenProductoSerializer


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer completo para productos
    """
    categoria = CategoriaProductoSerializer(read_only=True)
    categoria_id = serializers.IntegerField(write_only=True, required=False)
    variantes = serializers.SerializerMethodField()
    colores = ColorProductoSerializer(many=True, read_only=True)
    imagen_principal_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = [
            'id', 'sku', 'nombre', 'slug', 'descripcion_corta', 'descripcion_larga',
            'tipo', 'estado', 'categoria', 'categoria_id', 'precio', 'precio_comparacion',
            'costo', 'gestion_stock', 'stock', 'stock_minimo', 'vendidos',
            'peso', 'dimensiones', 'meta_titulo', 'meta_descripcion',
            'fecha_creacion', 'fecha_publicacion', 'fecha_actualizacion',
            'variantes', 'colores', 'imagen_principal_url', 'imagen_principal'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'vendidos', 'slug']

    def get_imagen_principal_url(self, obj):
        """
        Obtiene la URL de la imagen principal
        """
        if obj.imagen_principal:
            try:
                # Obtener la URL de la imagen
                url = obj.imagen_principal.url
                
                # Si es una URL de Cloudinary, devolverla tal como está
                if 'cloudinary.com' in url:
                    return url
                
                # Si es una URL local, construir la URL completa
                request = self.context.get('request')
                if request is not None:
                    return request.build_absolute_uri(url)
                return url
                
            except Exception as e:
                print(f"Error generando URL para imagen principal de producto {obj.slug}: {str(e)}")
                return None
        return None

    def get_variantes(self, obj):
        """
        Obtiene las variantes del producto
        """
        variantes = obj.variantes.all()
        return [
            {
                'id': v.id,
                'nombre': v.nombre,
                'valor': v.valor,
                'sku': v.sku,
                'precio_extra': v.precio_extra,
                'stock': v.stock,
                'orden': v.orden
            }
            for v in variantes
        ]

    def validate(self, attrs):
        """
        Validación personalizada para el serializer
        """
        # Remover slug de la validación si está presente
        attrs.pop('slug', None)
        print(f"🔍 ProductoSerializer.validate - attrs después de remover slug: {attrs}")
        return attrs

    def create(self, validated_data):
        """
        Crear producto con slug automático y manejo de imagen
        """
        # Remover slug si está presente para que se genere automáticamente
        validated_data.pop('slug', None)
        
        # Obtener la imagen si existe
        imagen = validated_data.pop('imagen_principal', None)
        
        # Crear el producto
        producto = super().create(validated_data)
        
        # Procesar imagen si se proporcionó
        if imagen:
            self._process_image(producto, imagen)
        
        return producto

    def update(self, instance, validated_data):
        """
        Actualizar producto con slug automático y manejo de imagen
        """
        # Remover slug si está presente para que se genere automáticamente
        validated_data.pop('slug', None)
        
        # Obtener la imagen si existe
        imagen = validated_data.pop('imagen_principal', None)
        
        # Actualizar el producto
        producto = super().update(instance, validated_data)
        
        # Procesar imagen si se proporcionó
        if imagen:
            self._process_image(producto, imagen)
        
        return producto

    def _process_image(self, producto, imagen):
        """
        Procesar y guardar imagen de manera segura
        """
        try:
            # Verificar que la imagen no esté vacía
            if not imagen or imagen.size == 0:
                print(f"⚠️ Imagen vacía para producto: {producto.nombre}")
                return
            
            # Generar nombre único para la imagen
            import uuid
            import os
            from django.utils.text import slugify
            
            # Obtener extensión del archivo original
            ext = os.path.splitext(imagen.name)[1].lower()
            
            # Crear nombre único
            unique_name = f"productos/{slugify(producto.nombre)}_{uuid.uuid4().hex}{ext}"
            
            print(f"📤 Procesando imagen para producto: {producto.nombre}")
            print(f"📁 Nombre único: {unique_name}")
            
            # Guardar la imagen directamente sin leerla primero
            producto.imagen_principal.save(unique_name, imagen, save=True)
            
            print(f"✅ Imagen guardada exitosamente para producto: {producto.nombre}")
            print(f"📁 Ruta de la imagen: {producto.imagen_principal.name}")
            
            # Verificar si se guardó en Cloudinary
            if hasattr(producto.imagen_principal, 'url'):
                print(f"🔗 URL de la imagen: {producto.imagen_principal.url}")
                if 'cloudinary.com' in producto.imagen_principal.url:
                    print("☁️ ¡La imagen se subió a Cloudinary!")
                else:
                    print("📁 La imagen se guardó localmente")
                    print("⚠️ Verificar configuración de DEFAULT_FILE_STORAGE")
            
        except Exception as e:
            print(f"❌ Error al procesar imagen: {str(e)}")
            # No lanzar excepción para no interrumpir la creación del producto
            # Solo registrar el error y continuar
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error al procesar imagen para producto {producto.nombre}: {str(e)}")
            # No lanzar la excepción para evitar error 500
            return