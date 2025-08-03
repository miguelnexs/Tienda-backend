from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os

@api_view(['GET'])
def debug_environment(request):
    """Debug endpoint para verificar variables de entorno en Render"""
    
    # Obtener variables de entorno
    render_var = os.environ.get('RENDER', 'No definida')
    cloudinary_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'No definida')
    cloudinary_key = os.environ.get('CLOUDINARY_API_KEY', 'No definida')
    cloudinary_secret = os.environ.get('CLOUDINARY_API_SECRET', 'No definida')
    
    # Verificar condiciones
    render_in_env = 'RENDER' in os.environ
    cloudinary_name_in_env = bool(os.environ.get('CLOUDINARY_CLOUD_NAME'))
    condition_total = render_in_env or cloudinary_name_in_env
    
    debug_info = {
        'variables_entorno': {
            'RENDER': render_var,
            'CLOUDINARY_CLOUD_NAME': cloudinary_name,
            'CLOUDINARY_API_KEY': cloudinary_key,
            'CLOUDINARY_API_SECRET': cloudinary_secret[:10] + '...' if cloudinary_secret != 'No definida' else 'No definida'
        },
        'condiciones': {
            'RENDER_in_os.environ': render_in_env,
            'CLOUDINARY_CLOUD_NAME_in_os.environ': cloudinary_name_in_env,
            'condicion_total': condition_total
        },
        'configuracion_django': {
            'DEFAULT_FILE_STORAGE': getattr(request, 'DEFAULT_FILE_STORAGE', 'No disponible'),
            'MEDIA_URL': getattr(request, 'MEDIA_URL', 'No disponible'),
            'MEDIA_ROOT': str(getattr(request, 'MEDIA_ROOT', 'No disponible'))
        }
    }
    
    return Response(debug_info, status=status.HTTP_200_OK) 