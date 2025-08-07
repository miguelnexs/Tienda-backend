#!/usr/bin/env python3
"""
Script de prueba directa del ImageKitStorage
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

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
import io

def test_direct_imagekit():
    """Probar ImageKitStorage directamente"""
    print("🚀 PRUEBA DIRECTA DE IMAGEKIT STORAGE")
    print("="*50)
    
    try:
        # Importar ImageKitStorage directamente
        from Backend.imagekit_storage import ImageKitStorage
        
        # Crear instancia
        storage = ImageKitStorage()
        print("✅ ImageKitStorage creado correctamente")
        
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 200), color='#4A90E2')
        draw = ImageDraw.Draw(img)
        
        # Agregar texto
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 80), "IMAGEKIT TEST", fill='white')
        draw.text((50, 110), "DIRECT UPLOAD", fill='white')
        
        # Convertir a bytes
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Crear archivo de prueba
        test_content = ContentFile(img_buffer.getvalue())
        test_content.name = 'test_direct_imagekit.png'
        
        # Subir usando el storage
        file_path = storage.save('test_direct_imagekit.png', test_content)
        print(f"✅ Archivo subido: {file_path}")
        
        # Obtener URL
        file_url = storage.url(file_path)
        print(f"🔗 URL del archivo: {file_url}")
        
        # Verificar que existe
        if storage.exists(file_path):
            print("✅ Archivo existe en ImageKit")
        else:
            print("❌ Archivo no encontrado en ImageKit")
        
        # Limpiar archivo de prueba
        storage.delete(file_path)
        print("🗑️ Archivo de prueba eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba directa: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_direct_imagekit()
    if success:
        print("\n🎉 ¡PRUEBA DIRECTA EXITOSA!")
    else:
        print("\n❌ PRUEBA DIRECTA FALLÓ") 