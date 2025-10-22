# Formato JSON de Interpretación Médica

## Resumen
La API de interpretación médica ahora devuelve respuestas estructuradas en formato JSON, facilitando la integración con el frontend y mejorando la legibilidad para el usuario.

## Estructura de la Respuesta

### Endpoint
```
POST /api/medical-interpret
```

### Parámetros de Entrada
```json
{
  "html_content": "<html>...</html>",
  "patient_info": {
    "age": 35,
    "gender": "F"
  }
}
```

### Estructura de Respuesta JSON

```json
{
  "success": true,
  "data": {
    "summary": "Resumen general de los resultados",
    "analysis_confidence": "95%",
    "interpretation": {
      "title": "Título de la interpretación",
      "description": "Descripción detallada de los hallazgos",
      "clinical_significance": "Significado clínico de los resultados",
      "possible_causes": [
        "Causa 1",
        "Causa 2",
        "Causa 3"
      ]
    },
    "normal_values": [
      {
        "test_name": "Nombre del examen",
        "value": "Valor obtenido",
        "reference_range": "Rango de referencia",
        "status": "normal"
      }
    ],
    "abnormal_values": [
      {
        "test_name": "Nombre del examen",
        "value": "Valor obtenido",
        "reference_range": "Rango de referencia",
        "status": "elevado|bajo|crítico",
        "significance": "Explicación del valor anormal"
      }
    ],
    "recommendations": [
      "Recomendación 1",
      "Recomendación 2",
      "Recomendación 3"
    ],
    "urgency": {
      "level": "Baja|Media|Alta|Crítica",
      "message": "Mensaje sobre la urgencia del caso"
    },
    "important_note": "Nota importante sobre limitaciones y recomendaciones"
  },
  "patient_info": {
    "age": 35,
    "gender": "F"
  },
  "model_used": "gemini-2.0-flash",
  "timestamp": "2025-10-21T18:31:27.251791Z"
}
```

## Campos Explicados para el Frontend

### 1. **summary** (string)
- **Propósito**: Resumen ejecutivo de todos los resultados
- **Uso en Frontend**: Mostrar como título principal o resumen destacado
- **Ejemplo**: "Los resultados revelan hiperuricemia con otros valores normales"

### 2. **analysis_confidence** (string)
- **Propósito**: Nivel de confianza del análisis (porcentaje)
- **Uso en Frontend**: Mostrar como indicador de confiabilidad
- **Ejemplo**: "95%"

### 3. **interpretation** (object)
- **title**: Título de la interpretación principal
- **description**: Descripción detallada de los hallazgos
- **clinical_significance**: Significado clínico para el médico
- **possible_causes**: Array de posibles causas del problema

### 4. **normal_values** (array)
- **Propósito**: Valores que están dentro del rango normal
- **Uso en Frontend**: Mostrar con ícono verde o indicador positivo
- **Estructura**: `{test_name, value, reference_range, status}`

### 5. **abnormal_values** (array)
- **Propósito**: Valores fuera del rango normal
- **Uso en Frontend**: Mostrar con ícono rojo/amarillo y explicación
- **Estructura**: `{test_name, value, reference_range, status, significance}`

### 6. **recommendations** (array)
- **Propósito**: Recomendaciones médicas específicas
- **Uso en Frontend**: Lista de acciones recomendadas para el médico

### 7. **urgency** (object)
- **level**: Nivel de urgencia (Baja, Media, Alta, Crítica)
- **message**: Mensaje explicativo sobre la urgencia
- **Uso en Frontend**: Mostrar con colores y prioridad visual

## Recomendaciones para el Frontend

### 1. **Diseño Visual**
```javascript
// Ejemplo de estructura para mostrar
const displayData = {
  summary: response.data.summary,
  confidence: response.data.analysis_confidence,
  urgency: {
    level: response.data.urgency.level,
    color: getUrgencyColor(response.data.urgency.level)
  },
  normalValues: response.data.normal_values,
  abnormalValues: response.data.abnormal_values,
  recommendations: response.data.recommendations
};
```

### 2. **Colores Sugeridos**
- **Normal**: Verde (#28a745)
- **Elevado**: Naranja (#fd7e14)
- **Bajo**: Azul (#17a2b8)
- **Crítico**: Rojo (#dc3545)

### 3. **Estructura de Componentes**
```
InterpretationCard
├── SummarySection
├── ConfidenceIndicator
├── UrgencyAlert
├── ValuesTable
│   ├── NormalValuesList
│   └── AbnormalValuesList
├── RecommendationsList
└── ImportantNote
```

### 4. **Manejo de Errores**
```javascript
if (!response.success) {
  // Mostrar mensaje de error
  showError(response.message);
  return;
}

// Verificar que los datos estén completos
if (!response.data || !response.data.summary) {
  showError("Datos de interpretación incompletos");
  return;
}
```

## Ejemplo de Implementación Frontend

```javascript
function displayMedicalInterpretation(response) {
  const { data } = response;
  
  // Mostrar resumen
  document.getElementById('summary').textContent = data.summary;
  
  // Mostrar confianza
  document.getElementById('confidence').textContent = data.analysis_confidence;
  
  // Mostrar urgencia
  const urgencyElement = document.getElementById('urgency');
  urgencyElement.textContent = data.urgency.message;
  urgencyElement.className = `urgency-${data.urgency.level.toLowerCase()}`;
  
  // Mostrar valores anormales
  const abnormalList = document.getElementById('abnormal-values');
  data.abnormal_values.forEach(value => {
    const item = document.createElement('li');
    item.innerHTML = `
      <strong>${value.test_name}:</strong> ${value.value} 
      <span class="status-${value.status}">(${value.status})</span>
      <p class="significance">${value.significance}</p>
    `;
    abnormalList.appendChild(item);
  });
  
  // Mostrar recomendaciones
  const recommendationsList = document.getElementById('recommendations');
  data.recommendations.forEach(rec => {
    const item = document.createElement('li');
    item.textContent = rec;
    recommendationsList.appendChild(item);
  });
}
```

## Ventajas del Nuevo Formato

1. **Estructura Clara**: Datos organizados por categorías
2. **Fácil Integración**: JSON estándar para frontend
3. **Información Completa**: Todos los datos necesarios en una respuesta
4. **Escalable**: Fácil agregar nuevos campos
5. **Legible**: Formato claro para desarrolladores y usuarios

## Notas Importantes

- La respuesta siempre incluye un campo `important_note` con limitaciones
- El campo `timestamp` indica cuándo se generó la interpretación
- Los valores de urgencia van de "Baja" a "Crítica"
- La confianza del análisis se expresa como porcentaje
- Todos los arrays pueden estar vacíos si no aplican

