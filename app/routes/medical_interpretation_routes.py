"""
Rutas para interpretación médica de resultados de laboratorio
"""
from flask import Blueprint
from app.controllers.medical_interpretation_controller import MedicalInterpretationController

# Crear blueprint
medical_interpretation_bp = Blueprint('medical_interpretation', __name__)

# Instanciar controlador
medical_controller = MedicalInterpretationController()

# Rutas de interpretación médica
@medical_interpretation_bp.route('/api/medical-interpret/health', methods=['GET'])
def health_check():
    """Verificar estado del servicio de interpretación médica"""
    return medical_controller.health_check()

@medical_interpretation_bp.route('/api/medical-interpret', methods=['POST'])
def interpret_lab_results():
    """
    Interpretar resultados de laboratorio desde HTML
    
    Body JSON:
    {
        "html_content": "contenido HTML de resultados",
        "patient_info": {
            "age": 35,
            "gender": "F"
        }
    }
    """
    return medical_controller.interpret_lab_results()

@medical_interpretation_bp.route('/api/medical-interpret/report/<int:lab_report_id>', methods=['POST'])
def interpret_from_report(lab_report_id):
    """
    Interpretar resultados desde un reporte de laboratorio existente
    
    Body JSON (opcional):
    {
        "patient_info": {
            "age": 35,
            "gender": "F"
        }
    }
    """
    return medical_controller.interpret_from_report(lab_report_id)

@medical_interpretation_bp.route('/api/medical-interpret/history', methods=['GET'])
def get_interpretation_history():
    """Obtener historial de interpretaciones (placeholder)"""
    return medical_controller.get_interpretation_history()





