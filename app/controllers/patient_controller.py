"""
Controlador para manejar las peticiones HTTP de pacientes
"""

from flask import request, jsonify, g
from typing import Dict, Any
from app.services.patient_service import PatientService
from app.middleware.auth_middleware import token_required


class PatientController:
    """Controlador para operaciones de pacientes"""
    
    @staticmethod
    @token_required
    def create_patient():
        """
        Crear un nuevo paciente
        
        POST /api/patients
        """
        try:
            data = request.get_json()
            
            # Validar datos requeridos
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'No se proporcionaron datos'
                }), 400
            
            required_fields = ['first_name', 'last_name']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'message': f'El campo {field} es requerido'
                    }), 400
            
            # Crear el paciente
            result = PatientService.create_patient(data, g.current_user['id'])
            
            if result['success']:
                return jsonify(result), 201
            else:
                status_code = 400
                if result.get('error') == 'DUPLICATE_PATIENT_CODE':
                    status_code = 409
                elif result.get('error') == 'DUPLICATE_DPI':
                    status_code = 409
                
                return jsonify(result), status_code
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error interno del servidor: {str(e)}'
            }), 500
    
    @staticmethod
    @token_required
    def get_patient_by_id(patient_id):
        """
        Obtener paciente por ID
        
        GET /api/patients/<int:patient_id>
        """
        try:
            result = PatientService.get_patient_by_id(patient_id)
            
            if result['success']:
                return jsonify(result), 200
            else:
                status_code = 404 if result.get('error') == 'PATIENT_NOT_FOUND' else 500
                return jsonify(result), status_code
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error interno del servidor: {str(e)}'
            }), 500
    
    @staticmethod
    @token_required
    def get_patient_by_code(patient_code):
        """
        Obtener paciente por código
        
        GET /api/patients/code/<string:patient_code>
        """
        try:
            result = PatientService.get_patient_by_code(patient_code)
            
            if result['success']:
                return jsonify(result), 200
            else:
                status_code = 404 if result.get('error') == 'PATIENT_NOT_FOUND' else 500
                return jsonify(result), status_code
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error interno del servidor: {str(e)}'
            }), 500
    
    @staticmethod
    @token_required
    def get_patient_by_dpi(dpi):
        """
        Obtener paciente por DPI
        
        GET /api/patients/dpi/<string:dpi>
        """
        try:
            result = PatientService.get_patient_by_dpi(dpi)
            
            if result['success']:
                return jsonify(result), 200
            else:
                status_code = 404 if result.get('error') == 'PATIENT_NOT_FOUND' else 500
                return jsonify(result), status_code
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error interno del servidor: {str(e)}'
            }), 500
    
    @staticmethod
    @token_required
    def search_patients():
        """
        Buscar pacientes
        
        GET /api/patients/search?q=<search_term>&limit=<limit>
        """
        try:
            search_term = request.args.get('q', '').strip()
            limit = request.args.get('limit', 50, type=int)
            
            if not search_term:
                return jsonify({
                    'success': False,
                    'message': 'El parámetro de búsqueda "q" es requerido'
                }), 400
            
            if limit > 100:
                limit = 100  # Limitar máximo 100 resultados
            
            result = PatientService.search_patients(search_term, limit)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 500
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error interno del servidor: {str(e)}'
            }), 500
    
    @staticmethod
    @token_required
    def get_all_patients():
        """
        Obtener todos los pacientes con paginación
        
        GET /api/patients?page=<page>&per_page=<per_page>&active_only=<active_only>
        """
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            active_only = request.args.get('active_only', 'true').lower() == 'true'
            
            # Validar parámetros
            if page < 1:
                page = 1
            if per_page < 1 or per_page > 100:
                per_page = 20
            
            result = PatientService.get_all_patients(page, per_page, active_only)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 500
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error interno del servidor: {str(e)}'
            }), 500
    
    @staticmethod
    @token_required
    def update_patient(patient_id):
        """
        Actualizar un paciente
        
        PUT /api/patients/<int:patient_id>
        """
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'No se proporcionaron datos para actualizar'
                }), 400
            
            result = PatientService.update_patient(patient_id, data)
            
            if result['success']:
                return jsonify(result), 200
            else:
                status_code = 404 if result.get('error') == 'PATIENT_NOT_FOUND' else 400
                if result.get('error') == 'DUPLICATE_DPI':
                    status_code = 409
                
                return jsonify(result), status_code
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error interno del servidor: {str(e)}'
            }), 500
    
    @staticmethod
    @token_required
    def deactivate_patient(patient_id):
        """
        Desactivar un paciente
        
        DELETE /api/patients/<int:patient_id>
        """
        try:
            result = PatientService.deactivate_patient(patient_id)
            
            if result['success']:
                return jsonify(result), 200
            else:
                status_code = 404 if result.get('error') == 'PATIENT_NOT_FOUND' else 500
                return jsonify(result), status_code
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error interno del servidor: {str(e)}'
            }), 500
    
    @staticmethod
    @token_required
    def activate_patient(patient_id):
        """
        Reactivar un paciente
        
        POST /api/patients/<int:patient_id>/activate
        """
        try:
            result = PatientService.activate_patient(patient_id)
            
            if result['success']:
                return jsonify(result), 200
            else:
                status_code = 404 if result.get('error') == 'PATIENT_NOT_FOUND' else 500
                return jsonify(result), status_code
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error interno del servidor: {str(e)}'
            }), 500
    
    @staticmethod
    @token_required
    def get_patient_statistics():
        """
        Obtener estadísticas de pacientes
        
        GET /api/patients/statistics
        """
        try:
            result = PatientService.get_patient_statistics()
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 500
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error interno del servidor: {str(e)}'
            }), 500
