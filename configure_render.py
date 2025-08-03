#!/usr/bin/env python
"""
Script para configurar variables de entorno en Render
"""

def print_render_config():
    """Imprime las instrucciones para configurar Render"""
    print("🚀 Configuración de Variables de Entorno en Render")
    print("=" * 50)
    
    print("\n📋 Variables a configurar en Render:")
    print("1. Ve a tu dashboard de Render")
    print("2. Selecciona tu servicio 'tienda-backend-api'")
    print("3. Ve a 'Settings > Environment Variables'")
    print("4. Agrega estas 3 variables:")
    
    print("\n🔧 Variables de entorno:")
    print("CLOUDINARY_CLOUD_NAME=do1ntnlop")
    print("CLOUDINARY_API_KEY=117225377115856")
    print("CLOUDINARY_API_SECRET=e0YSrk3sT_70-ijM6mwdFBIWP9w")
    
    print("\n📝 Pasos:")
    print("1. Haz clic en 'Add Environment Variable'")
    print("2. Agrega cada variable una por una")
    print("3. Guarda los cambios")
    print("4. Render redesplegará automáticamente")
    
    print("\n✅ Después del despliegue:")
    print("- Las imágenes se subirán a Cloudinary")
    print("- Las URLs cambiarán de /media/ a URLs de Cloudinary")
    print("- Las imágenes serán persistentes")
    
    print("\n🧪 Para verificar:")
    print("1. Ve a los logs de Render")
    print("2. Busca mensajes de Cloudinary")
    print("3. Prueba subiendo una imagen desde tu app")

if __name__ == "__main__":
    print_render_config() 