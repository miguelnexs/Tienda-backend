from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0007_merge_migrations'),
    ]

    operations = [
        # Recrear el modelo completo con configuración correcta
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Nombre descriptivo de la categoría', max_length=100, unique=True, verbose_name='Nombre de la categoría')),
                ('slug', models.SlugField(help_text='Identificador único para URLs', max_length=120, unique=True, verbose_name='Slug para URL')),
                ('descripcion', models.TextField(blank=True, help_text='Descripción detallada de la categoría', verbose_name='Descripción')),
                ('imagen', models.ImageField(blank=True, help_text='Imagen representativa de la categoría', null=True, upload_to='categorias/', verbose_name='Imagen de la categoría')),
                ('activa', models.BooleanField(default=True, help_text='Indica si la categoría está disponible', verbose_name='Categoría activa')),
                ('orden', models.PositiveIntegerField(default=0, verbose_name='Orden de visualización')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Fecha de creación')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'Categoría de producto',
                'verbose_name_plural': 'Categorías de productos',
                'ordering': ['orden', 'nombre'],
            },
        ),
        migrations.AddIndex(
            model_name='categoriaproducto',
            index=models.Index(fields=['nombre'], name='categorias__nombre_cbe9e9_idx'),
        ),
        migrations.AddIndex(
            model_name='categoriaproducto',
            index=models.Index(fields=['slug'], name='categorias__slug_aa9e7a_idx'),
        ),
        migrations.AddIndex(
            model_name='categoriaproducto',
            index=models.Index(fields=['activa'], name='categorias__activa_354dfb_idx'),
        ),
        migrations.AddIndex(
            model_name='categoriaproducto',
            index=models.Index(fields=['orden'], name='categorias__orden_a60610_idx'),
        ),
    ] 