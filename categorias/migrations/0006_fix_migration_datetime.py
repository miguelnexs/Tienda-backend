from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0005_emergency_datetime_fix'),
    ]

    operations = [
        # Fix the fecha_creacion field to have proper default
        migrations.AlterField(
            model_name='categoriaproducto',
            name='fecha_creacion',
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name='Fecha de creación'
            ),
        ),
        # Fix the descripcion field to remove invalid default
        migrations.AlterField(
            model_name='categoriaproducto',
            name='descripcion',
            field=models.TextField(
                blank=True,
                help_text='Descripción detallada de la categoría',
                verbose_name='Descripción'
            ),
        ),
    ] 