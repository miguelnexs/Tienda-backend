from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import os


def get_cloudinary_storage():
    """Obtiene el storage de Cloudinary solo si está disponible"""
    try:
        from cloudinary_storage.storage import MediaCloudinaryStorage
        return MediaCloudinaryStorage()
    except (ImportError, Exception):
        return None


class CategoriaProducto(models.Model):
    """
    Modelo para categorías de productos
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Nombre de la categoría"),
        help_text=_("Nombre descriptivo de la categoría")
    )
    
    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name=_("Slug para URL"),
        help_text=_("Identificador único para URLs")
    )
    
    descripcion = models.TextField(
        blank=True,
        verbose_name=_("Descripción"),
        help_text=_("Descripción detallada de la categoría")
    )
    
    imagen = models.ImageField(
        upload_to='categorias/',
        blank=True,
        null=True,
        verbose_name=_("Imagen de la categoría"),
        help_text=_("Imagen representativa de la categoría"),
        storage=get_cloudinary_storage()
    )
    
    activa = models.BooleanField(
        default=True,
        verbose_name=_("Categoría activa"),
        help_text=_("Indica si la categoría está disponible")
    )
    
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Orden de visualización")
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de creación")
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Fecha de actualización")
    )

    class Meta:
        verbose_name = _("Categoría de producto")
        verbose_name_plural = _("Categorías de productos")
        ordering = ['orden', 'nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['slug']),
            models.Index(fields=['activa']),
            models.Index(fields=['orden']),
        ]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Generar slug automáticamente si no existe
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    @property
    def cantidad_productos(self):
        """Retorna la cantidad de productos en esta categoría"""
        return self.productos.count()