# Pruebas de Cloudinary en Producción

Este documento contiene las instrucciones para verificar que Cloudinary esté funcionando correctamente en producción (Render).

## 📋 Variables de Entorno Requeridas

Asegúrate de que las siguientes variables estén configuradas en Render:

```
CLOUDINARY_API_KEY=117225377115856
CLOUDINARY_API_SECRET=e0YSrk3sT_70-ijM6mwdFBIWP9w
CLOUDINARY_CLOUD_NAME=do1ntnlop
DATABASE_URL=postgresql://tienda_user:PWKuO99372EAcsyx5KpHlV9VBIQJkvle@dpg-d278j5u3jp1c73en5gbg-a.ohio-postgres.render.com/tienda_production
DEBUG=False
DJANGO_SETTINGS_MODULE=Backend.settings
RENDER=true
SECRET_KEY=r@4-b1_76%pp5%body-8!!cnbkh+sz+5m!ry2&7cpst7o+1p_d
TIME_ZONE=America/Bogota
```

## 🚀 Scripts de Prueba Disponibles

### 1. Prueba Rápida (Recomendada)
```bash
python test_render_cloudinary.py
```
Este script hace una verificación completa y rápida de:
- Variables de entorno
- Conexión a Cloudinary
- Subida de archivos
- Storage de Django
- Endpoints de la API

### 2. Prueba Detallada
```bash
python test_production_cloudinary.py
```
Prueba más exhaustiva que incluye:
- Verificación completa de configuración
- Pruebas de subida y eliminación
- Verificación de base de datos
- Reporte detallado

### 3. Verificación Rápida
```bash
python verify_production_cloudinary.py
```
Verificación mínima para confirmar que todo funciona.

## 🔧 Cómo Ejecutar en Render

### Opción 1: Desde la Consola de Render
1. Ve a tu dashboard de Render
2. Selecciona tu servicio web
3. Ve a la pestaña "Shell"
4. Ejecuta:
```bash
cd /opt/render/project/src/Backend
python test_render_cloudinary.py
```

### Opción 2: Desde el Log de Build
Agrega esto a tu `build.sh`:
```bash
echo "🔍 Probando Cloudinary..."
python test_render_cloudinary.py
```

### Opción 3: Como Comando de Inicio
Modifica tu `startCommand` en `render.yaml`:
```yaml
startCommand: "python test_render_cloudinary.py && gunicorn Backend.wsgi:application"
```

## 📊 Interpretación de Resultados

### ✅ Todo Funciona Correctamente
Si ves:
```
🎉 ¡TODAS LAS PRUEBAS PASARON! Cloudinary está funcionando correctamente en Render.
```

### ❌ Problemas Comunes

1. **Variables de entorno faltantes**:
   - Verifica que todas las variables estén configuradas en Render
   - Asegúrate de que los valores sean correctos

2. **Error de conexión a Cloudinary**:
   - Verifica que las credenciales sean correctas
   - Confirma que la cuenta de Cloudinary esté activa

3. **Error de storage**:
   - Verifica que `DEFAULT_FILE_STORAGE` esté configurado correctamente
   - Confirma que el archivo `cloudinary_storage_fixed.py` existe

4. **Error de base de datos**:
   - Verifica que `DATABASE_URL` sea correcta
   - Confirma que la base de datos esté accesible

## 🔍 Verificación Manual

### 1. Verificar Variables de Entorno
```bash
echo $CLOUDINARY_CLOUD_NAME
echo $CLOUDINARY_API_KEY
echo $CLOUDINARY_API_SECRET
echo $RENDER
```

### 2. Verificar Configuración de Django
```bash
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.render_settings')
django.setup()
from django.conf import settings
print(f'DEBUG: {settings.DEBUG}')
print(f'DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}')
print(f'RENDER: {os.environ.get(\"RENDER\")}')
"
```

### 3. Probar Conexión Directa a Cloudinary
```bash
python -c "
import cloudinary
import os
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)
result = cloudinary.api.ping()
print(f'Conexión: {result}')
"
```

## 🛠️ Solución de Problemas

### Problema: Variables de entorno no se cargan
**Solución**: Verifica que estén configuradas en el dashboard de Render

### Problema: Error de importación de Cloudinary
**Solución**: Asegúrate de que `cloudinary` esté en `requirements.txt`

### Problema: Error de storage
**Solución**: Verifica que el archivo `cloudinary_storage_fixed.py` esté presente

### Problema: Error de base de datos
**Solución**: Verifica que `DATABASE_URL` sea correcta y la BD esté activa

## 📝 Logs Útiles

Para ver logs en tiempo real en Render:
```bash
# En la consola de Render
tail -f /opt/render/logs/app.log
```

## 🎯 Resultado Esperado

Un resultado exitoso debería mostrar:
```
🚀 PRUEBA DE CLOUDINARY EN RENDER
============================================================
✅ Configuración de producción cargada (render_settings.py)

🔧 PRUEBA BÁSICA DE CONFIGURACIÓN
==================================================
📋 Variables de Entorno:
  ✅ CLOUDINARY_CLOUD_NAME: do1ntnlop
  ✅ CLOUDINARY_API_KEY: 117225377...
  ✅ CLOUDINARY_API_SECRET: e0YSrk3sT_...
  ✅ DATABASE_URL: postgresql://...
  ✅ RENDER: true

⚙️ Configuración Django:
  DEBUG: False
  DEFAULT_FILE_STORAGE: Backend.cloudinary_storage_fixed.CloudinaryStorage
  MEDIA_URL: /media/

🌐 PRUEBA DE CONEXIÓN A CLOUDINARY
==================================================
✅ Conexión exitosa: ok
✅ Información de cuenta:
  Cloud Name: do1ntnlop
  Plan: free

📤 PRUEBA DE SUBIDA
==================================================
✅ Subida exitosa:
  Public ID: render_test_upload
  URL: https://res.cloudinary.com/do1ntnlop/image/upload/v1/render_test_upload
  Tamaño: 1234 bytes
✅ Imagen accesible desde URL
✅ Archivo de prueba eliminado

🔧 PRUEBA DE STORAGE DJANGO
==================================================
Storage actual: CloudinaryStorage
Storage configurado: Backend.cloudinary_storage_fixed.CloudinaryStorage
✅ Usando CloudinaryStorage

🌐 PRUEBA DE ENDPOINTS API
==================================================
✅ Productos: OK (200)
✅ Categorías: OK (200)

📊 RESUMEN DE PRUEBAS
============================================================
Configuración Básica    ✅ PASÓ
Conexión Cloudinary     ✅ PASÓ
Subida de Archivos      ✅ PASÓ
Storage Django          ✅ PASÓ
Endpoints API           ✅ PASÓ

🎯 RESULTADO: 5/5 pruebas pasaron
🎉 ¡TODAS LAS PRUEBAS PASARON! Cloudinary está funcionando correctamente en Render.
``` 