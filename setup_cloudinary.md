# 🚀 Configuración Completa de Cloudinary para Render

## 📋 Resumen del Problema
- Render no persiste archivos en el sistema de archivos
- Las imágenes se suben pero se pierden al reiniciar el contenedor
- URLs `/media/` devuelven 404 en producción

## ✅ Solución: Cloudinary
Cloudinary es un servicio de almacenamiento en la nube que soluciona este problema.

---

## 🔧 Pasos para Configurar Cloudinary

### **Paso 1: Crear cuenta en Cloudinary**
1. Ve a https://cloudinary.com/
2. Haz clic en **"Sign Up For Free"**
3. Completa el registro con tu email
4. Verifica tu cuenta por email

### **Paso 2: Obtener credenciales**
1. Inicia sesión en Cloudinary
2. En el **Dashboard**, anota tu **Cloud Name** (parte superior)
3. Ve a **Settings > Access Keys**
4. Copia tu **API Key** y **API Secret**

### **Paso 3: Configurar variables en Render**
1. Ve a tu dashboard de Render
2. Selecciona tu servicio `tienda-backend-api`
3. Ve a **Settings > Environment Variables**
4. Agrega estas 3 variables:

```
CLOUDINARY_CLOUD_NAME=do1ntnlop
CLOUDINARY_API_KEY=117225377115856
CLOUDINARY_API_SECRET=e0YSrk3sT_70-ijM6mwdFBIWP9w
```

### **Paso 4: Redesplegar**
1. Guarda las variables de entorno
2. Render redesplegará automáticamente
3. Espera a que termine el despliegue

### **Paso 5: Verificar configuración**
1. Ve a tu servicio en Render
2. **Logs > Build Logs**
3. Verifica que no hay errores de instalación

---

## 🧪 Scripts de Prueba

### **Probar configuración local:**
```bash
cd Backend
python test_cloudinary.py
```

### **Probar subida de imágenes:**
```bash
cd Backend
python test_image_upload.py
```

### **Migrar imágenes existentes (solo en producción):**
```bash
# En Render, ejecutar en la consola:
python migrate_images_to_cloudinary.py
```

---

## 🔍 Verificación

### **Antes de Cloudinary:**
- ❌ Imágenes se pierden al reiniciar
- ❌ URLs `/media/` devuelven 404
- ❌ No hay persistencia de archivos

### **Después de Cloudinary:**
- ✅ Imágenes se guardan en la nube
- ✅ URLs de Cloudinary funcionan
- ✅ CDN global para mejor performance
- ✅ Optimización automática de imágenes

---

## 📝 URLs de ejemplo

### **Antes:**
```
https://tienda-backend-ap-api.onrender.com/media/productos/imagen.jpg
```

### **Después:**
```
https://res.cloudinary.com/do1ntnlop/image/upload/v1234567890/productos/imagen.jpg
```

---

## ⚠️ Notas importantes

1. **Las imágenes existentes** no se migrarán automáticamente
2. **Solo las nuevas imágenes** se subirán a Cloudinary
3. **El plan gratuito** de Cloudinary incluye:
   - 25 GB de almacenamiento
   - 25 GB de ancho de banda mensual
   - Transformaciones de imagen ilimitadas

4. **Para migrar imágenes existentes**, usa el script `migrate_images_to_cloudinary.py`

---

## 🆘 Solución de problemas

### **Error: "Module not found"**
```bash
pip install django-cloudinary-storage
```

### **Error: "Invalid credentials"**
- Verifica que las variables de entorno estén correctas
- Asegúrate de que no hay espacios extra

### **Error: "Upload failed"**
- Verifica que tienes espacio en tu plan gratuito
- Revisa los logs de Render para más detalles

---

## 🎉 ¡Listo!

Una vez configurado, las imágenes se subirán automáticamente a Cloudinary y serán accesibles desde URLs de Cloudinary con CDN global. 