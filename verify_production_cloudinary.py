#!/usr/bin/env python3
"""
Verificación rápida de Cloudinary en producción
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings

def main():
    print("🔍 VERIFICACIÓN RÁPIDA DE CLOUDINARY EN PRODUCCIÓN")
    print("=" * 60)
    
    # 1. Verificar variables de entorno
    print("\n📋 Variables de Entorno:")
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
    api_key = os.environ.get('CLOUDINARY_API_KEY')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
    
    print(f"CLOUDINARY_CLOUD_NAME: {'✅' if cloud_name else '❌'} {cloud_name or 'NO ENCONTRADA'}")
    print(f"CLOUDINARY_API_KEY: {'✅' if api_key else '❌'} {api_key[:10] + '...' if api_key else 'NO ENCONTRADA'}")
    print(f"CLOUDINARY_API_SECRET: {'✅' if api_secret else '❌'} {api_secret[:10] + '...' if api_secret else 'NO ENCONTRADA'}")
    print(f"RENDER: {'✅' if os.environ.get('RENDER') else '❌'} {os.environ.get('RENDER', 'NO ENCONTRADA')}")
    
    if not all([cloud_name, api_key, api_secret]):
        print("\n❌ FALTAN VARIABLES DE ENTORNO DE CLOUDINARY")
        return False
    
    # 2. Configurar Cloudinary
    try:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        print("\n✅ Cloudinary configurado correctamente")
    except Exception as e:
        print(f"\n❌ Error configurando Cloudinary: {e}")
        return False
    
    # 3. Probar conexión
    try:
        result = cloudinary.api.ping()
        print("✅ Conexión exitosa a Cloudinary")
        print(f"Status: {result.get('status', 'OK')}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 4. Verificar configuración de Django
    print(f"\n⚙️ Configuración Django:")
    print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'No configurado')}")
    print(f"DEBUG: {getattr(settings, 'DEBUG', 'No configurado')}")
    
    # 5. Probar subida simple
    try:
        from PIL import Image
        import io
        
        # Crear imagen de prueba
        img = Image.new('RGB', (100, 100), color='green')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Subir imagen
        result = cloudinary.uploader.upload(
            buffer,
            public_id='quick_test_production',
            overwrite=True
        )
        
        print("✅ Subida de prueba exitosa")
        print(f"URL: {result['secure_url']}")
        
        # Limpiar archivo de prueba
        cloudinary.uploader.destroy('quick_test_production')
        print("✅ Archivo de prueba eliminado")
        
    except Exception as e:
        print(f"❌ Error en subida de prueba: {e}")
        return False
    
    print("\n🎉 ¡VERIFICACIÓN COMPLETADA! Cloudinary está funcionando correctamente.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 