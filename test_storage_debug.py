#!/usr/bin/env python3
"""
Script de debug para verificar la configuración del storage
"""

import os
import sys
import django
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage

def main():
    print("🔍 DEBUG DE CONFIGURACIÓN DE STORAGE")
    print("="*50)
    
    # Verificar configuración en settings
    print(f"1. DEFAULT_FILE_STORAGE en settings: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    
    # Verificar tipo de storage actual
    print(f"2. Tipo de default_storage: {type(default_storage).__name__}")
    
    # Verificar si es ImageKitStorage
    if 'ImageKitStorage' in str(type(default_storage)):
        print("✅ Usando ImageKitStorage")
    else:
        print("❌ No usando ImageKitStorage")
    
    # Intentar importar ImageKitStorage manualmente
    try:
        from Backend.imagekit_storage import ImageKitStorage
        print("✅ ImageKitStorage se puede importar")
        
        # Crear instancia manual
        manual_storage = ImageKitStorage()
        print("✅ ImageKitStorage se puede instanciar")
        
    except Exception as e:
        print(f"❌ Error con ImageKitStorage: {e}")
    
    # Verificar variables de entorno
    print(f"\n3. Variables de entorno:")
    print(f"   IMAGEKIT_PUBLIC_KEY: {'✅' if os.environ.get('IMAGEKIT_PUBLIC_KEY') else '❌'}")
    print(f"   IMAGEKIT_PRIVATE_KEY: {'✅' if os.environ.get('IMAGEKIT_PRIVATE_KEY') else '❌'}")
    print(f"   IMAGEKIT_URL_ENDPOINT: {'✅' if os.environ.get('IMAGEKIT_URL_ENDPOINT') else '❌'}")

if __name__ == "__main__":
    main() 