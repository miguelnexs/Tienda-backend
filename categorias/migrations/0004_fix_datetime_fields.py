from django.db import migrations, models
import django.utils.timezone


def fix_datetime_fields(apps, schema_editor):
    """
    Fix any datetime fields that might have invalid values
    """
    CategoriaProducto = apps.get_model('categorias', 'CategoriaProducto')
    
    # Fix CategoriaProducto model datetime fields
    for categoria in CategoriaProducto.objects.all():
        categoria.save()  # This will trigger auto_now_add and auto_now


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0003_alter_categoriaproducto_options_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_datetime_fields, reverse_code=migrations.RunPython.noop),
    ] 