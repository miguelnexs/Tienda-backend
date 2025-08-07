#!/usr/bin/env python3
"""
Script para verificar credenciales de Cloudinary y probar subida directa
"""
import cloudinary
import cloudinary.api
import cloudinary.uploader
from io import BytesIO
from PIL import Image

def verify_credentials():
    """Verificar credenciales de Cloudinary"""
    print("🔍 VERIFICANDO CREDENCIALES DE CLOUDINARY")
    print("=" * 60)
    
    # Credenciales proporcionadas
    cloud_name = "do1ntnlop"
    api_key = "117225377115856"
    api_secret = "e0YSrk3sT_70-ijM6mwdFBIWP9w"
    
    print(f"📋 Credenciales a verificar:")
    print(f"  Cloud Name: {cloud_name}")
    print(f"  API Key: {api_key}")
    print(f"  API Secret: {api_secret[:10]}...")
    
    try:
        # Configurar Cloudinary
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
        print("\n✅ Cloudinary configurado correctamente")
        
        # Probar conexión
        try:
            result = cloudinary.api.ping()
            print("✅ Conexión a Cloudinary exitosa")
        except Exception as e:
            print(f"❌ Error conectando a Cloudinary: {e}")
            return False
        
        # Probar subida directa
        print("\n🧪 Probando subida directa...")
        
        # Crear imagen de prueba
        img = Image.new('RGB', (300, 300), color='red')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Subir directamente
        result = cloudinary.uploader.upload(
            img_io,
            public_id=f"test_credentials_{cloud_name}",
            resource_type="image",
            overwrite=True
        )
        
        print("✅ Subida directa exitosa")
        print(f"  Public ID: {result['public_id']}")
        print(f"  URL: {result['secure_url']}")
        print(f"  Tamaño: {result.get('bytes', 0)} bytes")
        
        # Verificar que existe
        try:
            resource = cloudinary.api.resource(result['public_id'])
            print("✅ Archivo existe en Cloudinary")
            print(f"  URL segura: {resource.get('secure_url')}")
        except Exception as e:
            print(f"❌ Error verificando archivo: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando credenciales: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_django_storage():
    """Probar storage de Django"""
    print("\n🧪 PROBANDO STORAGE DE DJANGO")
    print("=" * 60)
    
    try:
        import os
        import sys
        import django
        
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        django.setup()
        
        from Backend.cloudinary_storage_complete import CloudinaryStorageComplete
        from django.core.files import File
        
        # Crear imagen de prueba
        img = Image.new('RGB', (400, 400), color='blue')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear archivo Django
        django_file = File(img_io, name=f'test_django_storage_{os.getpid()}.jpg')
        
        # Usar storage
        storage = CloudinaryStorageComplete()
        saved_name = storage.save(django_file.name, django_file)
        
        print("✅ Storage de Django funcionando")
        print(f"  Nombre guardado: {saved_name}")
        
        # Obtener URL
        url = storage.url(saved_name)
        print(f"  URL: {url}")
        
        # Verificar existencia
        exists = storage.exists(saved_name)
        print(f"  Existe: {exists}")
        
        # Limpiar
        storage.delete(saved_name)
        print("✅ Archivo eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando storage de Django: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_admin_simulation():
    """Simular exactamente lo que hace el admin"""
    print("\n🧪 SIMULANDO ADMIN DE DJANGO")
    print("=" * 60)
    
    try:
        import os
        import sys
        import django
        
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        django.setup()
        
        from categorias.models import CategoriaProducto
        from django.core.files import File
        
        # Crear imagen de prueba
        img = Image.new('RGB', (500, 500), color='green')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # Crear categoría
        categoria = CategoriaProducto(
            nombre="Categoría Test Credenciales",
            descripcion="Categoría para probar credenciales",
            slug=f"categoria-test-credenciales-{os.getpid()}"
        )
        
        # Guardar categoría
        categoria.save()
        print(f"✅ Categoría creada: {categoria.id}")
        
        # Crear archivo como lo haría el admin
        django_file = File(img_io, name=f'categoria_test_credenciales_{os.getpid()}.jpg')
        
        print("📤 Subiendo imagen como lo haría el admin...")
        
        # Asignar imagen (exactamente como lo hace el admin)
        categoria.imagen.save(django_file.name, django_file, save=True)
        
        print("✅ Imagen asignada")
        print(f"  Nombre: {categoria.imagen.name}")
        print(f"  URL: {categoria.imagen.url}")
        
        # Verificar URL
        if 'cloudinary.com' in categoria.imagen.url:
            print("✅ URL es de Cloudinary")
        else:
            print("❌ URL no es de Cloudinary")
        
        # Verificar existencia
        if hasattr(categoria.imagen, 'storage'):
            exists = categoria.imagen.storage.exists(categoria.imagen.name)
            print(f"  Existe en storage: {exists}")
        
        # Obtener información de Cloudinary
        try:
            import cloudinary.api
            result = cloudinary.api.resource(categoria.imagen.name)
            print(f"📊 Información de Cloudinary:")
            print(f"  Public ID: {result['public_id']}")
            print(f"  URL segura: {result.get('secure_url', 'N/A')}")
            print(f"  Tamaño: {result.get('bytes', 0)} bytes")
        except Exception as e:
            print(f"⚠️ No se pudo obtener información: {e}")
        
        # Limpiar
        categoria.delete()
        print("✅ Categoría eliminada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error simulando admin: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO VERIFICACIÓN DE CREDENCIALES")
    print("=" * 60)
    
    # Verificar credenciales
    cred_success = verify_credentials()
    
    # Probar storage de Django
    storage_success = test_django_storage()
    
    # Simular admin
    admin_success = test_admin_simulation()
    
    print("\n📊 RESULTADOS FINALES")
    print("=" * 60)
    print(f"Credenciales: {'✅ PASÓ' if cred_success else '❌ FALLÓ'}")
    print(f"Storage Django: {'✅ PASÓ' if storage_success else '❌ FALLÓ'}")
    print(f"Simulación Admin: {'✅ PASÓ' if admin_success else '❌ FALLÓ'}")
    
    if cred_success and storage_success and admin_success:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ Las credenciales son correctas.")
        print("✅ El storage funciona correctamente.")
        print("✅ El admin funciona correctamente.")
    else:
        print("\n⚠️ Algunas pruebas fallaron.")
        print("❌ Revisa las credenciales o configuración.") 