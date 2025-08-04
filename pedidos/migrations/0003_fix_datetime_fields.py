from django.db import migrations, models
import django.utils.timezone


def fix_datetime_fields(apps, schema_editor):
    """
    Fix any datetime fields that might have invalid values
    """
    Pedido = apps.get_model('pedidos', 'Pedido')
    HistorialPedido = apps.get_model('pedidos', 'HistorialPedido')
    
    # Fix Pedido model datetime fields
    for pedido in Pedido.objects.all():
        pedido.save()  # This will trigger auto_now_add
    
    # Fix HistorialPedido model datetime fields
    for historial in HistorialPedido.objects.all():
        historial.save()  # This will trigger auto_now_add


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_itempedido_color'),
    ]

    operations = [
        migrations.RunPython(fix_datetime_fields, reverse_code=migrations.RunPython.noop),
    ] 