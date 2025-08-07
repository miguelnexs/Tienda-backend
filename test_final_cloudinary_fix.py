#!/usr/bin/env python
"""
Script final para probar la configuración de Cloudinary corregida
"""
import os
import sys
import django
import requests
import json
from pathlib import Path
from datetime import datetime

def test_local_settings():
    """Probar configuración local"""
    
    print("🔍 PROBANDO CONFIGURACIÓN LOCAL")
    print("="*50)
    
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
        
        print("✅ Configuración local cargada")
        print(f"📋 DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        print(f"📋 STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
        
        if hasattr(settings, 'CLOUDINARY'):
            print(f"☁️ CLOUDINARY configurado: {settings.CLOUDINARY}")
        else:
            print("❌ CLOUDINARY no configurado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración local: {e}")
        return False

def test_render_api():
    """Probar API de Render"""
    
    print("\n🌐 PROBANDO API DE RENDER")
    print("="*50)
    
    RENDER_API_URL = "https://tienda-backend-qsre.onrender.com/api"
    
    try:
        # 1. Verificar respuesta del servicio
        print("📋 1. Verificando respuesta del servicio...")
        
        response = requests.get(f"{RENDER_API_URL}/categorias/", timeout=30)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ El servicio está respondiendo")
            
            try:
                categorias = response.json()
                print(f"📊 Número de categorías: {len(categorias)}")
                
                # Verificar URLs de imágenes existentes
                cloudinary_count = 0
                local_count = 0
                
                for categoria in categorias:
                    if isinstance(categoria, dict) and categoria.get('imagen_url'):
                        if 'cloudinary.com' in categoria['imagen_url']:
                            cloudinary_count += 1
                        elif 'onrender.com/media' in categoria['imagen_url']:
                            local_count += 1
                
                print(f"☁️ Imágenes en Cloudinary: {cloudinary_count}")
                print(f"📁 Imágenes locales: {local_count}")
                
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                return False
        
        # 2. Crear nueva categoría con nombre único
        print("\n📋 2. Creando categoría de prueba...")
        
        # Generar nombre único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_categoria = f"Test Final Fix {timestamp}"
        
        # Buscar imagen de prueba
        imagen_path = Path("D:/usuario/Downloads/bolso/cartera-casual-para-mujer-23064.jpg")
        
        if imagen_path.exists():
            # Preparar datos
            data = {
                'nombre': nombre_categoria,
                'descripcion': f'Prueba final de configuración corregida - {timestamp}',
                'activa': True,
                'orden': 987
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
                        print("✅ El servicio está usando render_settings.py correctamente")
                        return True
                    else:
                        print("📁 La imagen se guardó localmente")
                        print("⚠️ El servicio NO está usando render_settings.py")
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

def main():
    """Función principal"""
    print("🎯 PRUEBA FINAL DE CONFIGURACIÓN DE CLOUDINARY")
    print("="*60)
    
    # Probar configuración local
    local_ok = test_local_settings()
    
    # Probar API de Render
    api_ok = test_render_api()
    
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL")
    print("="*60)
    print(f"✅ Configuración local: {'EXITOSA' if local_ok else 'FALLIDA'}")
    print(f"✅ API de Render: {'EXITOSA' if api_ok else 'FALLIDA'}")
    
    # Conclusión
    print("\n" + "="*60)
    print("🎯 CONCLUSIÓN")
    print("="*60)
    
    if local_ok and api_ok:
        print("🎉 ¡PERFECTO! La configuración está funcionando correctamente")
        print("✅ La configuración local es correcta")
        print("✅ Las imágenes se suben a Cloudinary desde Render")
        print("✅ El problema está resuelto")
    elif local_ok:
        print("✅ La configuración local es correcta")
        print("⚠️ Pero las imágenes aún se guardan localmente en Render")
        print("🔧 Esperar a que se aplique el cambio en Render")
    else:
        print("❌ Hay problemas con la configuración local")
        print("🔧 Revisar la configuración de render_settings.py")
    
    print("\n💡 RECOMENDACIONES:")
    if not api_ok:
        print("1. Esperar a que Render aplique los cambios")
        print("2. Verificar los logs de Render para confirmar")
        print("3. Probar crear otra categoría en unos minutos")
    else:
        print("1. ¡Todo está funcionando perfectamente!")
        print("2. Las nuevas imágenes se subirán a Cloudinary")
        print("3. El problema está completamente resuelto")

if __name__ == '__main__':
    main() 