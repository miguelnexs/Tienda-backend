#!/usr/bin/env python3
"""
Script para verificar Cloudinary en producción
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()

def check_production_config():
    """Verificar configuración de producción"""
    print("🚀 VERIFICANDO CONFIGURACIÓN DE PRODUCCIÓN")
    print("=" * 50)
    
    from django.conf import settings
    
    # Verificar variables de entorno
    print("📋 Variables de entorno:")
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
    api_key = os.environ.get('CLOUDINARY_API_KEY')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
    
    print(f"  CLOUDINARY_CLOUD_NAME: {cloud_name}")
    print(f"  CLOUDINARY_API_KEY: {api_key[:10] if api_key else 'No configurado'}...")
    print(f"  CLOUDINARY_API_SECRET: {api_secret[:10] if api_secret else 'No configurado'}...")
    
    # Verificar configuración de Django
    print(f"\n⚙️ Configuración de Django:")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"  MEDIA_URL: {settings.MEDIA_URL}")
    
    # Verificar si estamos en producción
    is_production = 'RENDER' in os.environ
    print(f"  Entorno: {'Producción (Render)' if is_production else 'Desarrollo'}")
    
    return True

def test_production_cloudinary():
    """Probar Cloudinary en producción"""
    print("\n☁️ PROBANDO CLOUDINARY EN PRODUCCIÓN")
    print("=" * 50)
    
    try:
        import cloudinary
        import cloudinary.uploader
        
        # Configurar Cloudinary
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET')
        )
        
        # Probar conexión
        result = cloudinary.api.ping()
        print(f"✅ Conexión exitosa: {result.get('status', 'OK')}")
        
        # Probar subida simple
        from PIL import Image
        import io
        
        # Crear imagen de prueba
        img = Image.new('RGB', (100, 100), color='blue')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Subir imagen
        result = cloudinary.uploader.upload(
            buffer,
            public_id='test_production_upload',
            overwrite=True
        )
        
        print(f"✅ Subida exitosa")
        print(f"  Public ID: {result['public_id']}")
        print(f"  URL: {result['secure_url']}")
        
        # Eliminar imagen de prueba
        delete_result = cloudinary.uploader.destroy('test_production_upload')
        if delete_result.get('result') == 'ok':
            print("✅ Imagen de prueba eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_storage_configuration():
    """Verificar configuración del storage"""
    print("\n🔧 VERIFICANDO CONFIGURACIÓN DEL STORAGE")
    print("=" * 50)
    
    try:
        from django.conf import settings
        from django.core.files.storage import default_storage
        
        print(f"Storage actual: {type(default_storage).__name__}")
        print(f"Clase configurada: {settings.DEFAULT_FILE_STORAGE}")
        
        # Verificar si es CloudinaryStorage
        if 'CloudinaryStorage' in str(type(default_storage)):
            print("✅ Usando CloudinaryStorage")
        else:
            print("⚠️ No usando CloudinaryStorage")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 VERIFICACIÓN DE PRODUCCIÓN - CLOUDINARY")
    print("=" * 60)
    
    tests = [
        ("Configuración", check_production_config),
        ("Cloudinary", test_production_cloudinary),
        ("Storage", check_storage_configuration),
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
    print("\n📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 RESULTADO: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("🎉 ¡CLOUDINARY ESTÁ CONFIGURADO CORRECTAMENTE EN PRODUCCIÓN!")
    else:
        print("⚠️ Algunas verificaciones fallaron. Revisa la configuración.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 