#!/usr/bin/env python3
"""
Script para probar la generación de URLs de Cloudinary
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
    print("✅ Django configurado correctamente")
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

from Backend.cloudinary_storage_fixed_urls import CloudinaryStorageFixedURLs

def test_url_generation():
    """Probar generación de URLs"""
    print("\n🧪 PROBANDO GENERACIÓN DE URLS")
    print("=" * 60)
    
    # Crear instancia del storage
    storage = CloudinaryStorageFixedURLs()
    
    # Lista de nombres de archivo para probar
    test_files = [
        'categorias/D_NQ_NP_846922-MLA49172515582_022022-O.webp',
        'categorias/test_image.jpg',
        'categorias/another_image.png',
        'test_image.webp',
        'D_NQ_NP_846922-MLA49172515582_022022-O.webp'
    ]
    
    print("\n📋 Probando diferentes formatos de nombre:")
    for name in test_files:
        print(f"\n🔍 Probando: {name}")
        url = storage.url(name)
        print(f"🔗 URL generada: {url}")
        
        # Verificar si la URL es accesible
        import requests
        try:
            response = requests.head(url)
            if response.status_code == 200:
                print(f"✅ URL accesible (200 OK)")
            else:
                print(f"⚠️ URL no accesible ({response.status_code})")
        except Exception as e:
            print(f"❌ Error verificando URL: {e}")

def test_file_upload():
    """Probar subida y URL de archivo"""
    print("\n🧪 PROBANDO SUBIDA Y URL")
    print("=" * 60)
    
    storage = CloudinaryStorageFixedURLs()
    
    # Crear un archivo de prueba
    from django.core.files.base import ContentFile
    content = ContentFile(b"test content", name="test_file.txt")
    
    try:
        # Subir archivo
        path = storage.save("test/test_file.txt", content)
        print(f"✅ Archivo guardado en: {path}")
        
        # Obtener URL
        url = storage.url(path)
        print(f"🔗 URL generada: {url}")
        
        # Verificar URL
        import requests
        response = requests.head(url)
        if response.status_code == 200:
            print(f"✅ URL accesible (200 OK)")
        else:
            print(f"⚠️ URL no accesible ({response.status_code})")
            
    except Exception as e:
        print(f"❌ Error en prueba de subida: {e}")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE URLS DE CLOUDINARY")
    print("=" * 60)
    
    # Ejecutar pruebas
    test_url_generation()
    test_file_upload()
    
    print("\n✅ PRUEBAS COMPLETADAS") 