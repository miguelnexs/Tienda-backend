# Configuración de Cloudinary para Almacenamiento de Imágenes

## ¿Por qué Cloudinary?

Render no proporciona almacenamiento persistente para archivos. Cuando el contenedor se reinicia, todas las imágenes subidas se pierden. Cloudinary es una solución gratuita y robusta para almacenamiento de imágenes en la nube.

## Pasos para Configurar Cloudinary

### 1. Crear cuenta en Cloudinary

1. Ve a [cloudinary.com](https://cloudinary.com)
2. Regístrate para una cuenta gratuita
3. Una vez registrado, ve a tu Dashboard
4. Copia tu `Cloud Name`, `API Key` y `API Secret`

### 2. Configurar Variables de Entorno

#### En Render (Producción):
1. Ve a tu proyecto en Render
2. Ve a la sección "Environment"
3. Agrega estas variables:
   ```
   CLOUDINARY_CLOUD_NAME=tu-cloud-name
   CLOUDINARY_API_KEY=tu-api-key
   CLOUDINARY_API_SECRET=tu-api-secret
   ```

#### En Desarrollo Local:
1. Crea un archivo `.env` en la raíz del proyecto Backend
2. Agrega las mismas variables:
   ```
   CLOUDINARY_CLOUD_NAME=tu-cloud-name
   CLOUDINARY_API_KEY=tu-api-key
   CLOUDINARY_API_SECRET=tu-api-secret
   ```

### 3. Instalar Dependencias

```bash
pip install django-cloudinary-storage
```

### 4. Configuración Automática

El proyecto ya está configurado para usar Cloudinary automáticamente cuando detecta que está en Render (producción). En desarrollo local seguirá usando almacenamiento local.

### 5. Migrar Imágenes Existentes (Opcional)

Si ya tienes imágenes en tu base de datos local, puedes migrarlas a Cloudinary:

```bash
python migrate_to_cloudinary.py
```

## Características de Cloudinary

- **Gratuito**: 25 GB de almacenamiento y 25 GB de ancho de banda mensual
- **Transformaciones automáticas**: Redimensionamiento, compresión, formatos optimizados
- **CDN global**: Imágenes servidas desde servidores cercanos
- **Seguridad**: URLs seguras con HTTPS

## Estructura de Carpetas en Cloudinary

- `/productos/` - Imágenes principales de productos
- `/productos/colores/` - Imágenes de colores específicos

## URLs de Imágenes

Las imágenes se servirán desde URLs como:
- `https://res.cloudinary.com/tu-cloud-name/image/upload/v1234567890/productos/producto_1_principal.jpg`

## Troubleshooting

### Error: "Invalid cloud name"
- Verifica que `CLOUDINARY_CLOUD_NAME` esté correctamente configurado

### Error: "Invalid API key"
- Verifica que `CLOUDINARY_API_KEY` y `CLOUDINARY_API_SECRET` sean correctos

### Las imágenes no se suben
- Verifica que las variables de entorno estén configuradas en Render
- Asegúrate de que el proyecto esté desplegado con las nuevas variables

### Migración fallida
- Verifica que las imágenes existan en el sistema de archivos local
- Asegúrate de tener permisos de lectura en la carpeta `media/` 