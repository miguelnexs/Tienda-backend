"""
Configuración que fuerza el uso del storage correcto
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

django.setup()

from django.core.files.storage import default_storage
from Backend.cloudinary_storage_fixed_urls import CloudinaryStorageFixedURLs

# Forzar el uso del storage correcto
print("🔧 FORZANDO STORAGE CORRECTO...")

# Crear instancia del storage correcto
cloudinary_storage = CloudinaryStorageFixedURLs()

# Reemplazar el default_storage
import django.core.files.storage
django.core.files.storage.default_storage = cloudinary_storage

print("✅ Storage forzado correctamente")
print(f"📁 Storage actual: {type(django.core.files.storage.default_storage).__name__}")

# Verificar que funciona
try:
    test_result = cloudinary_storage.exists("test_file")
    print("✅ Storage verificado correctamente")
except Exception as e:
    print(f"❌ Error verificando storage: {e}") 