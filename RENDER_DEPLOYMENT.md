# 🚀 Deployment en Render

Esta guía te ayudará a desplegar el backend de la Tienda en Render.

## 📋 Pre-requisitos

- Cuenta en [Render](https://render.com/)
- Repositorio en GitHub con la rama `render-deploy`
- Variables de entorno configuradas

## 🔧 Configuración de Variables de Entorno en Render

### Variables Obligatorias:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `SECRET_KEY` | `tu-clave-secreta-aqui` | Clave secreta Django (generar nueva) |
| `RENDER` | `true` | Indica que está en producción |
| `DJANGO_SETTINGS_MODULE` | `Backend.settings` | Configuración Django |

### Variables Opcionales:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `CORS_ALLOWED_ORIGINS` | `https://tu-frontend.com` | URLs permitidas para CORS |
| `TIME_ZONE` | `America/Mexico_City` | Zona horaria |

## 🛠️ Pasos para Deployment

### 1️⃣ Crear Web Service en Render

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Clic en **"New +"** → **"Web Service"**
3. Conecta tu repositorio GitHub
4. Selecciona la rama `render-deploy`

### 2️⃣ Configurar el Service

```yaml
# Configuración básica
Name: tienda-backend-api
Runtime: Python 3
Region: Ohio (US East)
Branch: render-deploy

# Comandos
Build Command: ./build.sh
Start Command: gunicorn Backend.wsgi:application

# Plan
Plan: Free
```

### 3️⃣ Configurar Base de Datos PostgreSQL

1. En Render Dashboard → **"New +"** → **"PostgreSQL"**
2. Configurar:
   ```
   Name: tienda-db
   Database: tienda_production
   User: tienda_user
   Region: Ohio (US East)
   Plan: Free
   ```

### 4️⃣ Conectar Base de Datos

1. En el Web Service → **"Environment"**
2. Agregar variable `DATABASE_URL`:
   - Ir a la base de datos creada
   - Copiar la **"External Database URL"**
   - Pegarla como valor de `DATABASE_URL`

### 5️⃣ Variables de Entorno Completas

```env
# Básicas
SECRET_KEY=tu-clave-secreta-super-segura
RENDER=true
DJANGO_SETTINGS_MODULE=Backend.settings

# Base de datos (desde PostgreSQL service)
DATABASE_URL=postgres://user:pass@host:port/dbname

# CORS (ajustar según tu frontend)
CORS_ALLOWED_ORIGINS=https://tu-frontend.onrender.com

# Opcional
TIME_ZONE=America/Mexico_City
```

## 🎯 URLs de la API

Una vez desplegado, tu API estará disponible en:
```
https://tienda-backend-ap-api.onrender.com/
```

### Endpoints principales:
- `GET /api/productos/` - Listar productos
- `GET /api/categorias/` - Listar categorías  
- `POST /api/ventas/` - Procesar ventas
- `GET /admin/` - Panel de administración Django

## 🔍 Verificación del Deployment

### ✅ Checklist Post-Deployment:

- [ ] **API responde**: `https://tu-app.onrender.com/api/productos/`
- [ ] **Admin funciona**: `https://tu-app.onrender.com/admin/`
- [ ] **CORS configurado**: Frontend puede conectarse
- [ ] **Base de datos**: Migraciones aplicadas
- [ ] **Archivos estáticos**: CSS del admin se ve bien

### 🐛 Troubleshooting

#### Error 500 - Internal Server Error
```bash
# Verificar logs en Render Dashboard
# Posibles causas:
- SECRET_KEY no configurada
- DATABASE_URL incorrecta
- Migraciones no aplicadas
```

#### Error de CORS
```bash
# Verificar en variables de entorno:
CORS_ALLOWED_ORIGINS=https://tu-frontend.com
```

#### Build fallido
```bash
# Verificar que build.sh es ejecutable
# Verificar que requirements.txt es válido
```

## 🚀 Comandos Útiles

### Ejecutar migraciones manualmente:
```bash
# En Render Shell (si está disponible)
python manage.py migrate
```

### Crear superusuario:
```bash
python manage.py createsuperuser
```

### Recolectar archivos estáticos:
```bash
python manage.py collectstatic --noinput
```

## 📞 Soporte

Si tienes problemas:
1. Revisar logs en Render Dashboard
2. Verificar variables de entorno
3. Comprobar que la rama `render-deploy` tiene todos los archivos
4. Crear issue en el repositorio GitHub

---

🎉 **¡Tu API estará lista para producción!** 🎉 