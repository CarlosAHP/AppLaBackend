# Lab Esperanza - Backend API

Sistema de gestión de laboratorio clínico desarrollado con Flask y PostgreSQL.

## 🚀 Características

- **Gestión de Pacientes**: CRUD completo para pacientes
- **Resultados de Laboratorio**: Manejo de resultados y reportes
- **Sistema de Pagos**: Gestión de pagos y facturación
- **Autenticación JWT**: Sistema seguro de autenticación
- **Sincronización**: API para sincronización de datos
- **Reportes HTML**: Generación de reportes en formato HTML

## 🛠️ Tecnologías

- **Backend**: Python 3.8+, Flask, SQLAlchemy
- **Base de Datos**: PostgreSQL
- **Autenticación**: JWT (JSON Web Tokens)
- **Migraciones**: Flask-Migrate
- **Documentación**: API Documentation

## 📋 Requisitos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   # Copiar el archivo de ejemplo
   cp .env.example .env
   
   # Editar .env con tus credenciales
   nano .env
   ```

5. **Configurar base de datos**
   ```bash
   # Crear la base de datos en PostgreSQL
   createdb lab_esperanza
   
   # Ejecutar migraciones
   flask db upgrade
   ```

6. **Ejecutar la aplicación**
   ```bash
   python run.py
   ```

## 🔐 Configuración

### Variables de Entorno Principales

```env
# Configuración de la aplicación
SECRET_KEY=your-secret-key-here
DEBUG=False

# Configuración de base de datos
DATABASE_URL=postgresql://username:password@host:port/database_name

# Configuración de JWT
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### Configuración de Base de Datos

El sistema utiliza PostgreSQL como base de datos principal. Asegúrate de:

1. Tener PostgreSQL instalado y ejecutándose
2. Crear una base de datos para el proyecto
3. Configurar la URL de conexión en el archivo `.env`

## 📚 API Endpoints

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/logout` - Cerrar sesión
- `GET /api/auth/profile` - Obtener perfil de usuario

### Pacientes
- `GET /api/patients` - Listar pacientes
- `POST /api/patients` - Crear paciente
- `GET /api/patients/{id}` - Obtener paciente
- `PUT /api/patients/{id}` - Actualizar paciente
- `DELETE /api/patients/{id}` - Eliminar paciente

### Resultados de Laboratorio
- `GET /api/lab-results` - Listar resultados
- `POST /api/lab-results` - Crear resultado
- `GET /api/lab-results/{id}` - Obtener resultado
- `PUT /api/lab-results/{id}` - Actualizar resultado

### Reportes
- `GET /api/reports` - Listar reportes
- `POST /api/reports` - Crear reporte
- `GET /api/reports/{id}` - Obtener reporte
- `GET /api/reports/{id}/html` - Obtener reporte en HTML

### Pagos
- `GET /api/payments` - Listar pagos
- `POST /api/payments` - Crear pago
- `GET /api/payments/{id}` - Obtener pago

## 🏗️ Estructura del Proyecto

```
backend/
├── app/
│   ├── controllers/     # Controladores de la API
│   ├── models/          # Modelos de base de datos
│   ├── routes/          # Rutas de la API
│   ├── services/        # Lógica de negocio
│   ├── middleware/      # Middleware de autenticación
│   └── config.py        # Configuración de la aplicación
├── tests/               # Archivos de prueba
├── bocetos_pruebas/     # Plantillas HTML para reportes
├── reports/             # Reportes generados
├── static/              # Archivos estáticos
├── requirements.txt     # Dependencias de Python
├── run.py              # Punto de entrada de la aplicación
└── README.md           # Este archivo
```

## 🔒 Seguridad

- **Autenticación JWT**: Tokens seguros para autenticación
- **Variables de entorno**: Credenciales protegidas en archivos `.env`
- **CORS configurado**: Control de acceso desde diferentes orígenes
- **Validación de datos**: Validación de entrada en todos los endpoints

## 📝 Documentación

- [API de Autenticación](API_AUTH_DOCUMENTATION.md)
- [API de Pacientes](PATIENTS_API_DOCUMENTATION.md)
- [API de Reportes](REPORTS_API_DOCUMENTATION.md)

## 🚀 Despliegue

### Variables de Entorno para Producción

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
SESSION_COOKIE_SECURE=true
```

### Consideraciones de Producción

1. **Base de datos**: Usar una instancia de PostgreSQL en producción
2. **Secretos**: Cambiar todas las claves secretas
3. **HTTPS**: Configurar SSL/TLS en producción
4. **Logs**: Configurar logging apropiado
5. **Backup**: Implementar estrategia de respaldo

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas sobre el proyecto, contacta al equipo de desarrollo.

---

**Lab Esperanza** - Sistema de Gestión de Laboratorio Clínico