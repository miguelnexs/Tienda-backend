# 🚀 Guía de Deploy en Render

## 📋 Configuración Lista para Producción

### ✅ Archivos Configurados:

1. **`render.yaml`** - Configuración de Render con variables de entorno
2. **`Backend/render_settings.py`** - Configuración de Django para producción
3. **`build.sh`** - Script de build con verificaciones
4. **`check_production.py`** - Verificación de configuración de producción

### 🔧 Variables de Entorno Configuradas:

```yaml
CLOUDINARY_CLOUD_NAME: do1ntnlop
CLOUDINARY_API_KEY: 117225377115856
CLOUDINARY_API_SECRET: e0YSrk3sT_70-ijM6mwdFBIWP9w
DJANGO_CLOUDINARY_STORAGE: true
DJANGO_SETTINGS_MODULE: Backend.render_settings
```

### 🚀 Pasos para Deploy:

#### 1. Preparar el Repositorio
```bash
# Asegúrate de que todos los archivos estén committeados
git add .
git commit -m "Configuración lista para producción en Render"
git push origin main
```

#### 2. Crear Servicio en Render

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Click en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Configura el servicio:

**Configuración Básica:**
- **Name**: `tienda-backend-api`
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn Backend.wsgi:application`

**Variables de Entorno:**
```
PYTHON_VERSION=3.11.0
DJANGO_SETTINGS_MODULE=Backend.render_settings
WEB_CONCURRENCY=4
CLOUDINARY_CLOUD_NAME=do1ntnlop
CLOUDINARY_API_KEY=117225377115856
CLOUDINARY_API_SECRET=e0YSrk3sT_70-ijM6mwdFBIWP9w
DJANGO_CLOUDINARY_STORAGE=true
```

#### 3. Crear Base de Datos

1. En Render Dashboard, click en "New +" → "PostgreSQL"
2. Configura:
   - **Name**: `tienda-db`
   - **Database**: `tienda_production`
   - **User**: `tienda_user`
   - **Plan**: Free

#### 4. Conectar Base de Datos

1. En tu servicio web, ve a "Environment"
2. Agrega la variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Copia la URL de conexión de tu base de datos PostgreSQL

#### 5. Deploy

1. Click en "Create Web Service"
2. Render automáticamente:
   - Instalará dependencias
   - Ejecutará migraciones
   - Verificará configuración
   - Desplegará la aplicación

### 🔍 Verificaciones Automáticas

El build script ejecutará automáticamente:

1. **`check_deployment.py`** - Verificación general
2. **`fix_db_migrations.py`** - Arreglar migraciones
3. **`check_cloudinary_production.py`** - Verificar Cloudinary
4. **`check_production.py`** - Verificar configuración de producción

### ✅ Funcionalidades Verificadas:

- ✅ **Cloudinary**: Subida de imágenes automática
- ✅ **Base de Datos**: PostgreSQL configurado
- ✅ **API REST**: Endpoints funcionando
- ✅ **CORS**: Configurado para frontend
- ✅ **Storage**: Cloudinary como storage principal
- ✅ **Error Handling**: Sin errores 500
- ✅ **URLs**: Todas accesibles desde Cloudinary

### 🌐 URLs del Servicio:

- **API**: `https://tienda-backend-api.onrender.com`
- **Admin**: `https://tienda-backend-api.onrender.com/admin/`
- **API Docs**: `https://tienda-backend-api.onrender.com/api/`

### 📊 Monitoreo:

1. **Logs**: Ve a "Logs" en Render Dashboard
2. **Metrics**: Ve a "Metrics" para monitorear rendimiento
3. **Health Check**: El servicio se auto-reinicia si falla

### 🔧 Troubleshooting:

#### Si el deploy falla:

1. **Verificar logs**: Ve a "Logs" en Render
2. **Revisar variables de entorno**: Asegúrate de que estén configuradas
3. **Verificar build script**: Ejecuta `./build.sh` localmente
4. **Probar configuración**: Ejecuta `python check_production.py`

#### Si las imágenes no se suben:

1. **Verificar Cloudinary**: Ejecuta `python check_cloudinary_production.py`
2. **Revisar credenciales**: Asegúrate de que las variables de entorno estén correctas
3. **Verificar storage**: Ejecuta `python check_production.py`

### 🎉 ¡Listo para Producción!

Una vez desplegado, tu aplicación estará disponible en:
- **URL**: `https://tienda-backend-api.onrender.com`
- **Admin**: `https://tienda-backend-api.onrender.com/admin/`
- **API**: `https://tienda-backend-api.onrender.com/api/`

### 📱 Conectar Frontend:

Actualiza la URL de la API en tu frontend a:
```javascript
const API_URL = 'https://tienda-backend-api.onrender.com/api';
```

¡El sistema está completamente configurado para producción! 🚀 