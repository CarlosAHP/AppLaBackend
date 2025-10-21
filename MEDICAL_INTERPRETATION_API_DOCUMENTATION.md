# 🏥 API de Interpretación Médica - Laboratorio Esperanza

## 📋 Descripción
Esta API permite interpretar resultados de laboratorio usando inteligencia artificial (Google Gemini Pro) para proporcionar análisis médicos profesionales de los resultados.

## 🚀 Configuración Inicial

### 1. Instalar Dependencias
```bash
# Instalar dependencias adicionales para interpretación médica
pip install -r requirements_medical.txt
```

### 2. Configurar API Key de Google Gemini
```bash
# En Windows (PowerShell)
$env:GEMINI_API_KEY="tu-api-key-aqui"

# En Windows (CMD)
set GEMINI_API_KEY=tu-api-key-aqui

# En Linux/Mac
export GEMINI_API_KEY="tu-api-key-aqui"
```

### 3. Obtener API Key de Google Gemini
1. Ir a: https://aistudio.google.com/
2. Iniciar sesión con cuenta de Google
3. Ir a: https://aistudio.google.com/app/apikey
4. Hacer clic en "Create API key"
5. Copiar la key y configurarla en el sistema

## 🔗 Endpoints Disponibles

### 1. Health Check
**GET** `/api/medical-interpret/health`

Verifica el estado del servicio de interpretación médica.

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "gemini_configured": true,
  "openai_configured": false
}
```

### 2. Interpretar Resultados desde HTML
**POST** `/api/medical-interpret`

Interpreta resultados de laboratorio desde contenido HTML.

**Body:**
```json
{
  "html_content": "<html>...contenido HTML de resultados...</html>",
  "patient_info": {
    "age": 35,
    "gender": "F"
  }
}
```

**Respuesta:**
```json
{
  "success": true,
  "interpretation": "RESUMEN CLÍNICO: ...\nVALORES ANORMALES: ...\nINTERPRETACIÓN: ...\nRECOMENDACIONES: ...\nURGENCIA: Media",
  "patient_info": {
    "age": 35,
    "gender": "F"
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "model_used": "gemini-pro"
}
```

### 3. Interpretar desde Reporte Existente
**POST** `/api/medical-interpret/report/{lab_report_id}`

Interpreta resultados desde un reporte de laboratorio existente en el sistema.

**Body (opcional):**
```json
{
  "patient_info": {
    "age": 35,
    "gender": "F"
  }
}
```

**Respuesta:**
```json
{
  "success": true,
  "interpretation": "RESUMEN CLÍNICO: ...\nVALORES ANORMALES: ...\nINTERPRETACIÓN: ...\nRECOMENDACIONES: ...\nURGENCIA: Media",
  "patient_info": {
    "age": 35,
    "gender": "F"
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "model_used": "gemini-pro"
}
```

### 4. Historial de Interpretaciones
**GET** `/api/medical-interpret/history`

Obtiene historial de interpretaciones (funcionalidad futura).

## 🧪 Pruebas de la API

### 1. Verificar Estado del Servicio
```bash
curl http://localhost:5000/api/medical-interpret/health
```

### 2. Probar Interpretación Médica
```bash
curl -X POST http://localhost:5000/api/medical-interpret \
  -H "Content-Type: application/json" \
  -d '{
    "html_content": "<html><body><h1>Resultados de Laboratorio</h1><p>Glucosa: 95 mg/dl (Normal: 70-100)</p><p>Colesterol: 180 mg/dl (Normal: <200)</p></body></html>",
    "patient_info": {"age": 35, "gender": "F"}
  }'
```

### 3. Interpretar desde Reporte Existente
```bash
curl -X POST http://localhost:5000/api/medical-interpret/report/123 \
  -H "Content-Type: application/json" \
  -d '{
    "patient_info": {"age": 35, "gender": "F"}
  }'
```

## 📊 Formato de Interpretación

La interpretación se devuelve en formato **Markdown simple** para que el frontend pueda parsearlo y estilizarlo:

### Estructura de la Respuesta:
```
**RESUMEN CLÍNICO**
[Resumen de los hallazgos principales]

**VALORES ANORMALES**
- [Lista de valores fuera de rango]
- [Si no hay valores anormales, indica "No se identifican valores anormales"]

**INTERPRETACIÓN**
- [Explicación médica de los resultados]
- [Análisis por secciones si es relevante]

**RECOMENDACIONES**
- [Sugerencias para el seguimiento médico]
- [Medidas preventivas si aplica]

**URGENCIA**
[Nivel de urgencia: Baja, Media o Alta]
```

### Ventajas del Formato Markdown:
- ✅ **Flexibilidad Total** - El frontend controla el formato y estilos
- ✅ **Fácil Parsing** - Simple conversión a HTML
- ✅ **Personalizable** - Diferentes estilos para cada sección
- ✅ **Responsive** - Se adapta a cualquier dispositivo
- ✅ **Mantenible** - Cambios de formato sin tocar el backend

## ⚠️ Consideraciones Importantes

- **Solo para fines informativos**: La interpretación no reemplaza la evaluación médica profesional
- **Consulta médica requerida**: El paciente debe consultar con su médico para diagnóstico y tratamiento
- **Privacidad**: Los datos se procesan a través de Google Gemini (revisar políticas de privacidad)
- **Límites de API**: Google Gemini tiene límites de uso gratuito

## 🔧 Solución de Problemas

### Error: "Servicio de interpretación no configurado"
- Verificar que `GEMINI_API_KEY` esté configurada
- Reiniciar el servidor después de configurar la variable

### Error: "Error procesando interpretación"
- Verificar conectividad a internet
- Verificar que la API key sea válida
- Revisar logs del servidor para más detalles

### Error: "No hay contenido HTML en el reporte"
- Verificar que el reporte tenga contenido HTML
- Verificar que el ID del reporte sea correcto

## 📝 Logs y Monitoreo

Los logs se registran en el nivel INFO y incluyen:
- Configuración del servicio
- Errores de procesamiento
- Errores de interpretación
- Errores de extracción de HTML

## 🎨 Ejemplos de Parsing Frontend

### JavaScript Simple
```javascript
function parseMedicalInterpretation(interpretation) {
    return interpretation
        // Títulos
        .replace(/^\*\*(.*?)\*\*$/gm, '<h3>$1</h3>')
        // Listas con viñetas
        .replace(/^\- (.*)$/gm, '<li>$1</li>')
        // Texto en negrita
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Agrupar listas
        .replace(/(<li>.*<\/li>)/g, '<ul>$1</ul>')
        // Saltos de línea
        .replace(/\n/g, '<br>');
}

// Uso
const response = await fetch('/api/medical-interpret', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        html_content: htmlContent,
        patient_info: patientInfo
    })
});

const data = await response.json();
if (data.success) {
    const parsedHtml = parseMedicalInterpretation(data.interpretation);
    document.getElementById('interpretation').innerHTML = parsedHtml;
}
```

### React Hook
```jsx
const useMedicalInterpretation = () => {
    const [interpretation, setInterpretation] = useState('');
    const [loading, setLoading] = useState(false);

    const parseMarkdown = (text) => {
        return text
            .replace(/^\*\*(.*?)\*\*$/gm, '<h3>$1</h3>')
            .replace(/^\- (.*)$/gm, '<li>$1</li>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/(<li>.*<\/li>)/g, '<ul>$1</ul>')
            .replace(/\n/g, '<br>');
    };

    const getInterpretation = async (htmlContent, patientInfo) => {
        setLoading(true);
        try {
            const response = await fetch('/api/medical-interpret', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ html_content: htmlContent, patient_info: patientInfo })
            });
            const data = await response.json();
            if (data.success) {
                setInterpretation(parseMarkdown(data.interpretation));
            }
        } finally {
            setLoading(false);
        }
    };

    return { interpretation, loading, getInterpretation };
};
```

## 🚀 Ejecutar el Servidor

```bash
# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements_medical.txt

# Configurar API key
export GEMINI_API_KEY="tu-api-key-aqui"

# Ejecutar servidor
python run.py
```

El servidor estará disponible en `http://localhost:5000`

## 📁 Archivos de Ejemplo

- `frontend_markdown_parser_example.html` - Ejemplo completo con estilos
- `frontend_integration_examples.md` - Ejemplos para React, Vue, Angular
- `test_medical_interpretation.py` - Script de pruebas
