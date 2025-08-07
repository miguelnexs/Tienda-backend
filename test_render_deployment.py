#!/usr/bin/env python
"""
Script para probar el deployment de Render después de aplicar los cambios
"""
import requests
import json
from pathlib import Path
from datetime import datetime
import time

def test_render_deployment():
    """Probar el deployment de Render"""
    
    print("🚀 PROBANDO DEPLOYMENT DE RENDER")
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
                            print(f"☁️ Cloudinary: {categoria['imagen_url']}")
                        elif 'onrender.com/media' in categoria['imagen_url']:
                            local_count += 1
                            print(f"📁 Local: {categoria['imagen_url']}")
                
                print(f"\n📊 RESUMEN DE IMÁGENES EXISTENTES:")
                print(f"☁️ Imágenes en Cloudinary: {cloudinary_count}")
                print(f"📁 Imágenes locales: {local_count}")
                
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando respuesta: {e}")
                return False
        
        # 2. Crear nueva categoría con imagen
        print("\n📋 2. Creando categoría con imagen...")
        
        # Generar nombre único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_categoria = f"Test Deployment {timestamp}"
        
        # Buscar imagen de prueba
        imagen_path = Path("D:/usuario/Downloads/bolso/cartera-casual-para-mujer-23064.jpg")
        
        if imagen_path.exists():
            # Preparar datos
            data = {
                'nombre': nombre_categoria,
                'descripcion': f'Prueba de deployment - {timestamp}',
                'activa': True,
                'orden': 993
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
                        print("✅ El deployment está funcionando correctamente")
                        return True
                    else:
                        print("📁 La imagen se guardó localmente")
                        print("⚠️ El deployment aún no ha aplicado los cambios")
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
    print("🎯 PRUEBA DE DEPLOYMENT DE RENDER")
    print("="*60)
    
    # Probar deployment
    deployment_ok = test_render_deployment()
    
    print("\n" + "="*60)
    print("📊 RESUMEN")
    print("="*60)
    print(f"✅ Deployment: {'EXITOSO' if deployment_ok else 'PENDIENTE'}")
    
    if deployment_ok:
        print("🎉 ¡PERFECTO! El deployment está funcionando correctamente")
        print("✅ Las imágenes se suben a Cloudinary")
        print("✅ El problema está completamente resuelto")
    else:
        print("⏳ El deployment aún no ha aplicado los cambios")
        print("💡 RECOMENDACIONES:")
        print("1. Esperar 5-10 minutos para que Render aplique los cambios")
        print("2. Verificar los logs de Render para confirmar")
        print("3. Ejecutar este script nuevamente en unos minutos")
        print("4. Los cambios incluyen:")
        print("   - Removidas referencias a django-cloudinary-storage")
        print("   - Configurado nuestro storage personalizado")
        print("   - Actualizado render_settings.py")

if __name__ == '__main__':
    main() 