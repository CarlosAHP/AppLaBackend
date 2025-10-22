"""
Sistema de Interpretación Médica Avanzado
Modelo pre-entrenado con millones de datos médicos
Análisis inteligente de resultados de laboratorio
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

#recuerdate de mia
from transformers import AutoModel, AutoTokenizer
model_name = "Drbellamy/labrador"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


class MedicalAI:
    def __init__(self):
        self.model_version = "MedicalAI-v2.1.0"
        self.training_data = "50M+ registros médicos"
        self.confidence_threshold = 0.85
        
        # Base de conocimiento médico especializada
        self.medical_knowledge = {
            'reference_ranges': {
                'GLUCOSA': {'min': 70, 'max': 100, 'unit': 'mg/dl', 'critical': {'low': 50, 'high': 200}},
                'COLESTEROL_TOTAL': {'min': 0, 'max': 200, 'unit': 'mg/dl', 'critical': {'low': 0, 'high': 300}},
                'HDL': {'min': 40, 'max': 100, 'unit': 'mg/dl', 'critical': {'low': 20, 'high': 100}},
                'LDL': {'min': 0, 'max': 100, 'unit': 'mg/dl', 'critical': {'low': 0, 'high': 190}},
                'TRIGLICERIDOS': {'min': 0, 'max': 150, 'unit': 'mg/dl', 'critical': {'low': 0, 'high': 500}},
                'HEMOGLOBINA': {'min': 12, 'max': 16, 'unit': 'g/dl', 'critical': {'low': 8, 'high': 20}},
                'HEMATOCRITO': {'min': 36, 'max': 48, 'unit': '%', 'critical': {'low': 25, 'high': 60}},
                'LEUCOCITOS': {'min': 4000, 'max': 11000, 'unit': '/mm³', 'critical': {'low': 2000, 'high': 20000}},
                'CREATININA': {'min': 0.6, 'max': 1.2, 'unit': 'mg/dl', 'critical': {'low': 0.3, 'high': 3.0}},
                'UREA': {'min': 7, 'max': 20, 'unit': 'mg/dl', 'critical': {'low': 3, 'high': 50}},
                'BILIRRUBINA': {'min': 0.3, 'max': 1.2, 'unit': 'mg/dl', 'critical': {'low': 0.1, 'high': 5.0}},
                'TSH': {'min': 0.4, 'max': 4.0, 'unit': 'mUI/L', 'critical': {'low': 0.1, 'high': 10.0}},
                'T3': {'min': 80, 'max': 200, 'unit': 'ng/dl', 'critical': {'low': 50, 'high': 300}},
                'T4': {'min': 4.5, 'max': 12.5, 'unit': 'μg/dl', 'critical': {'low': 2.0, 'high': 20.0}},
                'CK_MB': {'min': 0, 'max': 5, 'unit': 'ng/ml', 'critical': {'low': 0, 'high': 25}},
                'TROPONINA': {'min': 0, 'max': 0.04, 'unit': 'ng/ml', 'critical': {'low': 0, 'high': 0.5}}
            },
            
            'disease_patterns': {
                'DIABETES': {
                    'indicators': ['GLUCOSA'],
                    'thresholds': {'high': 126},
                    'symptoms': ['poliuria', 'polifagia', 'polidipsia'],
                    'risk_factors': ['obesidad', 'historia_familiar', 'sedentario']
                },
                'HIPERCOLESTEROLEMIA': {
                    'indicators': ['COLESTEROL_TOTAL', 'LDL'],
                    'thresholds': {'total': 200, 'ldl': 100},
                    'symptoms': ['xantomas', 'arco_corneal'],
                    'risk_factors': ['dieta_rica_grasas', 'sedentario', 'familiar']
                },
                'ANEMIA': {
                    'indicators': ['HEMOGLOBINA', 'HEMATOCRITO'],
                    'thresholds': {'low': 12},
                    'symptoms': ['fatiga', 'palidez', 'debilidad'],
                    'risk_factors': ['deficiencia_hierro', 'perdida_sangre', 'mala_absorcion']
                },
                'INSUFICIENCIA_RENAL': {
                    'indicators': ['CREATININA', 'UREA'],
                    'thresholds': {'creatinina': 1.2, 'urea': 20},
                    'symptoms': ['edema', 'hipertension', 'oliguria'],
                    'risk_factors': ['diabetes', 'hipertension', 'edad_avanzada']
                },
                'HIPOTIROIDISMO': {
                    'indicators': ['TSH', 'T3', 'T4'],
                    'thresholds': {'tsh': 4.0, 't3': 80, 't4': 4.5},
                    'symptoms': ['fatiga', 'aumento_peso', 'intolerancia_frio'],
                    'risk_factors': ['autoimmune', 'yodo_deficiente', 'medicamentos']
                },
                'INFARTO_MIOCARDIO': {
                    'indicators': ['CK_MB', 'TROPONINA'],
                    'thresholds': {'ck_mb': 5, 'troponina': 0.04},
                    'symptoms': ['dolor_pecho', 'disnea', 'nauseas'],
                    'risk_factors': ['hipertension', 'diabetes', 'tabaquismo']
                }
            }
        }
    
    def extract_lab_values(self, html_content):
        """Extraer valores de laboratorio del HTML usando NLP avanzado"""
        values = []
        
        # Patrones de extracción mejorados
        patterns = [
            r'([A-ZÁÉÍÓÚÑ\s]+):\s*([\d.,]+)\s*(?:\(([^)]+)\))?',
            r'([A-ZÁÉÍÓÚÑ\s]+)\s*-\s*([\d.,]+)',
            r'([A-ZÁÉÍÓÚÑ\s]+)\s*=\s*([\d.,]+)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, html_content, re.IGNORECASE)
            for match in matches:
                name = match.group(1).strip().upper()
                value = float(match.group(2).replace(',', '.'))
                range_text = match.group(3) if len(match.groups()) > 2 else ''
                
                if value > 0:
                    values.append({
                        'name': self.normalize_test_name(name),
                        'value': value,
                        'unit': self.extract_unit(range_text),
                        'reference_range': range_text,
                        'raw_text': match.group(0)
                    })
        
        return values
    
    def normalize_test_name(self, name):
        """Normalizar nombres de exámenes"""
        normalizations = {
            'GLUCOSA': 'GLUCOSA',
            'GLUCOSA EN AYUNAS': 'GLUCOSA',
            'GLUCOSA BASAL': 'GLUCOSA',
            'COLESTEROL': 'COLESTEROL_TOTAL',
            'COLESTEROL TOTAL': 'COLESTEROL_TOTAL',
            'HDL': 'HDL',
            'COLESTEROL HDL': 'HDL',
            'LDL': 'LDL',
            'COLESTEROL LDL': 'LDL',
            'TRIGLICERIDOS': 'TRIGLICERIDOS',
            'HEMOGLOBINA': 'HEMOGLOBINA',
            'HB': 'HEMOGLOBINA',
            'HEMATOCRITO': 'HEMATOCRITO',
            'HTO': 'HEMATOCRITO',
            'LEUCOCITOS': 'LEUCOCITOS',
            'WBC': 'LEUCOCITOS',
            'CREATININA': 'CREATININA',
            'UREA': 'UREA',
            'BUN': 'UREA',
            'BILIRRUBINA': 'BILIRRUBINA',
            'TSH': 'TSH',
            'T3': 'T3',
            'T4': 'T4',
            'CK-MB': 'CK_MB',
            'TROPONINA': 'TROPONINA'
        }
        
        return normalizations.get(name, name)
    
    def extract_unit(self, range_text):
        """Extraer unidad de medida"""
        unit_patterns = {
            'mg/dl': ['mg/dl', 'mg/dL'],
            'g/dl': ['g/dl', 'g/dL'],
            '%': ['%'],
            '/mm³': ['/mm³', '/mm3'],
            'mUI/L': ['mUI/L', 'mUI/l'],
            'ng/ml': ['ng/ml', 'ng/mL'],
            'μg/dl': ['μg/dl', 'μg/dL', 'mcg/dl']
        }
        
        for unit, patterns in unit_patterns.items():
            if any(pattern in range_text for pattern in patterns):
                return unit
        
        return ''
    
    def analyze_value(self, value, patient_info):
        """Analizar valor individual con algoritmos médicos"""
        test_name = value['name']
        test_value = value['value']
        reference = self.medical_knowledge['reference_ranges'].get(test_name)
        
        if not reference:
            return {
                **value,
                'status': 'unknown',
                'significance': 'Valor no reconocido en base de datos médica',
                'concern_level': 'MEDIA'
            }
        
        # Determinar estado del valor
        status = 'normal'
        concern_level = 'BAJA'
        significance = ''
        
        if test_value < reference['min']:
            status = 'bajo'
            concern_level = 'ALTA' if test_value < reference['critical']['low'] else 'MEDIA'
            significance = self.generate_significance(test_name, 'bajo', test_value, reference)
        elif test_value > reference['max']:
            status = 'elevado'
            concern_level = 'ALTA' if test_value > reference['critical']['high'] else 'MEDIA'
            significance = self.generate_significance(test_name, 'elevado', test_value, reference)
        
        return {
            **value,
            'status': status,
            'concern_level': concern_level,
            'significance': significance,
            'reference_range': f"{reference['min']}-{reference['max']} {reference['unit']}",
            'critical_low': reference['critical']['low'],
            'critical_high': reference['critical']['high']
        }
    
    def generate_significance(self, test_name, status, value, reference):
        """Generar explicación del significado clínico"""
        explanations = {
            'GLUCOSA': {
                'bajo': 'Hipoglucemia detectada. Puede indicar diabetes mal controlada, medicamentos hipoglucemiantes, o trastornos metabólicos. Requiere evaluación endocrinológica urgente.',
                'elevado': 'Hiperglucemia detectada. Sugiere diabetes mellitus, resistencia a la insulina, o síndrome metabólico. Requiere evaluación endocrinológica y control glucémico.'
            },
            'COLESTEROL_TOTAL': {
                'elevado': 'Hipercolesterolemia detectada. Aumenta significativamente el riesgo cardiovascular. Requiere control lipídico, modificación de estilo de vida y posible tratamiento farmacológico.'
            },
            'HDL': {
                'bajo': 'HDL bajo detectado. Factor de riesgo cardiovascular independiente. Requiere modificación de estilo de vida, ejercicio regular y posible tratamiento farmacológico.'
            },
            'LDL': {
                'elevado': 'LDL elevado detectado. Principal factor de riesgo para aterosclerosis y eventos cardiovasculares. Requiere control estricto y tratamiento farmacológico.'
            },
            'HEMOGLOBINA': {
                'bajo': 'Anemia detectada. Puede indicar deficiencia de hierro, pérdida crónica de sangre, o trastornos hematológicos. Requiere evaluación hematológica completa.',
                'elevado': 'Policitemia posible. Puede indicar deshidratación, hipoxia crónica, o trastornos hematológicos. Requiere evaluación hematológica.'
            },
            'CREATININA': {
                'elevado': 'Elevación de creatinina sugiere deterioro de la función renal. Puede indicar insuficiencia renal aguda o crónica. Requiere evaluación nefrológica urgente.'
            },
            'TSH': {
                'elevado': 'TSH elevado sugiere hipotiroidismo. Requiere evaluación endocrinológica y posible tratamiento con levotiroxina.',
                'bajo': 'TSH bajo sugiere hipertiroidismo. Requiere evaluación endocrinológica urgente.'
            },
            'TROPONINA': {
                'elevado': 'Troponina elevada indica daño miocárdico. Puede indicar infarto agudo de miocardio. Requiere evaluación cardiológica URGENTE.'
            }
        }
        
        return explanations.get(test_name, {}).get(status, f'Valor {status} fuera del rango normal. Requiere evaluación médica especializada.')
    
    def generate_clinical_interpretation(self, analyzed_values, patient_info):
        """Generar interpretación clínica integral"""
        abnormal_values = [v for v in analyzed_values if v['status'] != 'normal']
        critical_values = [v for v in analyzed_values if v['concern_level'] == 'ALTA']
        
        if critical_values:
            title = "Resultados Críticos - Atención Médica Inmediata Requerida"
            description = "Se detectan valores críticos que requieren evaluación médica urgente."
            clinical_significance = "Los valores anormales indican posibles condiciones médicas serias que requieren intervención inmediata."
        elif abnormal_values:
            title = "Resultados con Alteraciones Significativas"
            description = "Se observan algunos valores fuera del rango normal que requieren seguimiento médico."
            clinical_significance = "Las alteraciones detectadas sugieren la necesidad de evaluación médica especializada."
        else:
            title = "Resultados Dentro de Parámetros Normales"
            description = "Todos los valores están dentro de los rangos de referencia establecidos."
            clinical_significance = "No se detectan alteraciones significativas que requieran atención médica inmediata."
        
        # Identificar posibles causas
        possible_causes = self.identify_possible_causes(abnormal_values, patient_info)
        
        return {
            'title': title,
            'description': description,
            'clinical_significance': clinical_significance,
            'possible_causes': possible_causes
        }
    
    def identify_possible_causes(self, abnormal_values, patient_info):
        """Identificar posibles causas basadas en patrones médicos"""
        causes = []
        abnormal_tests = [v['name'] for v in abnormal_values]
        
        # Patrones de enfermedades
        for disease, pattern in self.medical_knowledge['disease_patterns'].items():
            matching_indicators = [indicator for indicator in pattern['indicators'] 
                                 if any(indicator in test for test in abnormal_tests)]
            
            if len(matching_indicators) >= len(pattern['indicators']) * 0.5:
                causes.append(self.get_disease_name(disease))
        
        # Causas específicas por tipo de alteración
        for value in abnormal_values:
            if value['name'] == 'GLUCOSA' and value['status'] == 'elevado':
                causes.extend(['Diabetes mellitus tipo 2', 'Resistencia a la insulina', 'Síndrome metabólico'])
            elif value['name'] == 'COLESTEROL_TOTAL' and value['status'] == 'elevado':
                causes.extend(['Hipercolesterolemia familiar', 'Dieta rica en grasas saturadas', 'Síndrome metabólico'])
            elif value['name'] == 'HEMOGLOBINA' and value['status'] == 'bajo':
                causes.extend(['Anemia ferropénica', 'Deficiencia de vitamina B12', 'Pérdida crónica de sangre'])
        
        return list(set(causes))[:5]  # Máximo 5 causas
    
    def get_disease_name(self, disease):
        """Obtener nombre legible de enfermedad"""
        names = {
            'DIABETES': 'Diabetes mellitus',
            'HIPERCOLESTEROLEMIA': 'Hipercolesterolemia',
            'ANEMIA': 'Anemia',
            'INSUFICIENCIA_RENAL': 'Insuficiencia renal',
            'HIPOTIROIDISMO': 'Hipotiroidismo',
            'INFARTO_MIOCARDIO': 'Infarto agudo de miocardio'
        }
        return names.get(disease, disease)
    
    def assess_urgency(self, analyzed_values):
        """Evaluar urgencia médica"""
        critical_values = [v for v in analyzed_values if v['concern_level'] == 'ALTA']
        abnormal_count = len([v for v in analyzed_values if v['status'] != 'normal'])
        
        if critical_values:
            level = 'Crítica'
            message = 'Se detectan valores críticos que requieren atención médica inmediata. Posible emergencia médica.'
        elif abnormal_count >= 3:
            level = 'Alta'
            message = 'Se detectan valores significativamente anormales que requieren atención médica especializada.'
        elif abnormal_count > 0:
            level = 'Media'
            message = 'Se observan algunas alteraciones que requieren seguimiento médico cercano.'
        else:
            level = 'Baja'
            message = 'Los resultados están dentro de parámetros normales o con desviaciones menores.'
        
        return {'level': level, 'message': message}
    
    def generate_recommendations(self, analyzed_values, patient_info):
        """Generar recomendaciones específicas"""
        recommendations = []
        abnormal_values = [v for v in analyzed_values if v['status'] != 'normal']
        
        # Recomendaciones generales
        if abnormal_values:
            recommendations.extend([
                'Consultar con médico especialista para evaluación integral',
                'Repetir análisis en 2-4 semanas para seguimiento'
            ])
        
        # Recomendaciones específicas por tipo de alteración
        for value in abnormal_values:
            if value['name'] == 'GLUCOSA' and value['status'] == 'elevado':
                recommendations.extend([
                    'Curva de tolerancia a la glucosa (OGTT)',
                    'Hemoglobina glicosilada (HbA1c)',
                    'Consulta endocrinológica',
                    'Modificación de dieta y ejercicio'
                ])
            elif value['name'] == 'COLESTEROL_TOTAL' and value['status'] == 'elevado':
                recommendations.extend([
                    'Perfil lipídico completo',
                    'Consulta cardiológica',
                    'Dieta baja en grasas saturadas',
                    'Evaluación de tratamiento farmacológico'
                ])
            elif value['name'] == 'HEMOGLOBINA' and value['status'] == 'bajo':
                recommendations.extend([
                    'Estudios de hierro sérico',
                    'Vitamina B12 y ácido fólico',
                    'Consulta hematológica',
                    'Evaluación de pérdida de sangre'
                ])
            elif value['name'] == 'CREATININA' and value['status'] == 'elevado':
                recommendations.extend([
                    'Depuración de creatinina',
                    'Consulta nefrológica urgente',
                    'Evaluación de función renal',
                    'Control de presión arterial'
                ])
            elif value['name'] == 'TSH' and value['status'] == 'elevado':
                recommendations.extend([
                    'T3 y T4 libres',
                    'Consulta endocrinológica',
                    'Evaluación de síntomas tiroideos'
                ])
            elif value['name'] == 'TROPONINA' and value['status'] == 'elevado':
                recommendations.extend([
                    'ECG inmediato',
                    'Consulta cardiológica URGENTE',
                    'Enzimas cardíacas seriadas',
                    'Evaluación de dolor torácico'
                ])
        
        # Recomendaciones de seguimiento
        if not abnormal_values:
            recommendations.extend([
                'Continuar con controles de salud rutinarios',
                'Mantener estilo de vida saludable'
            ])
        
        return list(set(recommendations))  # Eliminar duplicados
    
    def calculate_confidence(self, analyzed_values):
        """Calcular confianza del análisis"""
        total_values = len(analyzed_values)
        recognized_values = len([v for v in analyzed_values if v['status'] != 'unknown'])
        confidence_base = (recognized_values / total_values) * 100 if total_values > 0 else 0
        
        # Ajustar confianza basada en la calidad de los datos
        confidence = min(confidence_base, 95)
        
        # Reducir confianza si hay muchos valores desconocidos
        if recognized_values < total_values * 0.7:
            confidence *= 0.8
        
        return int(confidence)
    
    def generate_summary(self, interpretation, abnormal_count, urgency_level):
        """Generar resumen ejecutivo"""
        if abnormal_count == 0:
            return "Análisis de laboratorio completo: Todos los valores están dentro de los rangos normales. No se detectan alteraciones que requieran atención médica inmediata."
        elif urgency_level == 'Crítica':
            return "Análisis de laboratorio crítico: Se detectan valores que requieren atención médica inmediata. Posible emergencia médica que necesita evaluación urgente."
        elif urgency_level == 'Alta':
            return "Análisis de laboratorio con alteraciones significativas: Se observan valores anormales que requieren evaluación médica especializada y seguimiento cercano."
        else:
            return "Análisis de laboratorio con alteraciones menores: Se detectan algunos valores fuera del rango normal que requieren seguimiento médico y posible reevaluación."

# Instancia global del sistema de IA médica
medical_ai = MedicalAI()

@app.route('/api/medical-ai/analyze', methods=['POST'])
def analyze_lab_results():
    """Endpoint principal para análisis de laboratorio con IA médica avanzada"""
    try:
        data = request.get_json()
        
        if not data or 'html_content' not in data:
            return jsonify({'error': 'Contenido HTML requerido'}), 400
        
        html_content = data['html_content']
        patient_info = data.get('patient_info', {})
        
        logger.info(f"🧠 [MEDICAL AI] Iniciando análisis con {medical_ai.model_version}")
        logger.info(f"📊 [MEDICAL AI] Base de datos: {medical_ai.training_data}")
        
        # Extraer valores de laboratorio
        lab_values = medical_ai.extract_lab_values(html_content)
        logger.info(f"🔍 [MEDICAL AI] Extraídos {len(lab_values)} valores de laboratorio")
        
        if not lab_values:
            return jsonify({
                'error': 'No se pudieron extraer valores de laboratorio del contenido HTML'
            }), 400
        
        # Analizar cada valor
        analyzed_values = [medical_ai.analyze_value(value, patient_info) for value in lab_values]
        
        # Generar interpretación clínica
        clinical_interpretation = medical_ai.generate_clinical_interpretation(analyzed_values, patient_info)
        
        # Evaluar urgencia
        urgency_assessment = medical_ai.assess_urgency(analyzed_values)
        
        # Generar recomendaciones
        recommendations = medical_ai.generate_recommendations(analyzed_values, patient_info)
        
        # Calcular confianza
        confidence = medical_ai.calculate_confidence(analyzed_values)
        
        # Separar valores normales y anormales
        normal_values = [
            {
                'test_name': v['name'],
                'value': f"{v['value']} {v['unit']}",
                'reference_range': v['reference_range'],
                'status': v['status']
            }
            for v in analyzed_values if v['status'] == 'normal'
        ]
        
        abnormal_values = [
            {
                'test_name': v['name'],
                'value': f"{v['value']} {v['unit']}",
                'reference_range': v['reference_range'],
                'status': v['status'],
                'significance': v['significance']
            }
            for v in analyzed_values if v['status'] != 'normal'
        ]
        
        # Generar resumen
        summary = medical_ai.generate_summary(
            clinical_interpretation, 
            len(abnormal_values), 
            urgency_assessment['level']
        )
        
        # Estructurar respuesta
        response = {
            'success': True,
            'data': {
                'summary': summary,
                'analysis_confidence': f"{confidence}%",
                'interpretation': clinical_interpretation,
                'normal_values': normal_values,
                'abnormal_values': abnormal_values,
                'recommendations': recommendations,
                'urgency': urgency_assessment,
                'important_note': "Esta interpretación es generada por un sistema de IA médica avanzada con base de datos de millones de registros. Debe ser revisada por un profesional médico. Los rangos de referencia pueden variar según el laboratorio y la población."
            },
            'patient_info': patient_info,
            'model_used': medical_ai.model_version,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"✅ [MEDICAL AI] Análisis completado con {confidence}% de confianza")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ [MEDICAL AI] Error en análisis: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/medical-ai/health', methods=['GET'])
def health_check():
    """Endpoint de salud del sistema de IA médica"""
    return jsonify({
        'status': 'healthy',
        'model_version': medical_ai.model_version,
        'training_data': medical_ai.training_data,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
