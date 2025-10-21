"""
Rutas para la API de pacientes
"""

from flask import Blueprint
from app.controllers.patient_controller import PatientController
from app.middleware.auth_middleware import token_required

# Crear el blueprint para las rutas de pacientes
patient_bp = Blueprint('patients', __name__, url_prefix='/api/patients')

# Rutas para pacientes
@patient_bp.route('', methods=['POST'])
@token_required
def create_patient():
    """Crear un nuevo paciente"""
    return PatientController.create_patient()

@patient_bp.route('', methods=['GET'])
@token_required
def get_all_patients():
    """Obtener todos los pacientes con paginación"""
    return PatientController.get_all_patients()

@patient_bp.route('/search', methods=['GET'])
@token_required
def search_patients():
    """Buscar pacientes"""
    return PatientController.search_patients()

@patient_bp.route('/statistics', methods=['GET'])
@token_required
def get_patient_statistics():
    """Obtener estadísticas de pacientes"""
    return PatientController.get_patient_statistics()

@patient_bp.route('/<int:patient_id>', methods=['GET'])
@token_required
def get_patient_by_id(patient_id):
    """Obtener paciente por ID"""
    return PatientController.get_patient_by_id(patient_id)

@patient_bp.route('/<int:patient_id>', methods=['PUT'])
@token_required
def update_patient(patient_id):
    """Actualizar un paciente"""
    return PatientController.update_patient(patient_id)

@patient_bp.route('/<int:patient_id>', methods=['DELETE'])
@token_required
def deactivate_patient(patient_id):
    """Desactivar un paciente"""
    return PatientController.deactivate_patient(patient_id)

@patient_bp.route('/<int:patient_id>/activate', methods=['POST'])
@token_required
def activate_patient(patient_id):
    """Reactivar un paciente"""
    return PatientController.activate_patient(patient_id)

@patient_bp.route('/code/<string:patient_code>', methods=['GET'])
@token_required
def get_patient_by_code(patient_code):
    """Obtener paciente por código"""
    return PatientController.get_patient_by_code(patient_code)

@patient_bp.route('/dpi/<string:dpi>', methods=['GET'])
@token_required
def get_patient_by_dpi(dpi):
    """Obtener paciente por DPI"""
    return PatientController.get_patient_by_dpi(dpi)
