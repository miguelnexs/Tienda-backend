from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0004_fix_datetime_fields'),
        ('categorias', '0003_alter_categoriaproducto_options_and_more'),
    ]

    operations = [
        # Esta migración de merge resuelve el conflicto
        # No necesita operaciones específicas
    ] 