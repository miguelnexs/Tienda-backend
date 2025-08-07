#!/usr/bin/env python3
"""
Script para probar la importación de CloudinaryStorage
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

print("🧪 PROBANDO IMPORTACIÓN DE CLOUDINARYSTORAGE")
print("=" * 50)

try:
    from Backend.cloudinary_storage import CloudinaryStorage
    print("✅ CloudinaryStorage importado correctamente")
    
    # Crear instancia
    storage = CloudinaryStorage()
    print("✅ CloudinaryStorage instanciado correctamente")
    
    # Probar una subida
    from django.core.files.base import ContentFile
    test_content = ContentFile(b"test content")
    test_name = "test_import.txt"
    
    saved_name = storage.save(test_name, test_content)
    print(f"✅ Subida exitosa: {saved_name}")
    
    url = storage.url(saved_name)
    print(f"🔗 URL: {url}")
    
    exists = storage.exists(saved_name)
    print(f"🔍 Existe: {exists}")
    
    # Limpiar
    storage.delete(saved_name)
    print("✅ Archivo eliminado")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 