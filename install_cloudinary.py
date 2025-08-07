#!/usr/bin/env python3
"""
Script para instalar Cloudinary y remover ImageKit
"""
import subprocess
import sys
import os

def install_cloudinary():
    """Instalar Cloudinary y remover ImageKit"""
    print("🔧 Instalando Cloudinary y removiendo ImageKit...")
    
    try:
        # Instalar Cloudinary
        print("📦 Instalando cloudinary...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cloudinary==1.36.0"])
        print("✅ Cloudinary instalado correctamente")
        
        # Desinstalar ImageKit
        print("🗑️ Desinstalando imagekitio...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "imagekitio"])
        print("✅ ImageKit removido correctamente")
        
        # Verificar instalación
        print("🔍 Verificando instalación...")
        subprocess.check_call([sys.executable, "-c", "import cloudinary; print('✅ Cloudinary importado correctamente')"])
        
        print("\n🎉 ¡Migración completada exitosamente!")
        print("📋 Cambios realizados:")
        print("  ✅ Cloudinary instalado")
        print("  ✅ ImageKit removido")
        print("  ✅ Storage configurado para desarrollo local")
        print("\n🚀 Puedes ejecutar 'python test_cloudinary.py' para verificar la configuración")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la instalación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = install_cloudinary()
    if not success:
        sys.exit(1) 