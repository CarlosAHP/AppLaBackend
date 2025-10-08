# Configuración para GitHub

## Pasos para subir el proyecto a GitHub

### 1. Crear repositorio en GitHub
1. Ve a [GitHub.com](https://github.com)
2. Haz clic en "New repository"
3. Nombre del repositorio: `lab-esperanza-backend`
4. Descripción: "Sistema de gestión de laboratorio clínico - Backend API"
5. Marca como **Privado** (recomendado para proyectos con datos sensibles)
6. **NO** inicialices con README, .gitignore o licencia (ya los tenemos)
7. Haz clic en "Create repository"

### 2. Conectar repositorio local con GitHub

```bash
# Agregar el repositorio remoto (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/lab-esperanza-backend.git

# Verificar que se agregó correctamente
git remote -v

# Subir el código a GitHub
git push -u origin master
```

### 3. Configuración adicional recomendada

#### Variables de entorno en GitHub (para despliegue)
Si planeas usar GitHub Actions o desplegar en la nube:

1. Ve a Settings > Secrets and variables > Actions
2. Agrega las siguientes variables:
   - `DATABASE_URL`: Tu URL de base de datos de producción
   - `SECRET_KEY`: Tu clave secreta de producción
   - `JWT_SECRET_KEY`: Tu clave JWT de producción

#### Protección de rama principal
1. Ve a Settings > Branches
2. Agrega una regla para la rama `master`
3. Marca "Require pull request reviews before merging"
4. Marca "Require status checks to pass before merging"

### 4. Comandos útiles para el desarrollo

```bash
# Ver el estado del repositorio
git status

# Agregar cambios
git add .

# Hacer commit
git commit -m "Descripción del cambio"

# Subir cambios
git push

# Descargar cambios
git pull

# Ver historial de commits
git log --oneline
```

### 5. Estructura del proyecto en GitHub

El repositorio incluye:
- ✅ Código fuente de la API
- ✅ Documentación completa
- ✅ Plantillas HTML para reportes
- ✅ Configuración de seguridad (.gitignore)
- ✅ Archivo de ejemplo para variables de entorno
- ❌ Archivos de testing (excluidos)
- ❌ Archivos Word (excluidos)
- ❌ Variables de entorno reales (protegidas)

### 6. Próximos pasos recomendados

1. **Configurar CI/CD**: GitHub Actions para testing automático
2. **Documentación**: Mantener actualizada la documentación de la API
3. **Seguridad**: Revisar regularmente las dependencias
4. **Backup**: Configurar respaldos automáticos de la base de datos
5. **Monitoreo**: Implementar logging y monitoreo en producción

## Notas importantes

- **NUNCA** subas el archivo `.env` con credenciales reales
- Usa el archivo `.env.example` como plantilla
- Mantén las credenciales de producción en variables de entorno del servidor
- Revisa regularmente el `.gitignore` para asegurar que no se suban archivos sensibles
