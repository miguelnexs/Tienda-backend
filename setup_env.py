#!/usr/bin/env python
"""
Script para configurar variables de entorno de Cloudinary localmente
"""

import os

def setup_cloudinary_env():
    """Configura las variables de entorno de Cloudinary"""
    print("🔧 Configurando variables de entorno de Cloudinary...")
    
    # Configurar variables de entorno
    os.environ['CLOUDINARY_CLOUD_NAME'] = 'mediaflows_4bc5a48b-2274-4a45-99b2-d05a4519862f'
    os.environ['CLOUDINARY_API_KEY'] = '117225377115856'
    os.environ['CLOUDINARY_API_SECRET'] = 'e0YSrk3sT_70-ijM6mwdFBIWP9w'
    
    print("✅ Variables de entorno configuradas:")
    print(f"   CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME')}")
    print(f"   CLOUDINARY_API_KEY: {os.environ.get('CLOUDINARY_API_KEY')}")
    print(f"   CLOUDINARY_API_SECRET: {os.environ.get('CLOUDINARY_API_SECRET')[:10]}...")
    
    print("\n🎯 Ahora puedes probar subiendo una imagen!")

if __name__ == "__main__":
    setup_cloudinary_env() 