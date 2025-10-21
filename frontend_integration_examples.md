# 🎨 Ejemplos de Integración Frontend - Interpretación Médica

## 📋 Formato de Respuesta de la API

La API devuelve la interpretación en formato Markdown simple:

```json
{
  "success": true,
  "interpretation": "**RESUMEN CLÍNICO**\n\nLa paciente presenta...\n\n**VALORES ANORMALES**\n\n- Hemoglobina: 10.5 g/dl (Normal: 12-16)\n- Glucosa: 140 mg/dl (Normal: 70-100)\n\n**INTERPRETACIÓN**\n\n- **Anemia:** Explicación detallada...\n- **Hiperglucemia:** Análisis médico...\n\n**RECOMENDACIONES**\n\n1. Consulta médica inmediata\n2. Pruebas adicionales\n\n**URGENCIA**\n\nMedia. Requiere atención en plazo razonable.",
  "model_used": "gemini-2.0-flash",
  "patient_info": {"age": 45, "gender": "F"},
  "timestamp": "2025-10-09T21:04:33.498502Z"
}
```

## 🔧 Ejemplos de Integración

### 1. JavaScript Vanilla

```javascript
// Función para parsear Markdown básico
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

// Uso con la API
async function getMedicalInterpretation(htmlContent, patientInfo) {
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
}
```

### 2. React

```jsx
import React, { useState } from 'react';

const MedicalInterpretation = () => {
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
                body: JSON.stringify({
                    html_content: htmlContent,
                    patient_info: patientInfo
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                const parsedHtml = parseMarkdown(data.interpretation);
                setInterpretation(parsedHtml);
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <button 
                onClick={() => getInterpretation(htmlContent, patientInfo)}
                disabled={loading}
            >
                {loading ? 'Interpretando...' : 'Interpretar Resultados'}
            </button>
            
            {interpretation && (
                <div 
                    className="interpretation"
                    dangerouslySetInnerHTML={{ __html: interpretation }}
                />
            )}
        </div>
    );
};
```

### 3. Vue.js

```vue
<template>
  <div>
    <button @click="getInterpretation" :disabled="loading">
      {{ loading ? 'Interpretando...' : 'Interpretar Resultados' }}
    </button>
    
    <div 
      v-if="interpretation" 
      class="interpretation"
      v-html="parsedInterpretation"
    ></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      interpretation: '',
      loading: false
    };
  },
  computed: {
    parsedInterpretation() {
      return this.interpretation
        .replace(/^\*\*(.*?)\*\*$/gm, '<h3>$1</h3>')
        .replace(/^\- (.*)$/gm, '<li>$1</li>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/(<li>.*<\/li>)/g, '<ul>$1</ul>')
        .replace(/\n/g, '<br>');
    }
  },
  methods: {
    async getInterpretation() {
      this.loading = true;
      try {
        const response = await fetch('/api/medical-interpret', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            html_content: this.htmlContent,
            patient_info: this.patientInfo
          })
        });
        
        const data = await response.json();
        
        if (data.success) {
          this.interpretation = data.interpretation;
        }
      } catch (error) {
        console.error('Error:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
```

### 4. Angular

```typescript
// medical-interpretation.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class MedicalInterpretationService {
  private apiUrl = '/api/medical-interpret';

  constructor(private http: HttpClient) {}

  getInterpretation(htmlContent: string, patientInfo: any) {
    return this.http.post(this.apiUrl, {
      html_content: htmlContent,
      patient_info: patientInfo
    });
  }
}

// medical-interpretation.component.ts
import { Component } from '@angular/core';
import { MedicalInterpretationService } from './medical-interpretation.service';

@Component({
  selector: 'app-medical-interpretation',
  template: `
    <button (click)="getInterpretation()" [disabled]="loading">
      {{ loading ? 'Interpretando...' : 'Interpretar Resultados' }}
    </button>
    
    <div 
      *ngIf="interpretation" 
      class="interpretation"
      [innerHTML]="parsedInterpretation"
    ></div>
  `
})
export class MedicalInterpretationComponent {
  interpretation = '';
  loading = false;

  constructor(private medicalService: MedicalInterpretationService) {}

  get parsedInterpretation() {
    return this.interpretation
      .replace(/^\*\*(.*?)\*\*$/gm, '<h3>$1</h3>')
      .replace(/^\- (.*)$/gm, '<li>$1</li>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/(<li>.*<\/li>)/g, '<ul>$1</ul>')
      .replace(/\n/g, '<br>');
  }

  getInterpretation() {
    this.loading = true;
    this.medicalService.getInterpretation(this.htmlContent, this.patientInfo)
      .subscribe({
        next: (data: any) => {
          if (data.success) {
            this.interpretation = data.interpretation;
          }
        },
        error: (error) => console.error('Error:', error),
        complete: () => this.loading = false
      });
  }
}
```

## 🎨 CSS para Estilizar

```css
.interpretation {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
  line-height: 1.6;
}

.interpretation h3 {
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 5px;
  margin-top: 20px;
}

.interpretation ul {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 4px;
  padding: 10px;
  margin: 10px 0;
}

.interpretation strong {
  color: #2c3e50;
  font-weight: bold;
}

/* Estilos específicos para urgencia */
.interpretation h3:contains("URGENCIA") {
  color: #e74c3c;
}

.interpretation h3:contains("VALORES ANORMALES") {
  color: #f39c12;
}
```

## 📱 Ejemplo Completo con Estilos

```html
<!DOCTYPE html>
<html>
<head>
    <title>Interpretación Médica</title>
    <style>
        .interpretation-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            font-family: Arial, sans-serif;
        }
        
        .section {
            margin: 20px 0;
            padding: 15px;
            border-radius: 8px;
        }
        
        .summary { background: #e8f4fd; }
        .abnormal { background: #fff3cd; }
        .interpretation { background: #f8f9fa; }
        .recommendations { background: #e7f3ff; }
        .urgency { background: #d4edda; font-weight: bold; }
        
        .urgency.high { background: #f8d7da; color: #721c24; }
        .urgency.medium { background: #fff3cd; color: #856404; }
        .urgency.low { background: #d4edda; color: #155724; }
    </style>
</head>
<body>
    <div class="interpretation-container">
        <div id="interpretation"></div>
    </div>
    
    <script>
        // Tu código de parsing aquí
    </script>
</body>
</html>
```

## 🚀 Ventajas de este Enfoque

1. **✅ Flexibilidad Total** - El frontend controla completamente el formato
2. **✅ Fácil Personalización** - Diferentes estilos para diferentes secciones
3. **✅ Responsive** - Se adapta a cualquier dispositivo
4. **✅ Mantenible** - Cambios de formato sin tocar el backend
5. **✅ Rápido** - Parsing simple y eficiente
6. **✅ Escalable** - Fácil agregar nuevas secciones o estilos

## 📋 Estructura de la Respuesta

La API siempre devuelve:

- **RESUMEN CLÍNICO** - Análisis general
- **VALORES ANORMALES** - Lista de valores fuera de rango
- **INTERPRETACIÓN** - Explicación médica detallada
- **RECOMENDACIONES** - Sugerencias profesionales
- **URGENCIA** - Nivel de prioridad (Baja/Media/Alta)

¡El frontend puede parsear y estilizar cada sección de manera independiente!





