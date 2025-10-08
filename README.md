# 🧪 Lab Esperanza - Sistema de Gestión de Laboratorio Clínico

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=for-the-badge&logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue?style=for-the-badge&logo=postgresql)
![JWT](https://img.shields.io/badge/JWT-Auth-orange?style=for-the-badge&logo=jsonwebtokens)

**Sistema integral de gestión para laboratorios clínicos con API REST moderna**

[![API Documentation](https://img.shields.io/badge/API-Documentation-purple?style=for-the-badge)](./API_AUTH_DOCUMENTATION.md)
[![Patients API](https://img.shields.io/badge/Patients-API-green?style=for-the-badge)](./PATIENTS_API_DOCUMENTATION.md)
[![Reports API](https://img.shields.io/badge/Reports-API-red?style=for-the-badge)](./REPORTS_API_DOCUMENTATION.md)

</div>

## ✨ Características Principales

### 🔐 **Seguridad Avanzada**
- Autenticación JWT con tokens seguros
- Middleware de autorización por roles
- Validación de datos de entrada
- Protección contra ataques comunes

### 👥 **Gestión de Pacientes**
- Registro completo de pacientes
- Historial médico integrado
- Búsqueda avanzada y filtros
- Exportación de datos

### 🧬 **Resultados de Laboratorio**
- Procesamiento de resultados automatizado
- Plantillas HTML personalizables
- Generación de reportes profesionales
- Integración con equipos de laboratorio

### 💰 **Sistema de Pagos**
- Gestión de facturación
- Seguimiento de pagos
- Reportes financieros
- Integración con sistemas de pago

### 📊 **Reportes Inteligentes**
- Más de 200 plantillas de reportes
- Generación automática de PDFs
- Personalización de formatos
- Exportación en múltiples formatos

### 🔄 **Sincronización de Datos**
- API REST completa
- Sincronización en tiempo real
- Backup automático
- Recuperación de datos

## 🚀 Inicio Rápido

### 📋 Prerrequisitos

| Tecnología | Versión | Descripción |
|------------|----------|-------------|
| 🐍 **Python** | 3.8+ | Lenguaje de programación |
| 🐘 **PostgreSQL** | 12+ | Base de datos principal |
| 📦 **pip** | Latest | Gestor de paquetes |

### ⚡ Instalación en 5 pasos

```bash
# 1️⃣ Clonar el repositorio
git clone https://github.com/tu-usuario/lab-esperanza-backend.git
cd lab-esperanza-backend

# 2️⃣ Crear entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3️⃣ Instalar dependencias
pip install -r requirements.txt

# 4️⃣ Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 5️⃣ Iniciar la aplicación
python run.py
```

### 🎯 Configuración de Base de Datos

```bash
# Crear base de datos
createdb lab_esperanza

# Ejecutar migraciones
flask db upgrade

# Verificar conexión
python -c "from database import test_connection; test_connection()"
```

## ⚙️ Configuración

### 🔧 Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de la aplicación | `your-secret-key-here` |
| `DATABASE_URL` | URL de conexión a PostgreSQL | `postgresql://user:pass@host:port/db` |
| `JWT_SECRET_KEY` | Clave para tokens JWT | `your-jwt-secret-key` |
| `DEBUG` | Modo de desarrollo | `False` |

### 🗄️ Base de Datos

El sistema utiliza **PostgreSQL** como base de datos principal:

```bash
# Instalar PostgreSQL (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib

# Crear base de datos
sudo -u postgres createdb lab_esperanza

# Crear usuario (opcional)
sudo -u postgres createuser --interactive
```

## 📚 API Endpoints

### 🔐 Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/auth/login` | Iniciar sesión |
| `POST` | `/api/auth/register` | Registrar usuario |
| `POST` | `/api/auth/logout` | Cerrar sesión |
| `GET` | `/api/auth/profile` | Obtener perfil |

### 👥 Pacientes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/patients` | Listar pacientes |
| `POST` | `/api/patients` | Crear paciente |
| `GET` | `/api/patients/{id}` | Obtener paciente |
| `PUT` | `/api/patients/{id}` | Actualizar paciente |
| `DELETE` | `/api/patients/{id}` | Eliminar paciente |

### 🧬 Resultados de Laboratorio
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/lab-results` | Listar resultados |
| `POST` | `/api/lab-results` | Crear resultado |
| `GET` | `/api/lab-results/{id}` | Obtener resultado |
| `PUT` | `/api/lab-results/{id}` | Actualizar resultado |

### 📊 Reportes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/reports` | Listar reportes |
| `POST` | `/api/reports` | Crear reporte |
| `GET` | `/api/reports/{id}` | Obtener reporte |
| `GET` | `/api/reports/{id}/html` | Reporte en HTML |

### 💰 Pagos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/payments` | Listar pagos |
| `POST` | `/api/payments` | Crear pago |
| `GET` | `/api/payments/{id}` | Obtener pago |

## 🏗️ Arquitectura del Proyecto

```
📁 lab-esperanza-backend/
├── 🐍 app/                          # Aplicación principal
│   ├── 🎮 controllers/              # Controladores de la API
│   ├── 🗃️ models/                   # Modelos de base de datos
│   ├── 🛣️ routes/                   # Rutas de la API
│   ├── ⚙️ services/                  # Lógica de negocio
│   ├── 🔒 middleware/                # Middleware de autenticación
│   └── ⚙️ config.py                  # Configuración
├── 📊 bocetos_pruebas/              # Plantillas HTML (200+ reportes)
├── 📁 reports/                      # Reportes generados
├── 🖼️ static/                       # Archivos estáticos
├── 📋 requirements.txt              # Dependencias
├── 🚀 run.py                        # Punto de entrada
└── 📖 README.md                     # Documentación
```

## 🔒 Seguridad Implementada

| Característica | Descripción |
|----------------|--------------|
| 🔐 **JWT Authentication** | Tokens seguros con expiración |
| 🛡️ **Middleware Protection** | Autorización por roles |
| 🔒 **Environment Variables** | Credenciales protegidas |
| 🌐 **CORS Configuration** | Control de acceso por origen |
| ✅ **Input Validation** | Validación de datos de entrada |

## 📚 Documentación Completa

| Documento | Descripción |
|-----------|-------------|
| [🔐 API de Autenticación](./API_AUTH_DOCUMENTATION.md) | Endpoints de login, registro y perfil |
| [👥 API de Pacientes](./PATIENTS_API_DOCUMENTATION.md) | Gestión completa de pacientes |
| [📊 API de Reportes](./REPORTS_API_DOCUMENTATION.md) | Generación y gestión de reportes |

## 🚀 Despliegue en Producción

### 🐳 Docker (Recomendado)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

### ☁️ Variables de Entorno para Producción

```env
# 🔐 Seguridad
SECRET_KEY=your-super-secret-production-key
JWT_SECRET_KEY=your-jwt-production-key

# 🗄️ Base de Datos
DATABASE_URL=postgresql://user:password@host:port/database

# 🌐 Configuración
DEBUG=False
SESSION_COOKIE_SECURE=true
CORS_ORIGINS=https://yourdomain.com
```

### 🏗️ Consideraciones de Producción

- ✅ **Base de datos**: PostgreSQL en producción
- ✅ **HTTPS**: SSL/TLS configurado
- ✅ **Logging**: Sistema de logs implementado
- ✅ **Backup**: Estrategia de respaldo automático
- ✅ **Monitoring**: Monitoreo de rendimiento

## 🤝 Contribuir al Proyecto

### 🚀 Flujo de Contribución

```bash
# 1️⃣ Fork del repositorio
# 2️⃣ Clonar tu fork
git clone https://github.com/tu-usuario/lab-esperanza-backend.git

# 3️⃣ Crear rama de feature
git checkout -b feature/nueva-funcionalidad

# 4️⃣ Hacer cambios y commit
git add .
git commit -m "feat: agregar nueva funcionalidad"

# 5️⃣ Push y crear Pull Request
git push origin feature/nueva-funcionalidad
```

### 📋 Estándares de Código

- **Python**: PEP 8
- **Commits**: Conventional Commits
- **Documentación**: Docstrings en funciones
- **Testing**: Cobertura mínima del 80%

## 📊 Estadísticas del Proyecto

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/tu-usuario/lab-esperanza-backend?style=social)
![GitHub forks](https://img.shields.io/github/forks/tu-usuario/lab-esperanza-backend?style=social)
![GitHub issues](https://img.shields.io/github/issues/tu-usuario/lab-esperanza-backend)
![GitHub pull requests](https://img.shields.io/github/issues-pr/tu-usuario/lab-esperanza-backend)

</div>

## 📞 Soporte y Contacto

| Canal | Descripción |
|-------|-------------|
| 🐛 **Issues** | Reportar bugs y solicitar features |
| 💬 **Discussions** | Preguntas y discusiones generales |
| 📧 **Email** | Soporte técnico directo |
| 📖 **Wiki** | Documentación adicional |

---

<div align="center">

**🧪 Lab Esperanza** - Sistema de Gestión de Laboratorio Clínico

*Desarrollado con ❤️ para mejorar la gestión de laboratorios clínicos*

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=python)](https://python.org)
[![Powered by Flask](https://img.shields.io/badge/Powered%20by-Flask-green?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)

</div>