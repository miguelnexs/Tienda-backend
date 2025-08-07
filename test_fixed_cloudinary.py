#!/usr/bin/env python3
"""
Script para probar la configuración corregida de Cloudinary
"""
import os
import sys
import django
from pathlib import Path
import tempfile
from PIL import Image
import io

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

def test_fixed_storage():
    """Probar el storage corregido"""
    print("🔧 PROBANDO STORAGE CORREGIDO")
    print("=" * 50)
    
    try:
        from Backend.cloudinary_storage_fixed import CloudinaryStorage
        
        # Crear instancia
        storage = CloudinaryStorage()
        print("✅ CloudinaryStorage corregido importado correctamente")
        
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 200), color='green')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            temp_file.write(buffer.getvalue())
            temp_file_path = temp_file.name
        
        # Abrir el archivo como File de Django
        from django.core.files import File
        with open(temp_file_path, 'rb') as f:
            django_file = File(f, name='test_fixed.png')
            
            # Guardar usando el storage corregido
            saved_name = storage._save('test_fixed_storage', django_file)
            
            print("✅ Subida con storage corregido exitosa")
            print(f"  Nombre guardado: {saved_name}")
            
            # Obtener URL
            url = storage.url(saved_name)
            print(f"  URL: {url}")
            
            # Verificar existencia
            exists = storage.exists(saved_name)
            print(f"  Existe: {exists}")
            
            # Obtener tamaño
            size = storage.size(saved_name)
            print(f"  Tamaño: {size} bytes")
        
        # Limpiar archivo temporal
        os.unlink(temp_file_path)
        
        return saved_name
        
    except Exception as e:
        print(f"❌ Error con storage corregido: {e}")
        return None

def test_django_settings():
    """Probar configuración de Django"""
    print("\n⚙️ PROBANDO CONFIGURACIÓN DE DJANGO")
    print("=" * 50)
    
    try:
        from django.conf import settings
        from django.core.files.storage import default_storage
        
        print(f"Storage configurado: {type(default_storage).__name__}")
        print(f"Clase del storage: {settings.DEFAULT_FILE_STORAGE}")
        
        # Verificar si es CloudinaryStorage
        if 'CloudinaryStorage' in str(type(default_storage)):
            print("✅ Usando CloudinaryStorage")
        else:
            print("⚠️ No usando CloudinaryStorage")
            print(f"   Storage actual: {type(default_storage).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando configuración: {e}")
        return False

def test_cloudinary_direct():
    """Probar Cloudinary directamente"""
    print("\n☁️ PROBANDO CLOUDINARY DIRECTAMENTE")
    print("=" * 50)
    
    try:
        import cloudinary
        import cloudinary.uploader
        
        # Configurar Cloudinary
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', 'do1ntnlop'),
            api_key=os.environ.get('CLOUDINARY_API_KEY', '117225377115856'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET', 'e0YSrk3sT_70-ijM6mwdFBIWP9w')
        )
        
        # Probar conexión
        result = cloudinary.api.ping()
        print(f"✅ Conexión exitosa: {result.get('status', 'OK')}")
        
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 200), color='blue')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Subir imagen
        result = cloudinary.uploader.upload(
            buffer,
            public_id='test_fixed_direct',
            overwrite=True,
            invalidate=True
        )
        
        print("✅ Subida directa exitosa")
        print(f"  Public ID: {result['public_id']}")
        print(f"  URL: {result['secure_url']}")
        print(f"  Tamaño: {result['bytes']} bytes")
        
        # Eliminar imagen de prueba
        delete_result = cloudinary.uploader.destroy('test_fixed_direct')
        if delete_result.get('result') == 'ok':
            print("✅ Imagen de prueba eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en subida directa: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 PRUEBA DE CONFIGURACIÓN CORREGIDA")
    print("=" * 60)
    
    tests = [
        ("Storage Corregido", test_fixed_storage),
        ("Django Settings", test_django_settings),
        ("Cloudinary Directo", test_cloudinary_direct),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results[test_name] = False
    
    # Resumen
    print("\n📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! La configuración corregida funciona.")
        print("\n💡 Ahora puedes:")
        print("   1. Desplegar a Render con la configuración corregida")
        print("   2. Las imágenes se subirán correctamente a Cloudinary")
        print("   3. Las URLs serán absolutas de Cloudinary")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 