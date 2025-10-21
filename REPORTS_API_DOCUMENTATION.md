# 📋 API de Reportes de Laboratorio - Documentación

## 🎯 Descripción General

Sistema completo para el almacenamiento y gestión de reportes HTML de laboratorio con base de datos PostgreSQL y sistema de archivos organizados por fecha.

## 🗄️ Estructura de Base de Datos

### Tabla `lab_reports`
```sql
CREATE TABLE lab_reports (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    patient_name VARCHAR(255) NOT NULL,
    patient_age INTEGER,
    patient_gender VARCHAR(1) CHECK (patient_gender IN ('M', 'F')),
    doctor_name VARCHAR(255),
    reception_date DATE,
    file_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    selected_tests JSONB,
    html_content TEXT,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'final', 'printed')),
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### Tabla `report_tests`
```sql
CREATE TABLE report_tests (
    id SERIAL PRIMARY KEY,
    report_id INTEGER NOT NULL,
    test_name VARCHAR(255) NOT NULL,
    test_filename VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES lab_reports(id) ON DELETE CASCADE
);
```

## 🛠️ Endpoints de la API

### 1. Crear Reporte
**POST** `/api/reports`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Body:**
```json
{
    "order_number": "ORD-001",
    "patient_name": "Juan Pérez",
    "patient_age": 35,
    "patient_gender": "M",
    "doctor_name": "Dr. García",
    "reception_date": "2024-01-15",
    "html_content": "<html>...</html>",
    "selected_tests": [
        {
            "name": "Hemograma Completo",
            "filename": "hematologia.html"
        }
    ],
    "status": "draft"
}
```

**Respuesta:**
```json
{
    "success": true,
    "message": "Reporte creado exitosamente",
    "data": {
        "id": 1,
        "order_number": "ORD-001",
        "patient_name": "Juan Pérez",
        "file_path": "/path/to/reports/2024/01/ORD-001_Juan_Perez_20240115_143022.html",
        "file_name": "ORD-001_Juan_Perez_20240115_143022.html",
        "status": "draft",
        "created_at": "2024-01-15T14:30:22"
    }
}
```

### 2. Obtener Reporte
**GET** `/api/reports/{id}`

**Query Parameters:**
- `include_html`: true/false (default: true)

**Respuesta:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "order_number": "ORD-001",
        "patient_name": "Juan Pérez",
        "html_content": "<html>...</html>",
        "status": "draft"
    }
}
```

### 3. Actualizar Reporte
**PUT** `/api/reports/{id}`

**Body:**
```json
{
    "patient_name": "Juan Pérez Actualizado",
    "status": "final",
    "html_content": "<html>...</html>"
}
```

### 4. Eliminar Reporte
**DELETE** `/api/reports/{id}`

**Respuesta:**
```json
{
    "success": true,
    "message": "Reporte eliminado exitosamente"
}
```

### 5. Buscar por Paciente
**GET** `/api/reports/patient/{patient_name}`

**Query Parameters:**
- `limit`: número máximo de resultados (default: 50, max: 100)
- `include_html`: true/false (default: false)

### 6. Buscar por Rango de Fechas
**GET** `/api/reports/date-range`

**Query Parameters:**
- `start_date`: YYYY-MM-DD (required)
- `end_date`: YYYY-MM-DD (required)
- `include_html`: true/false (default: false)

### 7. Estadísticas
**GET** `/api/reports/stats`

**Respuesta:**
```json
{
    "success": true,
    "data": {
        "reports": {
            "total_reports": 150,
            "unique_patients": 120,
            "unique_doctors": 15,
            "draft_reports": 25,
            "final_reports": 100,
            "printed_reports": 25
        },
        "system": {
            "permissions": {
                "base_directory_exists": true,
                "base_directory_readable": true,
                "base_directory_writable": true,
                "sufficient_space": true,
                "free_space_bytes": 1073741824
            },
            "backup_enabled": true,
            "max_file_size": 10485760
        }
    }
}
```

### 8. Validar Sistema
**GET** `/api/reports/system/validate`

### 9. Crear Backup
**POST** `/api/reports/backup`

**Query Parameters:**
- `date`: YYYY-MM-DD (opcional, default: hoy)

### 10. Limpiar Backups
**DELETE** `/api/reports/backup/cleanup`

## 📁 Estructura de Archivos

```
reports/
├── 2024/
│   ├── 01/
│   │   ├── ORD-001_Juan_Perez_20240115_143022.html
│   │   └── ORD-002_Maria_Garcia_20240115_150030.html
│   └── 02/
│       └── ORD-003_Carlos_Lopez_20240201_090015.html
└── backups/
    ├── reports_backup_20240115.zip
    └── reports_backup_20240116.zip
```

## ⚙️ Configuración

### Variables de Entorno
```bash
# Configuración de reportes
REPORTS_FOLDER=reports
REPORTS_BASE_PATH=/path/to/reports
REPORTS_BACKUP_ENABLED=True
REPORTS_BACKUP_RETENTION_DAYS=730
REPORTS_MAX_FILE_SIZE=10485760
```

### Configuración en `app/config.py`
```python
# Configuración de reportes HTML
REPORTS_FOLDER = os.environ.get('REPORTS_FOLDER') or 'reports'
REPORTS_BASE_PATH = os.environ.get('REPORTS_BASE_PATH') or os.path.join(os.getcwd(), 'reports')
REPORTS_BACKUP_ENABLED = os.environ.get('REPORTS_BACKUP_ENABLED', 'True').lower() == 'true'
REPORTS_BACKUP_RETENTION_DAYS = int(os.environ.get('REPORTS_BACKUP_RETENTION_DAYS', 730))
REPORTS_MAX_FILE_SIZE = int(os.environ.get('REPORTS_MAX_FILE_SIZE', 10 * 1024 * 1024))
```

## 🔒 Validaciones

### Validaciones de Entrada
- `order_number`: Requerido, único, formato válido
- `patient_name`: Requerido, mínimo 2 caracteres
- `patient_age`: Opcional, entre 0-150
- `patient_gender`: Opcional, solo 'M' o 'F'
- `html_content`: Requerido, contenido HTML válido
- `selected_tests`: Requerido, array no vacío

### Validaciones de Archivo
- Verificar que el directorio de destino existe
- Verificar permisos de escritura
- Verificar espacio disponible en disco
- Validar nombre de archivo (sin caracteres especiales)

## 🚨 Códigos de Error

| Código | Descripción |
|--------|-------------|
| `VALIDATION_ERROR` | Datos de entrada inválidos |
| `FILE_SAVE_ERROR` | Error al guardar archivo |
| `DATABASE_ERROR` | Error en base de datos |
| `PERMISSION_ERROR` | Sin permisos para escribir archivos |
| `NOT_FOUND` | Reporte no encontrado |
| `AUTHENTICATION_ERROR` | Usuario no autenticado |
| `INTERNAL_ERROR` | Error interno del servidor |

## 🔧 Funciones del Servicio

### `LabReportService`

#### Métodos Principales
- `create_report(data, created_by)`: Crear nuevo reporte
- `update_report(report_id, data)`: Actualizar reporte existente
- `get_report(report_id, include_html)`: Obtener reporte por ID
- `delete_report(report_id)`: Eliminar reporte
- `get_reports_by_patient(patient_name, limit)`: Buscar por paciente
- `get_reports_by_date_range(start_date, end_date)`: Buscar por fechas
- `get_reports_stats()`: Obtener estadísticas

#### Funciones de Archivo
- `create_directory_structure(year, month)`: Crear estructura de directorios
- `generate_file_name(order_number, patient_name, timestamp)`: Generar nombre único
- `save_report_file(html_content, file_path)`: Guardar archivo HTML
- `backup_reports(backup_date)`: Crear backup
- `cleanup_old_backups()`: Limpiar backups antiguos
- `validate_file_permissions()`: Validar permisos

## 🧪 Pruebas

### Scripts de Prueba
1. `create_reports_tables.py`: Crear tablas de base de datos
2. `test_reports_simple.py`: Prueba básica del sistema
3. `test_reports_system.py`: Prueba completa de todos los endpoints

### Ejecutar Pruebas
```bash
# Crear tablas
python create_reports_tables.py

# Probar sistema básico
python test_reports_simple.py

# Probar sistema completo (requiere servidor corriendo)
python test_reports_system.py
```

## 🚀 Instalación y Uso

### 1. Crear Tablas
```bash
python create_reports_tables.py
```

### 2. Iniciar Servidor
```bash
python run.py
```

### 3. Probar Sistema
```bash
python test_reports_simple.py
```

## 📊 Características

### ✅ Implementado
- ✅ Base de datos con tablas `lab_reports` y `report_tests`
- ✅ Modelo `LabReport` con validaciones completas
- ✅ Servicio `LabReportService` con funciones de archivo
- ✅ Controlador con todos los endpoints requeridos
- ✅ Rutas configuradas con autenticación
- ✅ Sistema de archivos organizado por fecha
- ✅ Validaciones de entrada y archivo
- ✅ Manejo de errores apropiado
- ✅ Sistema de backup automático
- ✅ Logging y auditoría
- ✅ Seguridad y autenticación

### 🔄 Funcionalidades Adicionales
- Búsqueda avanzada de reportes
- Reportes recientes
- Información de archivos
- Validación del sistema
- Limpieza automática de backups
- Estadísticas detalladas

## 🎯 Resumen

El sistema de reportes está completamente implementado y listo para usar. Incluye:

1. **Base de datos** con tablas optimizadas e índices
2. **API REST** completa con todos los endpoints requeridos
3. **Sistema de archivos** organizado por fecha
4. **Validaciones** robustas de entrada y archivo
5. **Backup automático** con limpieza de archivos antiguos
6. **Seguridad** con autenticación JWT
7. **Logging** y manejo de errores
8. **Pruebas** automatizadas

El sistema está diseñado para ser escalable, seguro y fácil de mantener.
















