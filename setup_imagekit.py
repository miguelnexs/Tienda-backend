#!/usr/bin/env python3
"""
Script de configuración automática para ImageKit.io
Ejecutar con: python setup_imagekit.py
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    """Imprimir encabezado formateado"""
    print(f"\n{'='*50}")
    print(f"🔧 {title}")
    print(f"{'='*50}")

def check_python_version():
    """Verificar versión de Python"""
    print_header("VERIFICACIÓN DE PYTHON")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    
    print("✅ Versión de Python compatible")
    return True

def install_dependencies():
    """Instalar dependencias de ImageKit"""
    print_header("INSTALACIÓN DE DEPENDENCIAS")
    
    try:
        # Actualizar requirements.txt
        subprocess.run([
            sys.executable, "-m", "pip", "install", "imagekit==4.0.2"
        ], check=True)
        print("✅ ImageKit instalado correctamente")
        
        # Instalar requests para el script de migración
        subprocess.run([
            sys.executable, "-m", "pip", "install", "requests"
        ], check=True)
        print("✅ Requests instalado correctamente")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_env_file():
    """Crear archivo .env con variables de ImageKit"""
    print_header("CONFIGURACIÓN DE VARIABLES DE ENTORNO")
    
    env_file = Path(".env")
    
    if env_file.exists():
        print("📁 Archivo .env ya existe")
        
        # Verificar si ya tiene las variables de ImageKit
        content = env_file.read_text()
        if "IMAGEKIT_PUBLIC_KEY" in content:
            print("✅ Variables de ImageKit ya configuradas")
            return True
    
    # Solicitar credenciales al usuario
    print("🔑 Configuración de ImageKit.io")
    print("Obtén tus credenciales en: https://imagekit.io/dashboard/developers/api-keys")
    print()
    
    public_key = input("Public Key: ").strip()
    private_key = input("Private Key: ").strip()
    url_endpoint = input("URL Endpoint (ej: https://ik.imagekit.io/tu_endpoint): ").strip()
    
    if not all([public_key, private_key, url_endpoint]):
        print("❌ Todas las credenciales son requeridas")
        return False
    
    # Crear contenido del archivo .env
    env_content = f"""
# Configuración de la base de datos local
DATABASE_URL=postgresql://productos:migel1457@localhost:5432/tiendadb

# Clave secreta para desarrollo (cambia en producción)
SECRET_KEY=tu-clave-secreta-super-segura-para-desarrollo

# Configuración de debug
DEBUG=True

# URL del frontend (para desarrollo)
FRONTEND_URL=http://localhost:3000

# Configuración de CORS para desarrollo
CORS_ALLOW_ALL_ORIGINS=True

# Configuración de archivos estáticos
STATIC_URL=/static/
MEDIA_URL=/media/

# Configuración de ImageKit.io
IMAGEKIT_PUBLIC_KEY={public_key}
IMAGEKIT_PRIVATE_KEY={private_key}
IMAGEKIT_URL_ENDPOINT={url_endpoint}
"""
    
    # Escribir archivo .env
    with open(env_file, "w") as f:
        f.write(env_content.strip())
    
    print("✅ Archivo .env creado con las variables de ImageKit")
    return True

def run_tests():
    """Ejecutar pruebas de configuración"""
    print_header("PRUEBAS DE CONFIGURACIÓN")
    
    try:
        # Ejecutar script de pruebas
        result = subprocess.run([
            sys.executable, "test_imagekit.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Todas las pruebas pasaron")
            return True
        else:
            print("❌ Algunas pruebas fallaron")
            print("Salida:", result.stdout)
            print("Errores:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando pruebas: {e}")
        return False

def show_next_steps():
    """Mostrar próximos pasos"""
    print_header("PRÓXIMOS PASOS")
    
    print("🎉 ¡Configuración completada!")
    print()
    print("📋 Para completar la migración:")
    print("1. Ejecuta las migraciones de Django:")
    print("   python manage.py migrate")
    print()
    print("2. Ejecuta el script de migración de datos:")
    print("   python migrate_to_imagekit.py")
    print()
    print("3. Inicia el servidor de desarrollo:")
    print("   python manage.py runserver")
    print()
    print("4. Prueba la subida de imágenes desde el frontend")
    print()
    print("📚 Documentación:")
    print("- Revisa MIGRACION_IMAGEKIT.md para detalles completos")
    print("- Consulta la documentación de ImageKit.io")
    print()
    print("🔧 Troubleshooting:")
    print("- Si hay errores, ejecuta: python test_imagekit.py")
    print("- Verifica las variables de entorno en el archivo .env")

def main():
    """Función principal"""
    print("🚀 CONFIGURACIÓN AUTOMÁTICA DE IMAGEKIT.IO")
    print("="*50)
    
    steps = [
        ("Verificación de Python", check_python_version),
        ("Instalación de dependencias", install_dependencies),
        ("Configuración de variables", create_env_file),
        ("Pruebas de configuración", run_tests),
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            print(f"❌ Error en: {step_name}")
            print("Revisa los errores y ejecuta el script nuevamente")
            return
    
    show_next_steps()

if __name__ == "__main__":
    main() 