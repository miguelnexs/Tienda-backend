#!/usr/bin/env python
"""
Script de diagnóstico para identificar por qué las imágenes no se suben a Cloudinary
"""
import os
import sys
import django
import requests
import json
from pathlib import Path
from datetime import datetime

def test_django_storage_configuration():
    """Probar la configuración de Django storage"""
    
    print("🔍 DIAGNÓSTICO DE CONFIGURACIÓN DE DJANGO STORAGE")
    print("="*60)
    
    try:
        # Simular entorno de Render
        os.environ['RENDER'] = 'true'
        os.environ['DJANGO_SETTINGS_MODULE'] = 'Backend.render_settings'
        
        # Configurar DATABASE_URL para pruebas
        if not os.environ.get('DATABASE_URL'):
            os.environ['DATABASE_URL'] = 'postgresql://tienda_user:PWKuO99372EAcsyx5KpHlV9VBIQJkvle@dpg-d278j5u3jp1c73en5gbg-a.ohio-postgres.render.com/tienda_production'
        
        # Configurar Django
        django.setup()
        
        from django.conf import settings
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        
        print("✅ Django configurado correctamente")
        print(f"📋 DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        print(f"📋 STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
        print(f"📋 Storage actual: {default_storage}")
        print(f"📋 Storage class: {type(default_storage)}")
        
        # Verificar configuración de Cloudinary
        if hasattr(settings, 'CLOUDINARY'):
            print(f"☁️ CLOUDINARY configurado: {settings.CLOUDINARY}")
        else:
            print("❌ CLOUDINARY no configurado")
        
        # Probar subida directa a Cloudinary
        print("\n🧪 PROBANDO SUBIDA DIRECTA A CLOUDINARY")
        
        # Crear un archivo de prueba
        test_content = b"Test file content for Cloudinary upload"
        test_file = ContentFile(test_content, name="test_upload.txt")
        
        # Intentar guardar usando el storage configurado
        try:
            saved_path = default_storage.save('test/test_upload.txt', test_file)
            print(f"✅ Archivo guardado en: {saved_path}")
            
            # Verificar URL
            url = default_storage.url(saved_path)
            print(f"🔗 URL del archivo: {url}")
            
            if 'cloudinary.com' in url:
                print("☁️ ¡EXCELENTE! El archivo se subió a Cloudinary")
                return True
            else:
                print("📁 El archivo se guardó localmente")
                return False
                
        except Exception as e:
            print(f"❌ Error al guardar archivo: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_serializer_upload():
    """Probar subida a través del serializer"""
    
    print("\n🧪 PROBANDO SUBIDA A TRAVÉS DEL SERIALIZER")
    print("="*60)
    
    try:
        from categorias.models import CategoriaProducto
        from categorias.serializers import CategoriaProductoSerializer
        from django.core.files.base import ContentFile
        
        # Crear una categoría de prueba
        categoria = CategoriaProducto.objects.create(
            nombre=f"Test Cloudinary {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            descripcion="Prueba de subida a Cloudinary",
            activa=True,
            orden=999
        )
        
        # Crear un archivo de prueba
        test_content = b"Test image content for Cloudinary upload"
        test_file = ContentFile(test_content, name="test_image.jpg")
        
        # Simular InMemoryUploadedFile
        from django.core.files.uploadedfile import InMemoryUploadedFile
        from io import BytesIO
        
        file_obj = InMemoryUploadedFile(
            file=BytesIO(test_content),
            field_name='imagen',
            name='test_image.jpg',
            content_type='image/jpeg',
            size=len(test_content),
            charset=None
        )
        
        # Crear serializer y probar _save_imagen
        serializer = CategoriaProductoSerializer()
        serializer._save_imagen(categoria, file_obj)
        
        print(f"✅ Imagen guardada para categoría: {categoria.nombre}")
        print(f"📁 Ruta de la imagen: {categoria.imagen.name}")
        print(f"🔗 URL de la imagen: {categoria.imagen.url}")
        
        if 'cloudinary.com' in categoria.imagen.url:
            print("☁️ ¡EXCELENTE! La imagen se subió a Cloudinary")
            return True
        else:
            print("📁 La imagen se guardó localmente")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de serializer: {e}")
        return False

def test_render_api_upload():
    """Probar subida a través de la API de Render"""
    
    print("\n🌐 PROBANDO SUBIDA A TRAVÉS DE LA API DE RENDER")
    print("="*60)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # Generar nombre único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_categoria = f"Test Debug {timestamp}"
        
        # Buscar imagen de prueba
        imagen_path = Path("D:/usuario/Downloads/bolso/cartera-casual-para-mujer-23064.jpg")
        
        if imagen_path.exists():
            # Preparar datos
            data = {
                'nombre': nombre_categoria,
                'descripcion': f'Prueba de diagnóstico - {timestamp}',
                'activa': True,
                'orden': 998
            }
            
            # Preparar archivo
            files = {
                'imagen': ('cartera-casual-para-mujer-23064.jpg', open(imagen_path, 'rb'), 'image/jpeg')
            }
            
            # Crear categoría
            response = requests.post(
                f"{RENDER_API_URL}/categorias/",
                data=data,
                files=files,
                timeout=30
            )
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 201:
                try:
                    categoria = response.json()
                    print("✅ ¡Categoría creada exitosamente!")
                    print(f"📸 ID: {categoria['id']}")
                    print(f"🏷️ Nombre: {categoria['nombre']}")
                    print(f"🔗 URL de la imagen: {categoria['imagen_url']}")
                    
                    # Verificar configuración
                    if 'cloudinary.com' in categoria['imagen_url']:
                        print("☁️ ¡EXCELENTE! La imagen se subió a Cloudinary")
                        return True
                    else:
                        print("📁 La imagen se guardó localmente")
                        return False
                        
                except json.JSONDecodeError as e:
                    print(f"❌ Error decodificando respuesta: {e}")
                    print(f"📊 Response Text: {response.text}")
                    return False
            else:
                print(f"❌ Error creando categoría: {response.status_code}")
                print(f"📊 Response: {response.text}")
                return False
        else:
            print("❌ No se encontró la imagen de prueba")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: La petición tardó demasiado")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión durante la petición")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def check_render_logs():
    """Verificar logs de Render para confirmar configuración"""
    
    print("\n📋 VERIFICANDO LOGS DE RENDER")
    print("="*60)
    
    print("📊 Según los logs que proporcionaste:")
    print("✅ Build successful")
    print("✅ Service is live")
    print("✅ Gunicorn started successfully")
    print("✅ All packages installed correctly")
    
    # Buscar mensajes específicos de render_settings.py
    print("\n🔍 BUSCANDO MENSAJES DE RENDER_SETTINGS.PY:")
    print("Los logs deberían mostrar:")
    print("🚀 RENDER_SETTINGS.PY CARGADO - CONFIGURACIÓN DE PRODUCCIÓN ACTIVA")
    print("☁️ CLOUDINARY CONFIGURADO:")
    print("✅ CONFIGURACIÓN DE RENDER APLICADA CORRECTAMENTE")
    
    print("\n💡 Si NO ves estos mensajes, significa que:")
    print("1. DJANGO_SETTINGS_MODULE no está configurado correctamente")
    print("2. El servicio no está usando render_settings.py")
    print("3. Hay un error de importación en render_settings.py")

def main():
    """Función principal de diagnóstico"""
    print("🔍 DIAGNÓSTICO COMPLETO DE CLOUDINARY")
    print("="*60)
    
    # 1. Probar configuración de Django storage
    storage_ok = test_django_storage_configuration()
    
    # 2. Probar subida a través del serializer
    serializer_ok = test_serializer_upload()
    
    # 3. Probar subida a través de la API de Render
    api_ok = test_render_api_upload()
    
    # 4. Verificar logs
    check_render_logs()
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE DIAGNÓSTICO")
    print("="*60)
    print(f"✅ Configuración de storage: {'EXITOSA' if storage_ok else 'FALLIDA'}")
    print(f"✅ Subida por serializer: {'EXITOSA' if serializer_ok else 'FALLIDA'}")
    print(f"✅ Subida por API: {'EXITOSA' if api_ok else 'FALLIDA'}")
    
    print("\n" + "="*60)
    print("🎯 ANÁLISIS DEL PROBLEMA")
    print("="*60)
    
    if storage_ok and serializer_ok and api_ok:
        print("🎉 ¡PERFECTO! Todo está funcionando correctamente")
        print("✅ La configuración local es correcta")
        print("✅ Los serializers funcionan correctamente")
        print("✅ La API funciona correctamente")
    elif storage_ok and serializer_ok:
        print("✅ La configuración local es correcta")
        print("✅ Los serializers funcionan correctamente")
        print("⚠️ Pero la API de Render no está usando la configuración correcta")
        print("🔧 El problema está en que Render no está usando render_settings.py")
    elif storage_ok:
        print("✅ La configuración de storage es correcta")
        print("❌ Pero hay problemas con los serializers")
        print("🔧 Revisar la implementación de _save_imagen en el serializer")
    else:
        print("❌ Hay problemas fundamentales con la configuración")
        print("🔧 Revisar render_settings.py y la configuración de Cloudinary")
    
    print("\n💡 RECOMENDACIONES:")
    if not storage_ok:
        print("1. Verificar que render_settings.py se está cargando correctamente")
        print("2. Revisar la configuración de CLOUDINARY_STORAGE")
        print("3. Verificar que las credenciales de Cloudinary son correctas")
    elif not serializer_ok:
        print("1. Revisar la implementación de _save_imagen en CategoriaProductoSerializer")
        print("2. Verificar que el storage se está usando correctamente")
    elif not api_ok:
        print("1. Verificar que Render está usando render_settings.py")
        print("2. Revisar los logs de Render para confirmar")
        print("3. Esperar a que se apliquen los cambios en Render")

if __name__ == '__main__':
    main() 