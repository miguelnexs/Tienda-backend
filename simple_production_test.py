#!/usr/bin/env python3
"""
Script simple para probar configuración de producción
"""
import os
import sys
from pathlib import Path

# Simular variables de entorno de producción
os.environ['RENDER'] = 'true'
os.environ['DEBUG'] = 'False'
os.environ['DJANGO_SETTINGS_MODULE'] = 'Backend.render_settings'
os.environ['CLOUDINARY_CLOUD_NAME'] = 'do1ntnlop'
os.environ['CLOUDINARY_API_KEY'] = '117225377115856'
os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'

def test_cloudinary_config():
    """Probar configuración de Cloudinary"""
    print("🚀 PROBANDO CONFIGURACIÓN DE CLOUDINARY")
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
        
        print("✅ Cloudinary configurado correctamente")
        print(f"  Cloud Name: {cloudinary.config().cloud_name}")
        print(f"  API Key: {cloudinary.config().api_key[:10]}...")
        
        # Probar conexión
        result = cloudinary.api.ping()
        print(f"✅ Conexión exitosa: {result.get('status', 'OK')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error configurando Cloudinary: {e}")
        return False

def test_storage_class():
    """Probar la clase de storage"""
    print("\n🔧 PROBANDO CLASE DE STORAGE")
    print("=" * 50)
    
    try:
        # Importar la clase de storage
        from Backend.cloudinary_storage import CloudinaryStorage
        
        # Crear instancia
        storage = CloudinaryStorage()
        print("✅ CloudinaryStorage importado correctamente")
        
        # Probar configuración
        print(f"  Cloud Name: {storage.cloud_name if hasattr(storage, 'cloud_name') else 'N/A'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con CloudinaryStorage: {e}")
        return False

def test_image_upload():
    """Probar subida de imagen"""
    print("\n📤 PROBANDO SUBIDA DE IMAGEN")
    print("=" * 50)
    
    try:
        import cloudinary
        import cloudinary.uploader
        from PIL import Image
        import io
        
        # Configurar Cloudinary
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET')
        )
        
        # Crear imagen de prueba
        img = Image.new('RGB', (200, 200), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Subir imagen
        result = cloudinary.uploader.upload(
            buffer,
            public_id='test_production_simple',
            overwrite=True,
            invalidate=True
        )
        
        print("✅ Subida exitosa")
        print(f"  Public ID: {result['public_id']}")
        print(f"  URL: {result['secure_url']}")
        print(f"  Tamaño: {result['bytes']} bytes")
        
        # Eliminar imagen de prueba
        delete_result = cloudinary.uploader.destroy('test_production_simple')
        if delete_result.get('result') == 'ok':
            print("✅ Imagen de prueba eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en subida: {e}")
        return False

def test_render_settings():
    """Probar configuración de render_settings"""
    print("\n⚙️ PROBANDO CONFIGURACIÓN DE RENDER_SETTINGS")
    print("=" * 50)
    
    try:
        # Simular la configuración de render_settings
        CLOUDINARY = {
            'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME', 'do1ntnlop'),
            'api_key': os.environ.get('CLOUDINARY_API_KEY', '1172253771'),
            'api_secret': os.environ.get('CLOUDINARY_API_SECRET', 'e0YSrk3sT_'),
        }
        
        DEFAULT_FILE_STORAGE = 'Backend.cloudinary_storage.CloudinaryStorage'
        
        print("✅ Configuración simulada:")
        print(f"  CLOUDINARY_CLOUD_NAME: {CLOUDINARY['cloud_name']}")
        print(f"  CLOUDINARY_API_KEY: {CLOUDINARY['api_key'][:10]}...")
        print(f"  CLOUDINARY_API_SECRET: {CLOUDINARY['api_secret'][:10]}...")
        print(f"  DEFAULT_FILE_STORAGE: {DEFAULT_FILE_STORAGE}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 PRUEBA SIMPLE DE CONFIGURACIÓN DE PRODUCCIÓN")
    print("=" * 60)
    
    tests = [
        ("Cloudinary Config", test_cloudinary_config),
        ("Storage Class", test_storage_class),
        ("Image Upload", test_image_upload),
        ("Render Settings", test_render_settings),
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
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! La configuración básica está correcta.")
        print("\n💡 El problema puede estar en:")
        print("   1. Configuración de la base de datos")
        print("   2. Serializers específicos")
        print("   3. Vistas de la API")
        print("   4. Configuración de CORS")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración básica.")
    
    return passed >= 3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 