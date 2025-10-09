# 📥 Guía Frontend: Recibir Archivos HTML desde la API

## 🎯 **Objetivo**
Esta guía explica cómo el frontend puede recibir, mostrar y gestionar los archivos HTML guardados desde la API del backend.

## 📋 **Endpoints Disponibles para el Frontend**

### **1. 📥 Obtener Archivos Pendientes**
```javascript
GET /api/frontend-html/pending?limit=20
Headers: Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "filename": "frontend_reporte.html_20251009_004606_b16d77fe.html",
      "file_path": "frontend_html/2025/10/frontend_reporte.html_20251009_004606_b16d77fe.html",
      "size": 25182,
      "created_at": "2025-10-09T06:46:05.136Z",
      "metadata": {
        "patient_name": "Carlos Alfonso Hernández Pérez",
        "order_number": "005",
        "doctor_name": "MARIA SINAY",
        "patient_age": 22,
        "patient_gender": "F",
        "reception_date": "2025-10-09",
        "tests": [
          {
            "name": "heces_completa",
            "filename": "heces_completa.html"
          }
        ],
        "status": "pending",
        "created_at": "2025-10-09T06:46:05.136Z"
      }
    }
  ],
  "count": 1,
  "status": "pending",
  "message": "Se encontraron 1 archivos pendientes"
}
```

### **2. ✅ Obtener Archivos Completados**
```javascript
GET /api/frontend-html/completed?limit=20
Headers: Authorization: Bearer <token>
```

### **3. 📊 Obtener Estadísticas**
```javascript
GET /api/frontend-html/status-stats
Headers: Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "total_files": 1,
    "pending_count": 0,
    "completed_count": 1,
    "cancelled_count": 0,
    "by_status": {
      "pending": 0,
      "completed": 1,
      "cancelled": 0,
      "unknown": 0
    }
  }
}
```

### **4. 📄 Obtener Contenido HTML**
```javascript
GET /api/frontend-html/content/<filename>
Headers: Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "filename": "frontend_reporte.html_20251009_004606_b16d77fe.html",
    "html_content": "<html>...</html>",
    "metadata": {
      "patient_name": "Carlos Alfonso Hernández Pérez",
      "order_number": "005",
      "doctor_name": "MARIA SINAY",
      "status": "completed"
    }
  }
}
```

### **5. 🔄 Cambiar Estado de Archivo**
```javascript
PATCH /api/frontend-html/file/<filename>/status
Headers: Authorization: Bearer <token>
Body: {
  "status": "completed"
}
```

## 🚀 **Implementación en el Frontend**

### **📁 Estructura de Componentes Recomendada**

```
src/
├── components/
│   ├── HtmlFileList.jsx          # Lista de archivos
│   ├── HtmlFileCard.jsx         # Tarjeta individual
│   ├── HtmlFileViewer.jsx       # Visor de archivos
│   └── HtmlFileStatus.jsx       # Gestión de estados
├── services/
│   └── htmlFileService.js       # Servicio para API
└── pages/
    ├── PendingFiles.jsx         # Página archivos pendientes
    └── CompletedFiles.jsx      # Página archivos completados
```

### **🔧 Servicio para API (htmlFileService.js)**

```javascript
// src/services/htmlFileService.js
class HtmlFileService {
  constructor(baseURL = 'http://localhost:5000/api/frontend-html') {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('auth_token');
  }

  // Configurar headers con autenticación
  getHeaders() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.token}`
    };
  }

  // Obtener archivos pendientes
  async getPendingFiles(limit = 20) {
    try {
      const response = await fetch(`${this.baseURL}/pending?limit=${limit}`, {
        method: 'GET',
        headers: this.getHeaders()
      });
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error al obtener archivos pendientes:', error);
      throw error;
    }
  }

  // Obtener archivos completados
  async getCompletedFiles(limit = 20) {
    try {
      const response = await fetch(`${this.baseURL}/completed?limit=${limit}`, {
        method: 'GET',
        headers: this.getHeaders()
      });
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error al obtener archivos completados:', error);
      throw error;
    }
  }

  // Obtener estadísticas
  async getStatusStats() {
    try {
      const response = await fetch(`${this.baseURL}/status-stats`, {
        method: 'GET',
        headers: this.getHeaders()
      });
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error al obtener estadísticas:', error);
      throw error;
    }
  }

  // Obtener contenido HTML
  async getHtmlContent(filename) {
    try {
      const response = await fetch(`${this.baseURL}/content/${filename}`, {
        method: 'GET',
        headers: this.getHeaders()
      });
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error al obtener contenido HTML:', error);
      throw error;
    }
  }

  // Cambiar estado de archivo
  async updateFileStatus(filename, status) {
    try {
      const response = await fetch(`${this.baseURL}/file/${filename}/status`, {
        method: 'PATCH',
        headers: this.getHeaders(),
        body: JSON.stringify({ status })
      });
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error al cambiar estado:', error);
      throw error;
    }
  }

  // Obtener información de archivo
  async getFileInfo(filename) {
    try {
      const response = await fetch(`${this.baseURL}/info/${filename}`, {
        method: 'GET',
        headers: this.getHeaders()
      });
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error al obtener información del archivo:', error);
      throw error;
    }
  }
}

export default new HtmlFileService();
```

### **📋 Componente de Lista de Archivos (HtmlFileList.jsx)**

```jsx
// src/components/HtmlFileList.jsx
import React, { useState, useEffect } from 'react';
import HtmlFileCard from './HtmlFileCard';
import htmlFileService from '../services/htmlFileService';

const HtmlFileList = ({ status = 'pending', title = 'Archivos' }) => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadFiles();
    loadStats();
  }, [status]);

  const loadFiles = async () => {
    try {
      setLoading(true);
      setError(null);
      
      let response;
      if (status === 'pending') {
        response = await htmlFileService.getPendingFiles(20);
      } else if (status === 'completed') {
        response = await htmlFileService.getCompletedFiles(20);
      }
      
      if (response.success) {
        setFiles(response.data);
      } else {
        setError('Error al cargar archivos');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await htmlFileService.getStatusStats();
      if (response.success) {
        setStats(response.data);
      }
    } catch (err) {
      console.error('Error al cargar estadísticas:', err);
    }
  };

  const handleStatusChange = async (filename, newStatus) => {
    try {
      const response = await htmlFileService.updateFileStatus(filename, newStatus);
      if (response.success) {
        // Recargar archivos
        loadFiles();
        loadStats();
      }
    } catch (err) {
      console.error('Error al cambiar estado:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-2">Cargando archivos...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <strong>Error:</strong> {error}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header con estadísticas */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">{title}</h2>
        
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-blue-100 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{stats.total_files}</div>
              <div className="text-sm text-blue-800">Total Archivos</div>
            </div>
            <div className="bg-yellow-100 p-4 rounded-lg">
              <div className="text-2xl font-bold text-yellow-600">{stats.pending_count}</div>
              <div className="text-sm text-yellow-800">Pendientes</div>
            </div>
            <div className="bg-green-100 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{stats.completed_count}</div>
              <div className="text-sm text-green-800">Completados</div>
            </div>
            <div className="bg-red-100 p-4 rounded-lg">
              <div className="text-2xl font-bold text-red-600">{stats.cancelled_count}</div>
              <div className="text-sm text-red-800">Cancelados</div>
            </div>
          </div>
        )}
      </div>

      {/* Lista de archivos */}
      {files.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <div className="text-4xl mb-4">📄</div>
          <p>No hay archivos {status === 'pending' ? 'pendientes' : 'completados'}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {files.map((file, index) => (
            <HtmlFileCard
              key={index}
              file={file}
              onStatusChange={handleStatusChange}
              showStatusChange={status === 'pending'}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default HtmlFileList;
```

### **🃏 Componente de Tarjeta de Archivo (HtmlFileCard.jsx)**

```jsx
// src/components/HtmlFileCard.jsx
import React, { useState } from 'react';
import HtmlFileViewer from './HtmlFileViewer';

const HtmlFileCard = ({ file, onStatusChange, showStatusChange = false }) => {
  const [showViewer, setShowViewer] = useState(false);
  const [loading, setLoading] = useState(false);

  const metadata = file.metadata || {};
  const status = metadata.status || 'unknown';
  
  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending': return '⏳';
      case 'completed': return '✅';
      case 'cancelled': return '❌';
      default: return '❓';
    }
  };

  const handleStatusChange = async (newStatus) => {
    if (onStatusChange) {
      setLoading(true);
      try {
        await onStatusChange(file.filename, newStatus);
      } finally {
        setLoading(false);
      }
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return 'N/A';
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <>
      <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
        {/* Header con estado */}
        <div className="flex justify-between items-start mb-4">
          <div className="flex items-center space-x-2">
            <span className="text-2xl">{getStatusIcon(status)}</span>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(status)}`}>
              {status.toUpperCase()}
            </span>
          </div>
          <div className="text-xs text-gray-500">
            {formatFileSize(file.size)}
          </div>
        </div>

        {/* Información del paciente */}
        <div className="mb-4">
          <h3 className="font-semibold text-gray-800 mb-2">
            👤 {metadata.patient_name || 'Sin nombre'}
          </h3>
          <div className="space-y-1 text-sm text-gray-600">
            <p><strong>📋 Orden:</strong> {metadata.order_number || 'N/A'}</p>
            <p><strong>👨‍⚕️ Doctor:</strong> {metadata.doctor_name || 'N/A'}</p>
            <p><strong>👶 Edad:</strong> {metadata.patient_age || 'N/A'} años</p>
            <p><strong>⚥ Género:</strong> {metadata.patient_gender || 'N/A'}</p>
            <p><strong>📅 Fecha:</strong> {metadata.reception_date || 'N/A'}</p>
          </div>
        </div>

        {/* Tests */}
        {metadata.tests && metadata.tests.length > 0 && (
          <div className="mb-4">
            <h4 className="font-medium text-gray-700 mb-2">🧪 Pruebas:</h4>
            <div className="flex flex-wrap gap-1">
              {metadata.tests.map((test, index) => (
                <span key={index} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                  {test.name}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Fechas */}
        <div className="mb-4 text-xs text-gray-500">
          <p><strong>Creado:</strong> {formatDate(metadata.created_at)}</p>
          {metadata.completed_at && (
            <p><strong>Completado:</strong> {formatDate(metadata.completed_at)}</p>
          )}
        </div>

        {/* Botones de acción */}
        <div className="flex space-x-2">
          <button
            onClick={() => setShowViewer(true)}
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
          >
            👁️ Ver HTML
          </button>
          
          {showStatusChange && status === 'pending' && (
            <button
              onClick={() => handleStatusChange('completed')}
              disabled={loading}
              className="flex-1 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors disabled:opacity-50"
            >
              {loading ? '⏳' : '✅'} Completar
            </button>
          )}
        </div>
      </div>

      {/* Visor de archivos */}
      {showViewer && (
        <HtmlFileViewer
          file={file}
          onClose={() => setShowViewer(false)}
        />
      )}
    </>
  );
};

export default HtmlFileCard;
```

### **👁️ Componente Visor de Archivos (HtmlFileViewer.jsx)**

```jsx
// src/components/HtmlFileViewer.jsx
import React, { useState, useEffect } from 'react';
import htmlFileService from '../services/htmlFileService';

const HtmlFileViewer = ({ file, onClose }) => {
  const [htmlContent, setHtmlContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadHtmlContent();
  }, [file.filename]);

  const loadHtmlContent = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await htmlFileService.getHtmlContent(file.filename);
      if (response.success) {
        setHtmlContent(response.data.html_content);
      } else {
        setError('Error al cargar el contenido HTML');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePrint = () => {
    const printWindow = window.open('', '_blank');
    printWindow.document.write(htmlContent);
    printWindow.document.close();
    printWindow.print();
  };

  const handleDownload = () => {
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = file.filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-lg">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2">Cargando contenido HTML...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-lg max-w-md">
          <div className="text-red-600 mb-4">
            <div className="text-4xl mb-2">❌</div>
            <h3 className="text-lg font-semibold">Error</h3>
            <p>{error}</p>
          </div>
          <button
            onClick={onClose}
            className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
          >
            Cerrar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-6xl w-full h-5/6 flex flex-col">
        {/* Header */}
        <div className="flex justify-between items-center p-4 border-b">
          <div>
            <h3 className="text-lg font-semibold">📄 {file.filename}</h3>
            <p className="text-sm text-gray-600">
              👤 {file.metadata?.patient_name || 'Sin nombre'}
            </p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={handlePrint}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              🖨️ Imprimir
            </button>
            <button
              onClick={handleDownload}
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            >
              💾 Descargar
            </button>
            <button
              onClick={onClose}
              className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
            >
              ❌ Cerrar
            </button>
          </div>
        </div>

        {/* Contenido HTML */}
        <div className="flex-1 overflow-auto p-4">
          <div 
            className="w-full h-full"
            dangerouslySetInnerHTML={{ __html: htmlContent }}
          />
        </div>
      </div>
    </div>
  );
};

export default HtmlFileViewer;
```

### **📱 Páginas Principales**

#### **Página de Archivos Pendientes (PendingFiles.jsx)**

```jsx
// src/pages/PendingFiles.jsx
import React from 'react';
import HtmlFileList from '../components/HtmlFileList';

const PendingFiles = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          ⏳ Archivos Pendientes
        </h1>
        <p className="text-gray-600">
          Archivos HTML que requieren revisión y aprobación
        </p>
      </div>
      
      <HtmlFileList 
        status="pending" 
        title="Archivos Pendientes de Revisión"
      />
    </div>
  );
};

export default PendingFiles;
```

#### **Página de Archivos Completados (CompletedFiles.jsx)**

```jsx
// src/pages/CompletedFiles.jsx
import React from 'react';
import HtmlFileList from '../components/HtmlFileList';

const CompletedFiles = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          ✅ Archivos Completados
        </h1>
        <p className="text-gray-600">
          Archivos HTML que han sido revisados y aprobados
        </p>
      </div>
      
      <HtmlFileList 
        status="completed" 
        title="Archivos Completados"
      />
    </div>
  );
};

export default CompletedFiles;
```

## 🎯 **Flujo de Trabajo Recomendado**

### **1. 📥 Cargar Archivos Pendientes**
```javascript
// Al cargar la página
useEffect(() => {
  loadPendingFiles();
}, []);

const loadPendingFiles = async () => {
  try {
    const response = await htmlFileService.getPendingFiles(20);
    if (response.success) {
      setPendingFiles(response.data);
    }
  } catch (error) {
    console.error('Error al cargar archivos pendientes:', error);
  }
};
```

### **2. 🔄 Cambiar Estado de Archivo**
```javascript
const handleCompleteFile = async (filename) => {
  try {
    const response = await htmlFileService.updateFileStatus(filename, 'completed');
    if (response.success) {
      // Recargar lista
      loadPendingFiles();
      // Mostrar notificación
      showNotification('Archivo completado exitosamente', 'success');
    }
  } catch (error) {
    showNotification('Error al completar archivo', 'error');
  }
};
```

### **3. 👁️ Ver Contenido HTML**
```javascript
const handleViewFile = async (filename) => {
  try {
    const response = await htmlFileService.getHtmlContent(filename);
    if (response.success) {
      setHtmlContent(response.data.html_content);
      setShowViewer(true);
    }
  } catch (error) {
    console.error('Error al cargar contenido:', error);
  }
};
```

## 🎨 **Estilos CSS Recomendados**

```css
/* Estilos para las tarjetas de archivos */
.file-card {
  transition: all 0.3s ease;
}

.file-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

/* Estados de archivos */
.status-pending {
  background-color: #fef3c7;
  color: #92400e;
}

.status-completed {
  background-color: #d1fae5;
  color: #065f46;
}

.status-cancelled {
  background-color: #fee2e2;
  color: #991b1b;
}

/* Animaciones */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in {
  animation: fadeIn 0.5s ease-out;
}
```

## 🚀 **¡Implementación Lista!**

Con esta guía, el frontend puede:

- ✅ **Recibir archivos** desde la API
- ✅ **Mostrar archivos pendientes** y completados
- ✅ **Cambiar estados** de archivos
- ✅ **Ver contenido HTML** en modal
- ✅ **Imprimir y descargar** archivos
- ✅ **Mostrar estadísticas** en tiempo real
- ✅ **Gestionar estados** automáticamente

**¡El sistema está completamente funcional y listo para usar!** 🎉
