#!/usr/bin/env python
"""
Script para verificar la importación de Cloudinary
"""

import os
import sys
import django
from pathlib import Path

# Forzar variables de entorno de Cloudinary
os.environ['CLOUDINARY_CLOUD_NAME'] = 'do1ntnlop'
os.environ['CLOUDINARY_API_KEY'] = '117225377115856'
os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

def test_cloudinary_import():
    """Probar la importación de Cloudinary"""
    print("🔍 Verificando importación de Cloudinary...")
    
    try:
        # Probar importación directa
        from cloudinary_storage.storage import MediaCloudinaryStorage
        print("✅ MediaCloudinaryStorage importado correctamente")
        
        # Crear instancia
        storage = MediaCloudinaryStorage()
        print(f"✅ Instancia creada: {storage}")
        print(f"✅ Clase: {storage.__class__}")
        
        return storage
        
    except Exception as e:
        print(f"❌ Error importando MediaCloudinaryStorage: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_storage_config():
    """Probar configuración de storage"""
    print("\n🔧 Verificando configuración de storage...")
    
    from django.conf import settings
    from django.core.files.storage import default_storage
    
    print(f"📋 DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    print(f"📋 default_storage: {default_storage}")
    print(f"📋 default_storage.__class__: {default_storage.__class__}")
    
    # Intentar importar la clase configurada
    try:
        storage_class_path = getattr(settings, 'DEFAULT_FILE_STORAGE', None)
        if storage_class_path:
            module_path, class_name = storage_class_path.rsplit('.', 1)
            module = __import__(module_path, fromlist=[class_name])
            storage_class = getattr(module, class_name)
            print(f"✅ Clase importada: {storage_class}")
            
            # Crear instancia
            storage_instance = storage_class()
            print(f"✅ Instancia creada: {storage_instance}")
            
        else:
            print("❌ DEFAULT_FILE_STORAGE no configurado")
            
    except Exception as e:
        print(f"❌ Error importando clase de storage: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    storage = test_cloudinary_import()
    test_storage_config() 