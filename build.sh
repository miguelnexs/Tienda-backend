#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Iniciando build del proyecto..."

# Upgrade pip
echo "📦 Actualizando pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Check for potential issues
echo "🔍 Verificando configuración..."
python check_deployment.py

# Fix database migrations for Render
echo "🚀 Arreglando migraciones de base de datos..."
python fix_db_migrations.py

# Test Cloudinary configuration
echo "☁️ Probando configuración de Cloudinary..."
python check_cloudinary_production.py

echo "✅ Build completado exitosamente!" 