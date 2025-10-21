"""
Controlador para interpretación médica de resultados de laboratorio
"""
import logging
from flask import request, jsonify
from app.services.medical_interpretation_service import MedicalInterpretationService

# Configurar logging
logger = logging.getLogger(__name__)

class MedicalInterpretationController:
    """Controlador para manejar requests de interpretación médica"""
    
    def __init__(self):
        self.medical_service = MedicalInterpretationService()
    
    def health_check(self):
        """Endpoint para verificar el estado del servicio de interpretación"""
        try:
            status = self.medical_service.get_health_status()
            return jsonify(status), 200
        except Exception as e:
            logger.error(f"Error en health check: {e}")
            return jsonify({
                "error": "Error verificando estado del servicio",
                "message": str(e)
            }), 500
    
    def interpret_lab_results(self):
        """
        Interpreta resultados de laboratorio desde HTML
        
        Body JSON esperado:
        {
            "html_content": "contenido HTML de resultados",
            "patient_info": {
                "age": 35,
                "gender": "F"
            }
        }
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    "error": "No se proporcionaron datos",
                    "message": "Se requiere JSON con html_content y patient_info"
                }), 400
            
            html_content = data.get('html_content')
            patient_info = data.get('patient_info', {})
            
            if not html_content:
                return jsonify({
                    "error": "Contenido HTML requerido",
                    "message": "El campo html_content es obligatorio"
                }), 400
            
            # Validar información del paciente
            if not patient_info:
                patient_info = {"age": "No especificado", "gender": "No especificado"}
            
            # Interpretar resultados
            result = self.medical_service.interpret_lab_results(html_content, patient_info)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Error en interpret_lab_results: {e}")
            return jsonify({
                "error": "Error interno del servidor",
                "message": str(e)
            }), 500
    
    def interpret_from_report(self, lab_report_id):
        """
        Interpreta resultados desde un reporte de laboratorio existente
        
        Args:
            lab_report_id: ID del reporte de laboratorio
        """
        try:
            data = request.get_json() or {}
            patient_info = data.get('patient_info', {})
            
            # Validar ID del reporte
            if not lab_report_id:
                return jsonify({
                    "error": "ID de reporte requerido",
                    "message": "Se requiere lab_report_id"
                }), 400
            
            # Interpretar desde reporte
            result = self.medical_service.interpret_from_lab_report(lab_report_id, patient_info)
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Error en interpret_from_report: {e}")
            return jsonify({
                "error": "Error interno del servidor",
                "message": str(e)
            }), 500
    
    def get_interpretation_history(self):
        """
        Obtiene historial de interpretaciones (placeholder para futura implementación)
        """
        try:
            # TODO: Implementar almacenamiento de interpretaciones
            return jsonify({
                "message": "Funcionalidad de historial no implementada aún",
                "interpretations": []
            }), 200
        except Exception as e:
            logger.error(f"Error en get_interpretation_history: {e}")
            return jsonify({
                "error": "Error obteniendo historial",
                "message": str(e)
            }), 500





