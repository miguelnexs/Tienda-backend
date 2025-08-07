"""
Configuración específica para Render
"""
import os
from .settings import *
import dj_database_url

# DEBUG: Verificar si este archivo se está cargando
print("🚀 RENDER_SETTINGS.PY CARGADO - CONFIGURACIÓN DE PRODUCCIÓN ACTIVA")

# Configuración específica para Render
DEBUG = False

# Configuración de base de datos para Render
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Configuración de archivos estáticos para Render
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Configuración de archivos media para Render
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de Cloudinary para Render (producción)
CLOUDINARY = {
    'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME', 'do1ntnlop'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY', '1172253771'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET', 'e0YSrk3sT_'),
}

# Configurar Cloudinary para almacenamiento en producción
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Configurar Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY['cloud_name'],
    api_key=CLOUDINARY['api_key'],
    api_secret=CLOUDINARY['api_secret']
)

# FORZAR configuración de Cloudinary para Render
# En producción (Render), usar Cloudinary para archivos media
# IMPORTANTE: Usar nuestro storage personalizado
DEFAULT_FILE_STORAGE = 'Backend.cloudinary_storage.CloudinaryStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# DEBUG: Verificar configuración de Cloudinary
print(f"☁️ CLOUDINARY CONFIGURADO:")
print(f"  Cloud Name: {CLOUDINARY['cloud_name']}")
print(f"  API Key: {CLOUDINARY['api_key'][:10]}...")
print(f"  DEFAULT_FILE_STORAGE: {DEFAULT_FILE_STORAGE}")

# Configuración de seguridad para producción
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Configuración de CORS para Render - CORREGIDA
CORS_ALLOWED_ORIGINS = [
    "https://sobrio-estilo-tienda-main.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://tienda-backend-qsre.onrender.com",
]

# Configuración de logging para Render
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Configuración de archivos de imagen
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB

# Configuración de timezone
USE_TZ = True
TIME_ZONE = 'UTC'

# Configuración de sesiones
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 horas

# Configuración de caché (usar memoria en Render)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# DEBUG: Confirmar que la configuración se aplicó
print("✅ CONFIGURACIÓN DE RENDER APLICADA CORRECTAMENTE")
print(f"  DEFAULT_FILE_STORAGE: {DEFAULT_FILE_STORAGE}")
print(f"  STATICFILES_STORAGE: {STATICFILES_STORAGE}") 