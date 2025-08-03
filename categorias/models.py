from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from cloudinary_storage.storage import MediaCloudinaryStorage

class CategoriaBase(models.Model):
    """
    Modelo base abstracto para categorías genéricas
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Nombre"),
        help_text=_("Nombre único de la categoría")
    )
    
    slug = models.SlugField(
        max_length=110,
        unique=True,
        verbose_name=_("Slug"),
        help_text=_("Identificador único para URLs")
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Descripción"),
        help_text=_("Información adicional sobre la categoría")
    )
    
    activa = models.BooleanField(
        default=True,
        verbose_name=_("Activa"),
        help_text=_("Indica si la categoría está disponible")
    )
    
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Orden de visualización")
    )
    
    imagen = models.ImageField(
        upload_to='categorias/',
        blank=True,
        null=True,
        verbose_name=_("Imagen representativa"),
        storage=MediaCloudinaryStorage()
    )

    class Meta:
        abstract = True
        ordering = ['orden', 'nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class CategoriaProducto(CategoriaBase):
    """
    Modelo específico para categorías de productos
    """
    class Meta:
        verbose_name = _("Categoría de producto")
        verbose_name_plural = _("Categorías de productos")

    @property
    def cantidad_productos(self):
        from productos.models import Producto
        return Producto.objects.filter(categoria=self).count()

    @property
    def productos_vinculados(self):
        from productos.models import Producto
        return Producto.objects.filter(categoria=self)