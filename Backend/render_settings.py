"""
Configuración específica para Render
"""
import os
from .settings import *

# Configuración específica para Render
DEBUG = False

# Configuración de base de datos para Render
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'tienda_production'),
        'USER': os.environ.get('DATABASE_USER', 'tienda_user'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
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

# En producción (Render), usar Cloudinary para archivos media
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

# Configuración adicional para Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY['cloud_name'],
    'API_KEY': CLOUDINARY['api_key'],
    'API_SECRET': CLOUDINARY['api_secret'],
    'STATIC_IMAGES_EXTENSIONS': ['jpg', 'jpe', 'jpeg', 'jpc', 'jp2', 'j2k', 'wdp', 'jxr', 
                                'hdp', 'png', 'gif', 'webp', 'bmp', 'tif', 'tiff', 'ico'],
    'MAGIC_FILE_PATH': 'magic',
    'STATIC_IMAGES_TRANSFORMATIONS': {
        'default': {
            'quality': 'auto',
            'fetch_format': 'auto',
        }
    }
}

# Configuración de seguridad para producción
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Configuración de CORS para Render
CORS_ALLOWED_ORIGINS = [
    "https://sobrio-estilo-tienda-main.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
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