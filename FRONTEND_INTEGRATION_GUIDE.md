# 🖥️ Guía de Integración Frontend - Sistema de Estados

## 🎯 **Resumen de la Implementación**

El sistema de estados está completamente implementado y funcionando. Las pruebas muestran que:

- ✅ **4 archivos** en el sistema
- ✅ **3 archivos pendientes** (ordenados por fecha de creación)
- ✅ **1 archivo completado** (en el historial)
- ✅ **Estados funcionando** correctamente
- ✅ **API endpoints** operativos

## 📋 **Endpoints Principales para el Frontend**

### **1. Obtener Archivos Pendientes (Para la Interfaz Principal)**
```javascript
// GET /api/frontend-html/pending
async function getPendingFiles() {
    const response = await fetch('/api/frontend-html/pending?limit=20', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const result = await response.json();
    
    // result.data contiene los archivos pendientes ordenados por fecha
    return result.data;
}
```

**Respuesta JSON:**
```json
{
  "success": true,
  "data": [
    {
      "filename": "frontend_reporte_1_20251008_234506_c3ffac5a.html",
      "size": 962,
      "created_at": "2025-10-08T23:45:06.577830",
      "metadata": {
        "patient_name": "Carlos Alfonso Hernández Pérez",
        "order_number": "005",
        "doctor_name": "Dr. García",
        "status": "pending",
        "created_at": "2025-10-08T23:45:06.579512"
      }
    }
  ],
  "count": 3,
  "status": "pending",
  "message": "Se encontraron 3 archivos pendientes"
}
```

### **2. Obtener Estadísticas (Para el Dashboard)**
```javascript
// GET /api/frontend-html/status-stats
async function getStatusStats() {
    const response = await fetch('/api/frontend-html/status-stats', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const result = await response.json();
    
    return result.data;
}
```

**Respuesta JSON:**
```json
{
  "success": true,
  "data": {
    "total_files": 4,
    "pending_count": 3,
    "completed_count": 1,
    "cancelled_count": 0,
    "by_status": {
      "pending": 3,
      "completed": 1,
      "cancelled": 0,
      "unknown": 0
    }
  }
}
```

### **3. Obtener Archivos Completados (Para el Historial)**
```javascript
// GET /api/frontend-html/completed
async function getCompletedFiles() {
    const response = await fetch('/api/frontend-html/completed?limit=20', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const result = await response.json();
    
    return result.data;
}
```

### **4. Actualizar Estado de Archivo**
```javascript
// PATCH /api/frontend-html/file/<filename>/status
async function updateFileStatus(filename, newStatus) {
    const response = await fetch(`/api/frontend-html/file/${filename}/status`, {
        method: 'PATCH',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: newStatus })
    });
    
    const result = await response.json();
    return result;
}
```

## 🖥️ **Implementación en el Frontend**

### **Estructura HTML para Archivos Pendientes:**
```html
<!-- Sección de archivos pendientes -->
<div class="pending-files-section">
    <h3>📋 Archivos Pendientes</h3>
    <div id="pending-files-list">
        <!-- Los archivos se cargarán aquí dinámicamente -->
    </div>
</div>
```

### **JavaScript para Cargar y Mostrar Archivos Pendientes:**
```javascript
async function loadPendingFiles() {
    try {
        const pendingFiles = await getPendingFiles();
        const container = document.getElementById('pending-files-list');
        
        container.innerHTML = '';
        
        pendingFiles.forEach(file => {
            const metadata = file.metadata || {};
            const fileElement = document.createElement('div');
            fileElement.className = 'file-item pending';
            fileElement.innerHTML = `
                <div class="file-info">
                    <h4>${metadata.patient_name || 'Sin nombre'}</h4>
                    <p><strong>Orden:</strong> ${metadata.order_number || 'N/A'}</p>
                    <p><strong>Doctor:</strong> ${metadata.doctor_name || 'N/A'}</p>
                    <p><strong>Creado:</strong> ${new Date(metadata.created_at).toLocaleString()}</p>
                </div>
                <div class="file-actions">
                    <button onclick="markAsCompleted('${file.filename}')" class="btn-complete">
                        ✅ Completar
                    </button>
                    <button onclick="markAsCancelled('${file.filename}')" class="btn-cancel">
                        ❌ Cancelar
                    </button>
                </div>
            `;
            container.appendChild(fileElement);
        });
    } catch (error) {
        console.error('Error al cargar archivos pendientes:', error);
    }
}
```

### **JavaScript para Actualizar Estados:**
```javascript
async function markAsCompleted(filename) {
    try {
        const result = await updateFileStatus(filename, 'completed');
        console.log('Archivo completado:', result);
        
        // Recargar la lista de archivos pendientes
        await loadPendingFiles();
        
        // Actualizar estadísticas
        await updateDashboard();
        
    } catch (error) {
        console.error('Error al completar archivo:', error);
    }
}

async function markAsCancelled(filename) {
    try {
        const result = await updateFileStatus(filename, 'cancelled');
        console.log('Archivo cancelado:', result);
        
        // Recargar la lista de archivos pendientes
        await loadPendingFiles();
        
        // Actualizar estadísticas
        await updateDashboard();
        
    } catch (error) {
        console.error('Error al cancelar archivo:', error);
    }
}
```

### **JavaScript para Dashboard:**
```javascript
async function updateDashboard() {
    try {
        const stats = await getStatusStats();
        
        // Actualizar contadores
        document.getElementById('total-files').textContent = stats.total_files;
        document.getElementById('pending-count').textContent = stats.pending_count;
        document.getElementById('completed-count').textContent = stats.completed_count;
        document.getElementById('cancelled-count').textContent = stats.cancelled_count;
        
    } catch (error) {
        console.error('Error al actualizar dashboard:', error);
    }
}
```

## 📊 **Datos Reales del Sistema (Basado en las Pruebas)**

### **Archivos Pendientes Actuales:**
1. **Carlos Alfonso Hernández Pérez** - Orden: 005 - Dr. García
2. **María González López** - Orden: 006 - Dr. Martínez  
3. **Ana Patricia Rodríguez** - Orden: 007 - Dr. López

### **Estadísticas Actuales:**
- **Total de archivos:** 4
- **Pendientes:** 3
- **Completados:** 1
- **Cancelados:** 0

## 🎯 **Flujo de Trabajo Recomendado**

### **1. Al Cargar la Página:**
```javascript
// Cargar datos iniciales
document.addEventListener('DOMContentLoaded', async () => {
    await loadPendingFiles();
    await updateDashboard();
    await loadCompletedFiles(); // Para el historial
});
```

### **2. Actualización Automática:**
```javascript
// Actualizar cada 30 segundos
setInterval(async () => {
    await loadPendingFiles();
    await updateDashboard();
}, 30000);
```

### **3. Manejo de Eventos:**
```javascript
// Botones de acción
document.addEventListener('click', async (e) => {
    if (e.target.classList.contains('btn-complete')) {
        const filename = e.target.getAttribute('data-filename');
        await markAsCompleted(filename);
    }
    
    if (e.target.classList.contains('btn-cancel')) {
        const filename = e.target.getAttribute('data-filename');
        await markAsCancelled(filename);
    }
});
```

## 🎨 **CSS Sugerido para la Interfaz**

```css
.pending-files-section {
    margin: 20px 0;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
}

.file-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: white;
}

.file-item.pending {
    border-left: 4px solid #ffc107;
}

.file-item.completed {
    border-left: 4px solid #28a745;
}

.file-item.cancelled {
    border-left: 4px solid #dc3545;
}

.file-info h4 {
    margin: 0 0 5px 0;
    color: #333;
}

.file-info p {
    margin: 2px 0;
    color: #666;
    font-size: 14px;
}

.file-actions {
    display: flex;
    gap: 10px;
}

.btn-complete {
    background-color: #28a745;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
}

.btn-cancel {
    background-color: #dc3545;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
}

.dashboard-stats {
    display: flex;
    gap: 20px;
    margin: 20px 0;
}

.stat-item {
    text-align: center;
    padding: 15px;
    border-radius: 8px;
    background-color: white;
    border: 1px solid #ddd;
}

.stat-number {
    display: block;
    font-size: 24px;
    font-weight: bold;
    color: #333;
}

.stat-label {
    display: block;
    font-size: 14px;
    color: #666;
    margin-top: 5px;
}
```

## 🚀 **Implementación Completa**

### **HTML Base:**
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laboratorio Esperanza - Gestión de Resultados</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>📋 Generación de Resultados</h1>
        
        <!-- Dashboard -->
        <div class="dashboard-stats">
            <div class="stat-item">
                <span class="stat-number" id="total-files">0</span>
                <span class="stat-label">Total</span>
            </div>
            <div class="stat-item pending">
                <span class="stat-number" id="pending-count">0</span>
                <span class="stat-label">Pendientes</span>
            </div>
            <div class="stat-item completed">
                <span class="stat-number" id="completed-count">0</span>
                <span class="stat-label">Completados</span>
            </div>
        </div>
        
        <!-- Archivos Pendientes -->
        <div class="pending-files-section">
            <h3>📋 Archivos Pendientes</h3>
            <div id="pending-files-list">
                <!-- Se cargarán dinámicamente -->
            </div>
        </div>
        
        <!-- Historial -->
        <div class="completed-files-section">
            <h3>✅ Historial de Completados</h3>
            <div id="completed-files-list">
                <!-- Se cargarán dinámicamente -->
            </div>
        </div>
    </div>
    
    <script src="app.js"></script>
</body>
</html>
```

## 🎉 **¡Sistema Listo para Usar!**

El sistema de estados está completamente implementado y probado. Los datos muestran que:

- ✅ **Archivos pendientes** se obtienen correctamente
- ✅ **Estados se actualizan** sin problemas
- ✅ **Estadísticas** se calculan correctamente
- ✅ **API endpoints** funcionan perfectamente
- ✅ **Datos JSON** están estructurados correctamente

**El frontend puede empezar a usar estos endpoints inmediatamente para mostrar los archivos pendientes en la interfaz principal.**
