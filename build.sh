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

# Initialize database for Render
echo "🗄️  Inicializando base de datos..."
python init_render.py

echo "✅ Build completado exitosamente!" 