# Guía de Despliegue en Render

## Configuración del Proyecto

Este proyecto ha sido configurado específicamente para funcionar en Render sin problemas de fecha.

### Archivos de Configuración

1. **`Backend/render_settings.py`** - Configuración específica para Render
2. **`Backend/init_render.py`** - Script de inicialización
3. **`Backend/check_deployment.py`** - Script de verificación
4. **`Backend/build.sh`** - Script de build actualizado

### Variables de Entorno Requeridas

En Render, asegúrate de configurar las siguientes variables de entorno:

```bash
# Base de datos (se configura automáticamente en Render)
DATABASE_URL=postgresql://...

# Django
DJANGO_SETTINGS_MODULE=Backend.render_settings
SECRET_KEY=tu-clave-secreta-super-segura

# Configuración de la aplicación
DEBUG=False
ALLOWED_HOSTS=tu-app.onrender.com
```

### Proceso de Despliegue

1. **Build Command**: `./build.sh`
2. **Start Command**: `gunicorn Backend.wsgi:application`

### Verificaciones Automáticas

El script `check_deployment.py` verifica:
- ✅ Configuración de base de datos
- ✅ Migraciones aplicadas
- ✅ Archivos estáticos
- ✅ Configuración general

### Solución de Problemas

#### Error de Fecha (fromisoformat)

Si encuentras el error `fromisoformat: argument must be str`, el proyecto incluye:

1. **Migraciones de corrección** que arreglan campos de fecha
2. **Configuración específica** en `render_settings.py`
3. **Script de inicialización** que maneja la base de datos

#### Logs de Debug

Los logs incluyen información detallada sobre:
- Configuración de base de datos
- Estado de migraciones
- Errores de archivos estáticos

### Estructura de Archivos

```
Backend/
├── render_settings.py      # Configuración para Render
├── init_render.py         # Script de inicialización
├── check_deployment.py    # Script de verificación
├── build.sh              # Script de build
└── render.yaml           # Configuración de Render
```

### Comandos Útiles

```bash
# Verificar configuración local
python check_deployment.py

# Inicializar base de datos
python init_render.py

# Ejecutar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

### Notas Importantes

1. **Sin Cloudinary**: El proyecto ya no usa Cloudinary, todas las imágenes se guardan localmente
2. **Configuración Simplificada**: No se requieren variables de entorno complejas
3. **Logging Mejorado**: Los logs ayudan a diagnosticar problemas
4. **Migraciones Automáticas**: Se ejecutan automáticamente durante el build

### Contacto

Si tienes problemas con el despliegue:
1. Revisa los logs en Render
2. Ejecuta `python check_deployment.py` localmente
3. Verifica que todas las variables de entorno estén configuradas 