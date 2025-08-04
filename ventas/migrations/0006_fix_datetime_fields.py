from django.db import migrations, models
import django.utils.timezone


def fix_datetime_fields(apps, schema_editor):
    """
    Fix any datetime fields that might have invalid values
    """
    Cliente = apps.get_model('ventas', 'Cliente')
    Venta = apps.get_model('ventas', 'Venta')
    
    # Fix Cliente model datetime fields
    for cliente in Cliente.objects.all():
        cliente.save()  # This will trigger auto_now_add
    
    # Fix Venta model datetime fields
    for venta in Venta.objects.all():
        venta.save()  # This will trigger auto_now_add


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_fix_venta_usuario_id_column'),
    ]

    operations = [
        migrations.RunPython(fix_datetime_fields, reverse_code=migrations.RunPython.noop),
    ] 