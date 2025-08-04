from django.db import migrations
import django.utils.timezone


def fix_datetime_emergency(apps, schema_editor):
    """
    Emergency fix for datetime fields that might have invalid values
    """
    CategoriaProducto = apps.get_model('categorias', 'CategoriaProducto')
    
    # Update all existing records to have proper datetime values
    for categoria in CategoriaProducto.objects.all():
        # Set proper datetime values if they're invalid
        if not hasattr(categoria, 'fecha_creacion') or categoria.fecha_creacion is None:
            categoria.fecha_creacion = django.utils.timezone.now()
        if not hasattr(categoria, 'fecha_actualizacion') or categoria.fecha_actualizacion is None:
            categoria.fecha_actualizacion = django.utils.timezone.now()
        categoria.save()


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0004_fix_datetime_fields'),
    ]

    operations = [
        migrations.RunPython(fix_datetime_emergency, reverse_code=migrations.RunPython.noop),
    ] 