"""
Configuración específica para Render
"""
import os
import dj_database_url
import psycopg2.extensions
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'tienda-backend-qsre.onrender.com',
    'tienda-backend-api.onrender.com',
    'localhost',
    '127.0.0.1',
]

# Application definition - CRITICAL: Orden específico requerido
INSTALLED_APPS = [
    # Django apps - DEBEN IR PRIMERO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',  # CRÍTICO: Debe estar antes de las apps que lo usan
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap5',
    'colorfield',
    'django_filters',
    'rest_framework_simplejwt',
    'nested_admin',
    'whitenoise.runserver_nostatic',  # Para servir archivos estáticos
    
    # Local apps - DEBEN IR AL FINAL
    'productos.apps.ProductosConfig',
    'categorias.apps.CategoriasConfig',  # Usar la configuración completa
    'ventas.apps.VentasConfig',  # Usar la configuración completa
    'pedidos.apps.PedidosConfig',  # Usar la configuración completa
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Backend.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Configuración de Cloudinary
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', 'do1ntnlop')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', '117225377115856')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', 'e0YSrk3sT_70-ijM6mwdFBIWP9w')

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# Configuración de archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuración de archivos media
MEDIA_URL = 'https://res.cloudinary.com/do1ntnlop/image/upload/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de storage - FORZAR AGRESIVAMENTE
DEFAULT_FILE_STORAGE = 'Backend.cloudinary_storage_fixed_urls.CloudinaryStorageFixedURLs'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Forzar el storage correcto
from Backend.cloudinary_storage_fixed_urls import CloudinaryStorageFixedURLs
from django.core.files.storage import default_storage
import django.core.files.storage

print("🔧 FORZANDO STORAGE CORRECTO...")
cloudinary_storage = CloudinaryStorageFixedURLs()
django.core.files.storage.default_storage = cloudinary_storage

# Configuración de CORS
CORS_ALLOWED_ORIGINS = [
    "https://sobrio-estilo-tienda-main.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://tienda-backend-qsre.onrender.com",
    "https://tienda-backend-api.onrender.com",
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Configuración de REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Configuración de JWT
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# Configuración de idioma y zona horaria
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Configuración de validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuración de archivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Forzar el uso de Cloudinary
os.environ['DJANGO_CLOUDINARY_STORAGE'] = 'true'

# DEBUG: Verificar configuración
print("🚀 RENDER_SETTINGS.PY CARGADO - CONFIGURACIÓN DE PRODUCCIÓN ACTIVA")
print("☁️ CLOUDINARY CONFIGURADO PARA PRODUCCIÓN:")
print(f"  Cloud Name: {CLOUDINARY_CLOUD_NAME}")
print(f"  API Key: {CLOUDINARY_API_KEY[:10]}...")
print(f"  DEFAULT_FILE_STORAGE: {DEFAULT_FILE_STORAGE}")
print(f"  Storage forzado: {type(django.core.files.storage.default_storage).__name__}")
print("✅ CONFIGURACIÓN DE PRODUCCIÓN COMPLETADA")
print("🚀 SISTEMA LISTO PARA RENDER") 