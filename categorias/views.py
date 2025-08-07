from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.text import slugify
from django.core.files.images import get_image_dimensions
from categorias.models import CategoriaProducto
from categorias.serializers import CategoriaProductoSerializer
import os
import logging

logger = logging.getLogger(__name__)

class CategoriaViewSet(viewsets.ModelViewSet):
    """
    Vista completa para categorías (CRUD)
    """
    queryset = CategoriaProducto.objects.all().order_by('orden', 'nombre')
    serializer_class = CategoriaProductoSerializer
    lookup_field = 'slug'
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = []

    def create(self, request, *args, **kwargs):
        """Crear categoría con mejor manejo de errores"""
        try:
            logger.info(f"Creando categoría con datos: {request.data}")
            logger.info(f"Archivos recibidos: {request.FILES}")
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                logger.info("Vista: Serializer válido")
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                logger.error(f"Errores de validación: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error al crear categoría: {str(e)}")
            return Response(
                {"error": f"Error interno del servidor: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        """Actualizar categoría con mejor manejo de errores"""
        try:
            logger.info(f"Actualizando categoría con datos: {request.data}")
            logger.info(f"Archivos recibidos: {request.FILES}")
            
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            else:
                logger.error(f"Errores de validación: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error al actualizar categoría: {str(e)}")
            return Response(
                {"error": f"Error interno del servidor: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        """Crear categoría con validación de imagen"""
        instance = serializer.save()
        if not instance.slug:
            instance.slug = slugify(instance.nombre)
            instance.save()
        
        # Validar imagen si se proporcionó
        if 'imagen' in self.request.FILES:
            self._validate_and_save_image(instance, self.request.FILES['imagen'])

    def perform_update(self, serializer):
        """Actualizar categoría con validación de imagen"""
        instance = serializer.save()
        
        # Validar imagen si se proporcionó
        if 'imagen' in self.request.FILES:
            self._validate_and_save_image(instance, self.request.FILES['imagen'])

    def _validate_and_save_image(self, categoria, imagen):
        """Validar y guardar imagen de categoría"""
        try:
            # Verificar que la imagen no esté vacía
            if not imagen or imagen.size == 0:
                logger.warning(f"Imagen vacía para categoría: {categoria.nombre}")
                return
            
            # Validar tipo de archivo
            allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/svg+xml']
            if imagen.content_type not in allowed_types:
                raise serializers.ValidationError({
                    "imagen": "Tipo de archivo no permitido. Use JPEG, PNG, WEBP, GIF o SVG"
                })
            
            # Validar extensión
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg']
            ext = os.path.splitext(imagen.name)[1].lower()
            if ext not in valid_extensions:
                raise serializers.ValidationError({
                    "imagen": "Formato de imagen no soportado. Use JPG, PNG, WEBP, GIF o SVG"
                })
            
            # Validar tamaño (máximo 10MB para desarrollo)
            if imagen.size > 10 * 1024 * 1024:
                raise serializers.ValidationError({
                    "imagen": "La imagen es demasiado grande. Máximo 10MB"
                })
            
            # Verificar si el archivo ya fue leído
            current_position = imagen.tell()
            if current_position > 0:
                # El archivo ya fue leído, resetear posición
                imagen.seek(0)
            
            # Verificar que el contenido no esté vacío
            content_data = imagen.read()
            if len(content_data) == 0:
                logger.warning(f"Imagen sin contenido para categoría: {categoria.nombre}")
                return
            
            # Resetear posición del archivo
            imagen.seek(0)
            
            # Guardar imagen usando el storage de Cloudinary
            from django.core.files.base import ContentFile
            content_file = ContentFile(content_data, name=imagen.name)
            
            # Guardar usando el campo del modelo
            categoria.imagen.save(imagen.name, content_file, save=True)
            logger.info(f"Imagen guardada exitosamente para categoría: {categoria.nombre}")
            
        except Exception as e:
            logger.error(f"Error al procesar imagen: {str(e)}")
            # No lanzar la excepción para evitar error 500
            # Solo registrar el error y continuar
            return

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_imagen(self, request, slug=None):
        """Endpoint para subir imagen a categoría"""
        categoria = self.get_object()
        
        if 'imagen' not in request.FILES:
            return Response(
                {"error": "No se proporcionó imagen en el campo 'imagen'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            self._validate_and_save_image(categoria, request.FILES['imagen'])
            return Response(
                self.get_serializer(categoria).data,
                status=status.HTTP_200_OK
            )
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error al subir imagen: {str(e)}")
            return Response(
                {"error": f"Error interno del servidor: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )