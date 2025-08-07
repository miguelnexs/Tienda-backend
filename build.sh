#!/usr/bin/env bash
# exit on error
set -o errexit

# Mostrar comandos mientras se ejecutan
set -x

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Crear directorios necesarios
mkdir -p staticfiles media

# Forzar configuración de producción
export DJANGO_SETTINGS_MODULE=Backend.render_settings
export DJANGO_CLOUDINARY_STORAGE=true
export CLOUDINARY_CLOUD_NAME=do1ntnlop
export CLOUDINARY_API_KEY=117225377115856
export CLOUDINARY_API_SECRET=e0YSrk3sT_70-ijM6mwdFBIWP9w

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
python manage.py makemigrations
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

# Verificar configuración
echo "✅ Build completado exitosamente!" 