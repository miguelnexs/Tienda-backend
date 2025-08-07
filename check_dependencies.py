#!/usr/bin/env python3
"""
Script para verificar dependencias necesarias para Cloudinary
"""
import sys
import subprocess

def check_package(package_name, import_name=None):
    """Verificar si un paquete está instalado"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name}")
        return True
    except ImportError:
        print(f"❌ {package_name} - NO INSTALADO")
        return False

def check_pip_package(package_name):
    """Verificar paquete usando pip"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {package_name}")
            return True
        else:
            print(f"❌ {package_name} - NO INSTALADO")
            return False
    except Exception:
        print(f"❌ {package_name} - ERROR VERIFICANDO")
        return False

def main():
    """Verificar todas las dependencias"""
    print("🔍 VERIFICANDO DEPENDENCIAS PARA CLOUDINARY")
    print("=" * 50)
    
    # Dependencias principales
    main_packages = [
        ("django", "django"),
        ("cloudinary", "cloudinary"),
        ("Pillow", "PIL"),
        ("requests", "requests"),
        ("psycopg2-binary", "psycopg2"),
        ("python-dotenv", "dotenv"),
        ("django-cors-headers", "corsheaders"),
        ("django-filter", "django_filters"),
        ("django-colorfield", "colorfield"),
        ("djangorestframework", "rest_framework"),
    ]
    
    print("\n📦 DEPENDENCIAS PRINCIPALES:")
    main_installed = 0
    for package, import_name in main_packages:
        if check_package(package, import_name):
            main_installed += 1
    
    # Dependencias opcionales
    optional_packages = [
        ("whitenoise", "whitenoise"),
        ("dj-database-url", "dj_database_url"),
    ]
    
    print("\n📦 DEPENDENCIAS OPCIONALES:")
    optional_installed = 0
    for package, import_name in optional_packages:
        if check_package(package, import_name):
            optional_installed += 1
    
    # Verificar versiones específicas
    print("\n📋 VERSIONES INSTALADAS:")
    version_packages = [
        "django",
        "cloudinary",
        "Pillow",
        "requests",
        "djangorestframework",
    ]
    
    for package in version_packages:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", package],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                version = "N/A"
                for line in lines:
                    if line.startswith('Version:'):
                        version = line.split(':')[1].strip()
                        break
                print(f"  {package}: {version}")
        except Exception:
            print(f"  {package}: Error verificando")
    
    # Resumen
    print(f"\n📊 RESUMEN:")
    print(f"  Dependencias principales: {main_installed}/{len(main_packages)}")
    print(f"  Dependencias opcionales: {optional_installed}/{len(optional_packages)}")
    
    if main_installed == len(main_packages):
        print("✅ Todas las dependencias principales están instaladas")
        return True
    else:
        print("❌ Faltan algunas dependencias principales")
        print("\n💡 Para instalar las dependencias faltantes:")
        print("   pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 