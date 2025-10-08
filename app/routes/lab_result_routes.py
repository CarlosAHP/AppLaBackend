"""
Rutas de Resultados de Laboratorio
"""

from flask import Blueprint
from app.controllers.lab_result_controller import LabResultController

# Crear Blueprint para rutas de resultados de laboratorio
lab_result_bp = Blueprint('lab_results', __name__, url_prefix='/api/lab-results')

# Instanciar controlador
lab_result_controller = LabResultController()


@lab_result_bp.route('', methods=['POST'])
def create_lab_result():
    """Ruta para crear nuevo resultado de laboratorio"""
    return lab_result_controller.create_lab_result()


@lab_result_bp.route('', methods=['GET'])
def get_lab_results():
    """Ruta para obtener lista de resultados de laboratorio"""
    return lab_result_controller.get_lab_results()


@lab_result_bp.route('/<int:result_id>', methods=['GET'])
def get_lab_result(result_id):
    """Ruta para obtener un resultado de laboratorio específico"""
    return lab_result_controller.get_lab_result(result_id)


@lab_result_bp.route('/<int:result_id>', methods=['PUT'])
def update_lab_result(result_id):
    """Ruta para actualizar resultado de laboratorio"""
    return lab_result_controller.update_lab_result(result_id)


@lab_result_bp.route('/<int:result_id>', methods=['DELETE'])
def delete_lab_result(result_id):
    """Ruta para eliminar resultado de laboratorio"""
    return lab_result_controller.delete_lab_result(result_id)


@lab_result_bp.route('/<int:result_id>/status', methods=['PUT'])
def update_lab_result_status(result_id):
    """Ruta para actualizar estado del resultado de laboratorio"""
    return lab_result_controller.update_lab_result_status(result_id)
