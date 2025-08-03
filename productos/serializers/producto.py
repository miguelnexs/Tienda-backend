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
            'variantes', 'colores', 'imagen_principal_url'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'vendidos']

    def get_imagen_principal_url(self, obj):
        """
        Obtiene la URL de la imagen principal con manejo de Cloudinary
        """
        if obj.imagen_principal:
            try:
                # Si estamos en producción (Render) o tenemos Cloudinary configurado
                if 'RENDER' in os.environ or os.environ.get('CLOUDINARY_CLOUD_NAME'):
                    # Usar URL directa de Cloudinary
                    return obj.imagen_principal.url
                else:
                    # En desarrollo, construir URL absoluta
                    request = self.context.get('request')
                    if request is not None:
                        return request.build_absolute_uri(obj.imagen_principal.url)
                    return obj.imagen_principal.url
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