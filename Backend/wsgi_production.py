"""
WSGI config for Backend project - Production version.
"""

import os
from django.core.wsgi import get_wsgi_application

# Forzar configuración de producción
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')

# Inicializar aplicación WSGI
application = get_wsgi_application() 