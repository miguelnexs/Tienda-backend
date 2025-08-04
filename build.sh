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

# Final deployment for Render
echo "🚀 Iniciando despliegue final..."
python final_deploy.py

echo "✅ Build completado exitosamente!" 