# 🌐 API de Archivos HTML del Frontend - Documentación

## 🎯 Descripción General

Sistema completo para el manejo de archivos HTML generados y modificados desde el frontend, con almacenamiento organizado por fecha y sistema de backup automático.

## 📁 Estructura de Archivos

```
frontend_html/
├── 2024/
│   ├── 01/
│   │   ├── frontend_reporte_20240115_143022_abc12345.html
│   │   ├── frontend_reporte_20240115_143022_abc12345.html.meta
│   │   └── frontend_hemograma_20240115_150030_def67890.html
│   └── 02/
└── backups/
    └── frontend_html_backup_20240115.zip
```

## 🛠️ Endpoints de la API

### 1. Subir Archivo HTML
**POST** `/api/frontend-html/upload`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Body:**
```json
{
    "html_content": "<html><body><h1>Reporte de Laboratorio</h1></body></html>",
    "original_filename": "reporte.html",
    "patient_name": "Juan Pérez",
    "order_number": "ORD-001",
    "doctor_name": "Dr. García",
    "notes": "Notas adicionales",
    "prefix": "frontend"
}
```

**Respuesta:**
```json
{
    "success": true,
    "message": "Archivo HTML subido exitosamente",
    "data": {
        "filename": "frontend_reporte_20240115_143022_abc12345.html",
        "file_path": "/path/to/file.html",
        "size": 1024,
        "uploaded_at": "2024-01-15T14:30:22"
    }
}
```

### 2. Obtener Archivo HTML (Servir)
**GET** `/api/frontend-html/file/<filename>`

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:** Archivo HTML directamente (Content-Type: text/html)

### 3. Obtener Contenido HTML (JSON)
**GET** `/api/frontend-html/content/<filename>`

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
    "success": true,
    "data": {
        "filename": "reporte.html",
        "content": "<html>...</html>",
        "metadata": {
            "uploaded_at": "2024-01-15T14:30:22",
            "source": "frontend",
            "patient_name": "Juan Pérez",
            "order_number": "ORD-001"
        },
        "file_info": {
            "filename": "reporte.html",
            "file_path": "/path/to/file.html",
            "size": 1024,
            "created_at": "2024-01-15T14:30:22",
            "modified_at": "2024-01-15T14:30:22"
        }
    }
}
```

### 4. Listar Archivos HTML
**GET** `/api/frontend-html/list`

**Query Parameters:**
- `year`: Año a filtrar (opcional)
- `month`: Mes a filtrar (opcional)
- `limit`: Límite de resultados (default: 50, max: 200)

**Respuesta:**
```json
{
    "success": true,
    "data": [
        {
            "filename": "reporte.html",
            "file_path": "/path/to/file.html",
            "size": 1024,
            "created_at": "2024-01-15T14:30:22",
            "modified_at": "2024-01-15T14:30:22",
            "metadata": { ... }
        }
    ],
    "count": 1,
    "filters": {
        "year": null,
        "month": null,
        "limit": 50
    }
}
```

### 5. Actualizar Archivo HTML
**PUT** `/api/frontend-html/file/<filename>`

**Body:**
```json
{
    "html_content": "<html><body><h1>Reporte Actualizado</h1></body></html>",
    "patient_name": "Juan Pérez Actualizado",
    "notes": "Notas actualizadas"
}
```

**Respuesta:**
```json
{
    "success": true,
    "message": "Archivo reporte.html actualizado exitosamente",
    "data": {
        "filename": "reporte.html",
        "updated_at": "2024-01-15T15:30:22"
    }
}
```

### 6. Eliminar Archivo HTML
**DELETE** `/api/frontend-html/file/<filename>`

**Respuesta:**
```json
{
    "success": true,
    "message": "Archivo reporte.html eliminado exitosamente"
}
```

### 7. Obtener Información del Archivo
**GET** `/api/frontend-html/info/<filename>`

**Respuesta:**
```json
{
    "success": true,
    "data": {
        "file_info": {
            "filename": "reporte.html",
            "file_path": "/path/to/file.html",
            "size": 1024,
            "created_at": "2024-01-15T14:30:22",
            "modified_at": "2024-01-15T14:30:22"
        },
        "metadata": {
            "uploaded_at": "2024-01-15T14:30:22",
            "source": "frontend",
            "patient_name": "Juan Pérez",
            "order_number": "ORD-001"
        }
    }
}
```

### 8. Buscar Archivos HTML
**GET** `/api/frontend-html/search`

**Query Parameters:**
- `q`: Término de búsqueda general
- `patient_name`: Nombre del paciente
- `order_number`: Número de orden
- `doctor_name`: Nombre del doctor
- `limit`: Límite de resultados (default: 50, max: 200)

**Respuesta:**
```json
{
    "success": true,
    "data": [ ... ],
    "count": 5,
    "filters": {
        "search_term": "Juan",
        "patient_name": "",
        "order_number": "",
        "doctor_name": "",
        "limit": 50
    }
}
```

### 9. Crear Backup
**POST** `/api/frontend-html/backup`

**Query Parameters:**
- `date`: YYYY-MM-DD (opcional, default: hoy)

**Respuesta:**
```json
{
    "success": true,
    "message": "Backup creado exitosamente",
    "data": {
        "backup_path": "/path/to/backup.zip",
        "backup_date": "2024-01-15"
    }
}
```

### 10. Validar Sistema
**GET** `/api/frontend-html/system/validate`

**Respuesta:**
```json
{
    "success": true,
    "data": {
        "is_valid": true,
        "permissions": {
            "base_directory_exists": true,
            "base_directory_readable": true,
            "base_directory_writable": true,
            "sufficient_space": true,
            "free_space_bytes": 1073741824
        },
        "base_directory": "/path/to/frontend_html",
        "backup_enabled": true,
        "max_file_size": 5242880,
        "allowed_extensions": ["html", "htm"]
    }
}
```

### 11. Estadísticas
**GET** `/api/frontend-html/stats`

**Respuesta:**
```json
{
    "success": true,
    "data": {
        "total_files": 150,
        "total_size_bytes": 10485760,
        "files_by_year": {
            "2024": 100,
            "2023": 50
        },
        "files_by_month": {
            "01": 25,
            "02": 30
        },
        "recent_uploads": 10
    }
}
```

### 12. Archivos Recientes
**GET** `/api/frontend-html/recent`

**Query Parameters:**
- `limit`: Número de archivos (default: 10, max: 50)

**Respuesta:**
```json
{
    "success": true,
    "data": [ ... ],
    "count": 10
}
```

### 13. Descargar Archivo
**GET** `/api/frontend-html/download/<filename>`

**Respuesta:** Archivo HTML para descarga (Content-Disposition: attachment)

## 🔧 Configuración

### Variables de Entorno

```bash
# Configuración de archivos HTML del frontend
FRONTEND_HTML_FOLDER=frontend_html
FRONTEND_HTML_BASE_PATH=/path/to/frontend_html
FRONTEND_HTML_MAX_FILE_SIZE=5242880  # 5MB
FRONTEND_HTML_BACKUP_ENABLED=True
```

### Configuración en app/config.py

```python
# Configuración de archivos HTML del frontend
FRONTEND_HTML_FOLDER = os.environ.get('FRONTEND_HTML_FOLDER') or 'frontend_html'
FRONTEND_HTML_BASE_PATH = os.environ.get('FRONTEND_HTML_BASE_PATH') or os.path.join(os.getcwd(), 'frontend_html')
FRONTEND_HTML_MAX_FILE_SIZE = int(os.environ.get('FRONTEND_HTML_MAX_FILE_SIZE', 5 * 1024 * 1024))  # 5MB
FRONTEND_HTML_ALLOWED_EXTENSIONS = {'html', 'htm'}
FRONTEND_HTML_BACKUP_ENABLED = os.environ.get('FRONTEND_HTML_BACKUP_ENABLED', 'True').lower() == 'true'
```

## 📝 Ejemplos de Uso

### JavaScript (Frontend)

```javascript
// Subir archivo HTML
const uploadHTML = async (htmlContent, metadata) => {
    const response = await fetch('/api/frontend-html/upload', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            html_content: htmlContent,
            patient_name: metadata.patientName,
            order_number: metadata.orderNumber,
            doctor_name: metadata.doctorName,
            notes: metadata.notes
        })
    });
    
    return response.json();
};

// Obtener archivo HTML
const getHTMLFile = async (filename) => {
    const response = await fetch(`/api/frontend-html/file/${filename}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    return response.text(); // HTML content
};

// Listar archivos
const listHTMLFiles = async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await fetch(`/api/frontend-html/list?${params}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    return response.json();
};
```

### Python (Backend)

```python
from app.services.frontend_html_service import FrontendHTMLService
from app.config import Config

# Crear servicio
service = FrontendHTMLService(Config())

# Subir archivo HTML
html_content = "<html><body><h1>Reporte</h1></body></html>"
metadata = {
    "patient_name": "Juan Pérez",
    "order_number": "ORD-001"
}

file_path = service.create_directory_structure()
filename = service.generate_file_name("reporte.html", "frontend")
full_path = os.path.join(file_path, filename)

service.save_html_file(html_content, full_path, metadata)
```

## 🚀 Características

### ✅ Funcionalidades Implementadas

- **Subida de archivos HTML** desde el frontend
- **Almacenamiento organizado** por fecha (YYYY/MM/)
- **Metadatos automáticos** para cada archivo
- **Validación de contenido** HTML
- **Sistema de backup** automático
- **Búsqueda avanzada** por múltiples criterios
- **API REST completa** con 13 endpoints
- **Autenticación JWT** requerida
- **Manejo de errores** robusto
- **Logging detallado** para debugging

### 🔒 Seguridad

- **Validación de rutas** para prevenir directory traversal
- **Límites de tamaño** de archivo configurable
- **Autenticación requerida** para todos los endpoints
- **Validación de contenido** HTML básica
- **Limpieza de nombres** de archivo

### 📊 Monitoreo

- **Estadísticas detalladas** de uso
- **Validación del sistema** de archivos
- **Logging de operaciones** importantes
- **Métricas de rendimiento**

## 🎯 Casos de Uso

1. **Editor HTML del Frontend**: Los usuarios pueden crear y modificar reportes HTML
2. **Almacenamiento Temporal**: Guardar borradores de reportes
3. **Plantillas Personalizadas**: Crear plantillas HTML personalizadas
4. **Backup y Recuperación**: Sistema automático de respaldos
5. **Búsqueda de Archivos**: Encontrar reportes por paciente, doctor, etc.
6. **Integración con Sistema Principal**: Conectar con el sistema de reportes principal

## 🔄 Flujo de Trabajo Recomendado

1. **Frontend** crea/modifica HTML
2. **Subir** archivo HTML via `/api/frontend-html/upload`
3. **Sistema** organiza por fecha automáticamente
4. **Metadatos** se guardan junto al archivo
5. **Backup** automático según configuración
6. **Búsqueda** y recuperación cuando sea necesario
7. **Integración** con sistema de reportes principal

## 📈 Escalabilidad

- **Organización por fecha** para mejor rendimiento
- **Límites configurables** de tamaño y cantidad
- **Sistema de backup** para recuperación
- **API REST** estándar para integración
- **Logging detallado** para monitoreo
