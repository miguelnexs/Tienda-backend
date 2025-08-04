from pathlib import Path
import os
import psycopg2.extensions
import dj_database_url
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()



BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', default='default-secret-key')

DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ['*']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME') 
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'corsheaders',
    'rest_framework',
    'colorfield',
    'django_filters',
    'rest_framework_simplejwt',
    'nested_admin',
    'cloudinary_storage',  # Para almacenamiento de imágenes en la nube
    # 'debug_toolbar',  # Comentado temporalmente para producción
    
    # Local apps
    'productos.apps.ProductosConfig',
    'categorias',
    'ventas',
    'pedidos',
    # 'drf_spectacular',  # Comentado temporalmente para evitar problemas
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # CSRF deshabilitado para APIs - se maneja por authentication
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Agregar debug toolbar solo en desarrollo
if DEBUG:
    # MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')  # Comentado temporalmente para producción
    pass

ROOT_URLCONF = 'Backend.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'Backend.wsgi.application'

# Configuración de base de datos
if 'DATABASE_URL' in os.environ:
    # Producción: usar DATABASE_URL de Render
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
    # Agregar opciones específicas para PostgreSQL
    DATABASES['default']['OPTIONS'] = {
        'client_encoding': 'UTF8',
        'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
    }
else:
    # Desarrollo: usar configuración local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'tiendadb',
            'USER': 'productos',
            'PASSWORD': 'migel1457',
            'HOST': 'localhost',
            'PORT': '5432',
            'OPTIONS': {
                'client_encoding': 'UTF8',
                'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
            },
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    # Deshabilitadas para desarrollo
    # {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    # {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    # {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Configuración de archivos estáticos y media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Configuración de archivos media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configurar storage local
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Configuración específica para campos de fecha
USE_TZ = True
TIME_ZONE = 'UTC'

# Configuración para evitar problemas con campos de fecha
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'
SHORT_DATE_FORMAT = '%m/%d/%Y'
SHORT_DATETIME_FORMAT = '%m/%d/%Y %H:%M'

# Configuración de logging para debugging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
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
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración CORS para desarrollo y producción
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = ['*']
CORS_ALLOW_CREDENTIALS = True

# Orígenes permitidos para CORS (para casos específicos)
# Como CORS_ALLOW_ALL_ORIGINS = True, esto se usa solo como referencia
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # React por defecto
    "http://127.0.0.1:3000",
    "http://localhost:8080",    # Vue por defecto
    "http://127.0.0.1:8080",
    "http://localhost:5173",    # Vite por defecto
    "http://127.0.0.1:5173",
    "https://tienda-backend-qsre.onrender.com",  # Render backend
    "https://sobrio-estilo-tienda-main.vercel.app",  # Frontend en Vercel
]

# Configuración específica para subidas de archivos
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Headers permitidos para subidas de archivos
CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'cache-control',
    'content-disposition',  # Para subidas de archivos
    'content-length',       # Para subidas de archivos
]

# Métodos HTTP permitidos por CORS
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Headers permitidos por CORS
CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'cache-control',
]

# Si usas WhiteNoise para servir archivos estáticos/media en producción:
WHITENOISE_ALLOW_ALL_ORIGINS = True

# Configuración REST Framework para desarrollo
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Habilitado para desarrollo
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Límites aumentados para desarrollo
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024  # 50MB

# Configuraciones de seguridad deshabilitadas para desarrollo
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SECURE_BROWSER_XSS_FILTER = False
X_FRAME_OPTIONS = 'ALLOW'

# URL del frontend para desarrollo local
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

# Configuración de Cloudinary para almacenamiento de imágenes
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Configuración de Cloudinary
CLOUDINARY = {
    'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME', 'your-cloud-name'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY', 'your-api-key'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET', 'your-api-secret'),
}

# Configurar Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY['cloud_name'],
    api_key=CLOUDINARY['api_key'],
    api_secret=CLOUDINARY['api_secret']
)

# Configuración de almacenamiento para producción (Render)
if 'RENDER' in os.environ:
    # En producción, usar Cloudinary para archivos media
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
else:
    # En desarrollo, usar almacenamiento local
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'