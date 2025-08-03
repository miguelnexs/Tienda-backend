#!/usr/bin/env python
"""
Script para verificar el timing de la configuración de Cloudinary
"""

import os
import sys
import django
from pathlib import Path

# Configurar variables de entorno ANTES de importar Django
os.environ['CLOUDINARY_CLOUD_NAME'] = 'do1ntnlop'
os.environ['CLOUDINARY_API_KEY'] = '117225377115856'
os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')

def test_timing():
    """Probar el timing de la configuración"""
    print("⏰ Verificando timing de configuración...")
    
    # Verificar variables antes de Django
    print(f"📋 Variables antes de Django:")
    print(f"   CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME')}")
    print(f"   CLOUDINARY_API_KEY: {os.environ.get('CLOUDINARY_API_KEY')}")
    print(f"   CLOUDINARY_API_SECRET: {os.environ.get('CLOUDINARY_API_SECRET')[:10]}...")
    
    # Cargar Django
    django.setup()
    
    from django.conf import settings
    from django.core.files.storage import default_storage
    
    print(f"\n🔧 Configuración después de Django:")
    print(f"   DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    print(f"   default_storage: {default_storage}")
    print(f"   default_storage.__class__: {default_storage.__class__}")
    
    # Verificar si la condición se evaluó correctamente
    condition = 'RENDER' in os.environ or os.environ.get('CLOUDINARY_CLOUD_NAME')
    print(f"\n🔍 Condición de configuración:")
    print(f"   'RENDER' in os.environ: {'RENDER' in os.environ}")
    print(f"   os.environ.get('CLOUDINARY_CLOUD_NAME'): {os.environ.get('CLOUDINARY_CLOUD_NAME')}")
    print(f"   Condición resultante: {condition}")
    
    # Verificar si CLOUDINARY está en settings
    if hasattr(settings, 'CLOUDINARY'):
        print(f"\n✅ CLOUDINARY configurado en settings:")
        print(f"   {settings.CLOUDINARY}")
    else:
        print(f"\n❌ CLOUDINARY no configurado en settings")

def test_force_cloudinary():
    """Forzar Cloudinary manualmente"""
    print("\n🔧 Forzando Cloudinary manualmente...")
    
    from cloudinary_storage.storage import MediaCloudinaryStorage
    from django.core.files.base import ContentFile
    
    # Crear instancia manual
    cloudinary_storage = MediaCloudinaryStorage()
    print(f"✅ Cloudinary storage creado: {cloudinary_storage}")
    
    # Probar subida
    test_content = b"test content"
    test_file = ContentFile(test_content)
    
    try:
        file_path = cloudinary_storage.save('test_manual.txt', test_file)
        print(f"✅ Archivo subido manualmente: {file_path}")
        
        file_url = cloudinary_storage.url(file_path)
        print(f"🌐 URL del archivo: {file_url}")
        
        if 'cloudinary.com' in file_url:
            print("✅ ¡URL de Cloudinary detectada!")
        else:
            print("⚠️  URL local detectada")
            
        # Limpiar
        cloudinary_storage.delete(file_path)
        print("🗑️  Archivo eliminado")
        
    except Exception as e:
        print(f"❌ Error en subida manual: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_timing()
    test_force_cloudinary() 