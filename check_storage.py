#!/usr/bin/env python3
"""
Script para verificar qué storage está siendo usado
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.core.files.storage import default_storage
from django.conf import settings

print("🔍 VERIFICANDO CONFIGURACIÓN DE STORAGE")
print("=" * 50)

print(f"📁 DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
print(f"📁 Storage actual: {default_storage.__class__.__name__}")
print(f"📁 Módulo del storage: {default_storage.__class__.__module__}")

# Verificar si es nuestro storage personalizado
if 'CloudinaryStorage' in str(default_storage.__class__):
    print("✅ Usando CloudinaryStorage personalizado")
else:
    print("❌ No está usando CloudinaryStorage")

# Probar una subida simple
from django.core.files.base import ContentFile
test_content = ContentFile(b"test content")
test_name = "test_storage_check.txt"

try:
    saved_name = default_storage.save(test_name, test_content)
    print(f"✅ Subida exitosa: {saved_name}")
    
    url = default_storage.url(saved_name)
    print(f"🔗 URL: {url}")
    
    exists = default_storage.exists(saved_name)
    print(f"🔍 Existe: {exists}")
    
    # Limpiar
    default_storage.delete(saved_name)
    print("✅ Archivo eliminado")
    
except Exception as e:
    print(f"❌ Error en subida: {e}") 