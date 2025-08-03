# Configuración de Cloudinary para Subida de Imágenes

## Problema Identificado

Las imágenes no se están subiendo correctamente al cloud desde Render. Este documento explica cómo configurar y solucionar los problemas de subida de imágenes.

## Configuración Requerida

### 1. Variables de Entorno en Render

Asegúrate de que las siguientes variables estén configuradas en tu proyecto de Render:

```bash
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

### 2. Configuración Local (Desarrollo)

Para desarrollo local, puedes crear un archivo `.env` en el directorio `Backend/` con:

```bash
# Configuración de Cloudinary (opcional para desarrollo)
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret

# Otras variables de desarrollo
DATABASE_URL=postgresql://productos:migel1457@localhost:5432/tiendadb
SECRET_KEY=tu-clave-secreta-super-segura-para-desarrollo
DEBUG=True
```

### 3. Verificación de Configuración

Puedes verificar la configuración usando el endpoint de debug:

```bash
# En desarrollo local
curl http://localhost:8000/api/productos/debug/environment/

# En producción (Render)
curl https://tienda-backend-ap-api.onrender.com/api/productos/debug/environment/
```

### 4. Script de Prueba

Ejecuta el script de prueba para verificar la configuración:

```bash
cd Backend
python test_image_upload.py
```

## Cambios Realizados

### 1. Configuración de Settings (`Backend/settings.py`)

- ✅ Mejorada la configuración condicional de Cloudinary
- ✅ Agregado logging para debugging
- ✅ Configuración de storage local para desarrollo

### 2. Serializadores Mejorados

- ✅ `productos/serializers/color.py`: Manejo correcto de URLs de Cloudinary
- ✅ `productos/serializers/producto.py`: URLs de imagen principal
- ✅ `categorias/serializers.py`: URLs de imágenes de categorías

### 3. Validaciones de Imágenes

- ✅ `productos/views/colores.py`: Validaciones completas de imágenes
- ✅ Verificación de tipo, tamaño y dimensiones
- ✅ Manejo de errores mejorado

### 4. Endpoint de Debug

- ✅ `productos/views/debug.py`: Información detallada de configuración
- ✅ Verificación de variables de entorno
- ✅ Estado de configuración de Django

## Solución de Problemas

### Problema 1: Variables de Entorno No Configuradas

**Síntomas:**
- Las imágenes se guardan localmente en lugar de Cloudinary
- URLs de imágenes apuntan a `/media/` en lugar de Cloudinary

**Solución:**
1. Verifica que las variables de entorno estén configuradas en Render
2. Reinicia el servicio después de agregar las variables
3. Verifica con el endpoint de debug

### Problema 2: URLs de Imágenes Incorrectas

**Síntomas:**
- Las imágenes no se cargan en el frontend
- URLs rotas o incorrectas

**Solución:**
1. Los serializadores ahora manejan correctamente las URLs
2. Verifica que el frontend esté usando las URLs correctas
3. Revisa la configuración de CORS

### Problema 3: Errores de Validación

**Síntomas:**
- Errores al subir imágenes
- Mensajes de validación confusos

**Solución:**
1. Las validaciones ahora son más claras
2. Verifica el formato y tamaño de las imágenes
3. Revisa los logs del backend

## Testing

### 1. Prueba de Configuración

```bash
cd Backend
python test_image_upload.py
```

### 2. Prueba Manual

1. Accede al endpoint de debug
2. Intenta subir una imagen desde el frontend
3. Verifica que la URL de la imagen sea correcta

### 3. Verificación en Producción

1. Ve a https://tienda-backend-ap-api.onrender.com/api/productos/debug/environment/
2. Verifica que todas las variables estén configuradas
3. Prueba subir una imagen desde el frontend

## Logs y Debugging

### Logs del Backend

Los logs ahora incluyen información detallada sobre:
- Configuración de Cloudinary
- Errores de subida de imágenes
- URLs generadas

### Endpoint de Debug

El endpoint `/api/productos/debug/environment/` proporciona:
- Estado de variables de entorno
- Configuración de Django
- Estado de Cloudinary

## Notas Importantes

1. **Desarrollo vs Producción**: En desarrollo local, las imágenes se guardan localmente si no hay variables de Cloudinary configuradas.

2. **Variables de Entorno**: Las variables de Cloudinary son obligatorias en producción (Render).

3. **CORS**: Asegúrate de que el frontend tenga acceso a las URLs de Cloudinary.

4. **Tamaños de Imagen**: Las imágenes tienen límites de tamaño y dimensiones para optimizar el rendimiento.

## Contacto

Si sigues teniendo problemas, verifica:
1. Las variables de entorno en Render
2. Los logs del backend
3. El endpoint de debug
4. El script de prueba 