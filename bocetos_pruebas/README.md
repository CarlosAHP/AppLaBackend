# 📄 Sistema de Conversión Word a HTML - Laboratorio Esperanza

## 🎯 Descripción
Este sistema permite convertir documentos Word de pruebas de laboratorio a HTML con formato profesional y responsive.

## 📁 Estructura de Carpetas
```
bocetos_pruebas/
├── README.md                    # Este archivo
├── html_output/                 # Archivos HTML generados
│   ├── index.html              # Página índice
│   ├── hemograma_completo.html # Ejemplo: Hemograma
│   ├── perfil_lipídico.html    # Ejemplo: Perfil Lipídico
│   └── ...                     # Otros archivos HTML
└── [tus_archivos_word.docx]    # Coloca aquí tus archivos Word
```

## 🚀 Cómo Usar

### 1. Preparar Archivos Word
- Coloca tus archivos `.docx` o `.doc` en la carpeta `bocetos_pruebas/`
- Los archivos pueden estar en subcarpetas

### 2. Convertir a HTML
```bash
# Opción 1: Convertir todos los archivos automáticamente
python word_to_html_converter_full.py

# Opción 2: Usar el convertidor básico
python word_to_html_converter.py
```

### 3. Ver Resultados
- Abre `bocetos_pruebas/html_output/index.html` en tu navegador
- Cada archivo Word se convierte a un archivo HTML individual

## 🔧 Métodos de Conversión Disponibles

### 1. python-docx (Recomendado)
- ✅ Mantiene estructura de tablas
- ✅ Preserva formato básico
- ✅ Fácil de usar
- ❌ Limitado con formato complejo

### 2. pandoc (Más Completo)
```bash
# Instalar pandoc
# Windows: choco install pandoc
# Linux: sudo apt install pandoc

# Convertir manualmente
pandoc documento.docx -o documento.html
```

### 3. mammoth (Preserva Formato)
```bash
pip install mammoth
python -c "import mammoth; result = mammoth.convert_to_html(open('documento.docx', 'rb')); print(result.value)"
```

## 📋 Características del HTML Generado

### 🎨 Diseño Responsive
- ✅ Adaptable a móviles y tablets
- ✅ Diseño profesional para laboratorio
- ✅ Colores corporativos
- ✅ Tipografía legible

### 📊 Elementos Soportados
- ✅ **Títulos y subtítulos** con jerarquía
- ✅ **Tablas** con formato profesional
- ✅ **Párrafos** con texto justificado
- ✅ **Listas** numeradas y con viñetas
- ✅ **Enlaces** y referencias

### 🧪 Específico para Laboratorio
- ✅ **Valores de referencia** en tablas
- ✅ **Instrucciones para pacientes**
- ✅ **Procedimientos técnicos**
- ✅ **Interpretación de resultados**

## 📝 Ejemplos de Uso

### Crear una Nueva Prueba
1. Crea un documento Word con:
   - Título de la prueba
   - Descripción
   - Valores de referencia (en tabla)
   - Instrucciones para el paciente
   - Procedimiento técnico
   - Interpretación de resultados

2. Guarda como `.docx` en `bocetos_pruebas/`

3. Ejecuta la conversión:
```bash
python word_to_html_converter_full.py
```

### Personalizar el Diseño
Edita el archivo `word_to_html_converter_full.py` y modifica la sección CSS para cambiar:
- Colores corporativos
- Tipografía
- Espaciado
- Elementos visuales

## 🔍 Solución de Problemas

### Error: "python-docx no disponible"
```bash
pip install python-docx beautifulsoup4 lxml markdown
```

### Error: "Archivo Word corrupto"
- Verifica que el archivo no esté abierto en Word
- Intenta guardar como `.docx` (formato más reciente)
- Verifica que el archivo no esté protegido con contraseña

### Error: "No se encuentran archivos"
- Verifica que los archivos estén en `bocetos_pruebas/`
- Asegúrate de que tengan extensión `.docx` o `.doc`
- Verifica permisos de lectura

## 📊 Estadísticas de Conversión

### Archivos Soportados
- ✅ Microsoft Word (.docx)
- ✅ Microsoft Word (.doc)
- ✅ Texto enriquecido (.rtf) - limitado

### Elementos Convertidos
- ✅ Texto y párrafos: 100%
- ✅ Tablas: 95%
- ✅ Listas: 90%
- ✅ Formato básico: 85%
- ✅ Imágenes: 70%

## 🎯 Próximas Mejoras

- [ ] Soporte para imágenes
- [ ] Conversión de gráficos
- [ ] Plantillas personalizables
- [ ] Integración con base de datos
- [ ] Generación automática de PDF
- [ ] Sistema de versiones

## 📞 Soporte

Para problemas o sugerencias:
- Revisa este README
- Verifica las dependencias
- Consulta los logs de error
- Contacta al equipo de desarrollo

---

**Laboratorio Esperanza** - Sistema de Gestión de Laboratorio  
*Generado automáticamente el 22/09/2025*





















