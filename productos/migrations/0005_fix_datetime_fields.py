from django.db import migrations, models
import django.utils.timezone


def fix_datetime_fields(apps, schema_editor):
    """
    Fix any datetime fields that might have invalid values
    """
    Producto = apps.get_model('productos', 'Producto')
    ColorProducto = apps.get_model('productos', 'ColorProducto')
    ImagenProducto = apps.get_model('productos', 'ImagenProducto')
    
    # Fix Producto model datetime fields
    for producto in Producto.objects.all():
        if producto.fecha_publicacion is None:
            producto.fecha_publicacion = None
        producto.save()
    
    # Fix ColorProducto model datetime fields
    for color in ColorProducto.objects.all():
        color.save()  # This will trigger auto_now_add and auto_now
    
    # Fix ImagenProducto model datetime fields
    for imagen in ImagenProducto.objects.all():
        imagen.save()  # This will trigger auto_now_add


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0004_remove_producto_categorias_secundarias'),
    ]

    operations = [
        migrations.RunPython(fix_datetime_fields, reverse_code=migrations.RunPython.noop),
    ] 