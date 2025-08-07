#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración de ImageKit.io
Ejecutar con: python test_imagekit.py
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

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
import io

def print_header(title):
    """Imprimir encabezado formateado"""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")

def test_imagekit_config():
    """Probar configuración de ImageKit"""
    print_header("CONFIGURACIÓN DE IMAGEKIT")
    
    # Verificar variables de entorno
    required_vars = [
        'IMAGEKIT_PUBLIC_KEY',
        'IMAGEKIT_PRIVATE_KEY', 
        'IMAGEKIT_URL_ENDPOINT'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value[:10] if var != 'IMAGEKIT_URL_ENDPOINT' else value}...")
        else:
            print(f"❌ {var}: NO ENCONTRADA")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ FALTAN VARIABLES DE ENTORNO: {', '.join(missing_vars)}")
        return False
    
    return True

def test_imagekit_connection():
    """Probar conexión a ImageKit"""
    print_header("CONEXIÓN A IMAGEKIT")
    
    try:
        from imagekitio import ImageKit
        
        # Configurar ImageKit
        public_key = os.environ.get('IMAGEKIT_PUBLIC_KEY')
        private_key = os.environ.get('IMAGEKIT_PRIVATE_KEY')
        url_endpoint = os.environ.get('IMAGEKIT_URL_ENDPOINT')
        
        imagekit = ImageKit(
            private_key=private_key,
            public_key=public_key,
            url_endpoint=url_endpoint
        )
        
        # Probar conexión obteniendo información de la cuenta
        result = imagekit.list_files()
        print("✅ Conexión exitosa a ImageKit")
        print(f"📊 Archivos en la cuenta: {len(result.list)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error conectando a ImageKit: {e}")
        return False

def test_imagekit_upload():
    """Probar subida de archivo a ImageKit"""
    print_header("PRUEBA DE SUBIDA A IMAGEKIT")
    
    try:
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 200), color='#4A90E2')
        draw = ImageDraw.Draw(img)
        
        # Agregar texto
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 80), "IMAGEKIT TEST", fill='white')
        draw.text((50, 110), "UPLOAD SUCCESSFUL", fill='white')
        
        # Convertir a bytes
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Crear archivo de prueba
        test_content = ContentFile(img_buffer.getvalue())
        test_content.name = 'test_imagekit_upload.png'
        
        # Subir usando el storage
        file_path = default_storage.save('test_imagekit_upload.png', test_content)
        print(f"✅ Archivo subido: {file_path}")
        
        # Obtener URL
        file_url = default_storage.url(file_path)
        print(f"🔗 URL del archivo: {file_url}")
        
        # Verificar que existe
        if default_storage.exists(file_path):
            print("✅ Archivo existe en ImageKit")
        else:
            print("❌ Archivo no encontrado en ImageKit")
        
        # Limpiar archivo de prueba
        default_storage.delete(file_path)
        print("🗑️ Archivo de prueba eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de subida: {e}")
        return False

def test_storage_config():
    """Verificar configuración del storage"""
    print_header("CONFIGURACIÓN DEL STORAGE")
    
    # Verificar tipo de storage
    storage_type = type(default_storage).__name__
    print(f"📦 Storage actual: {storage_type}")
    
    if 'ImageKitStorage' in storage_type:
        print("✅ Usando ImageKitStorage")
    else:
        print("❌ No usando ImageKitStorage")
        return False
    
    return True

def main():
    """Función principal"""
    print("🚀 PRUEBA DE IMAGEKIT.IO")
    print("="*50)
    
    tests = [
        ("Configuración", test_imagekit_config),
        ("Conexión", test_imagekit_connection),
        ("Storage", test_storage_config),
        ("Subida", test_imagekit_upload),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASÓ")
            else:
                print(f"❌ {test_name}: FALLÓ")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n📊 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! ImageKit.io está funcionando correctamente.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración.")

if __name__ == "__main__":
    main() 