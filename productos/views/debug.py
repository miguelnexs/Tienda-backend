from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings

@api_view(['GET'])
def debug_environment(request):
    """Debug endpoint para verificar variables de entorno en Render"""
    
    # Obtener variables de entorno
    render_var = os.environ.get('RENDER', 'No definida')
    
    # Verificar condiciones
    render_in_env = 'RENDER' in os.environ
    
    # Obtener configuración de Django
    debug_info = {
        'variables_entorno': {
            'RENDER': render_var,
        },
        'condiciones': {
            'RENDER_in_os.environ': render_in_env,
        },
        'configuracion_django': {
            'DEFAULT_FILE_STORAGE': getattr(settings, 'DEFAULT_FILE_STORAGE', 'No disponible'),
            'MEDIA_URL': getattr(settings, 'MEDIA_URL', 'No disponible'),
            'MEDIA_ROOT': str(getattr(settings, 'MEDIA_ROOT', 'No disponible')),
            'DEBUG': getattr(settings, 'DEBUG', 'No disponible'),
            'ALLOWED_HOSTS': getattr(settings, 'ALLOWED_HOSTS', 'No disponible')
        }
    }
    
    return Response(debug_info, status=status.HTTP_200_OK) 