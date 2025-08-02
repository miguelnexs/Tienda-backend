from rest_framework import serializers
from .models import Cliente, Venta, ItemVenta
from productos.models import Producto, VarianteProducto, ColorProducto

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id', 'nombre', 'email', 'telefono', 'tipo_documento',
            'numero_documento', 'direccion', 'fecha_registro', 'activo'
        ]

class ColorProductoSerializer(serializers.ModelSerializer):
    """Serializer para información básica de colores en ventas"""
    class Meta:
        model = ColorProducto
        fields = ['id', 'nombre', 'hex_code', 'stock', 'activo']

class ItemVentaSerializer(serializers.ModelSerializer):
    producto = serializers.StringRelatedField(read_only=True)
    variante = serializers.StringRelatedField(read_only=True)
    color = ColorProductoSerializer(read_only=True)
    precio_unitario = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = ItemVenta
        fields = [
            'id', 'producto', 'variante', 'color', 'cantidad',
            'precio_unitario', 'descuento_item', 'subtotal'
        ]

class VentaSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    items = ItemVentaSerializer(many=True, read_only=True)
    cliente_nombre = serializers.CharField(read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id', 'numero_venta', 'fecha_venta', 'cliente', 'cliente_nombre',
            'subtotal', 'descuento', 'total', 'estado', 'metodo_pago',
            'observaciones', 'vendedor', 'items'
        ]

class VentaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = [
            'cliente', 'cliente_nombre', 'estado', 'metodo_pago',
            'observaciones', 'vendedor'
        ]
        read_only_fields = ['numero_venta', 'fecha_venta', 'subtotal', 'descuento', 'igv', 'total'] 