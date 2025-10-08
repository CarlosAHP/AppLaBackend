"""
Rutas para la API de pacientes
"""

from flask import Blueprint
from app.controllers.patient_controller import PatientController

# Crear el blueprint para las rutas de pacientes
patient_bp = Blueprint('patients', __name__, url_prefix='/api/patients')

# Rutas para pacientes
@patient_bp.route('', methods=['POST'])
def create_patient():
    """Crear un nuevo paciente"""
    return PatientController.create_patient()

@patient_bp.route('', methods=['GET'])
def get_all_patients():
    """Obtener todos los pacientes con paginación"""
    return PatientController.get_all_patients()

@patient_bp.route('/search', methods=['GET'])
def search_patients():
    """Buscar pacientes"""
    return PatientController.search_patients()

@patient_bp.route('/statistics', methods=['GET'])
def get_patient_statistics():
    """Obtener estadísticas de pacientes"""
    return PatientController.get_patient_statistics()

@patient_bp.route('/<int:patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    """Obtener paciente por ID"""
    return PatientController.get_patient_by_id(patient_id)

@patient_bp.route('/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Actualizar un paciente"""
    return PatientController.update_patient(patient_id)

@patient_bp.route('/<int:patient_id>', methods=['DELETE'])
def deactivate_patient(patient_id):
    """Desactivar un paciente"""
    return PatientController.deactivate_patient(patient_id)

@patient_bp.route('/<int:patient_id>/activate', methods=['POST'])
def activate_patient(patient_id):
    """Reactivar un paciente"""
    return PatientController.activate_patient(patient_id)

@patient_bp.route('/code/<string:patient_code>', methods=['GET'])
def get_patient_by_code(patient_code):
    """Obtener paciente por código"""
    return PatientController.get_patient_by_code(patient_code)

@patient_bp.route('/dpi/<string:dpi>', methods=['GET'])
def get_patient_by_dpi(dpi):
    """Obtener paciente por DPI"""
    return PatientController.get_patient_by_dpi(dpi)
