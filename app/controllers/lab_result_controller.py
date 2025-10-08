"""
Controlador de Resultados de Laboratorio
"""

from flask import request, jsonify
from app.services.lab_result_service import LabResultService
from app.controllers.auth_controller import token_required


class LabResultController:
    """Controlador para manejar resultados de laboratorio"""
    
    def __init__(self):
        self.lab_result_service = LabResultService()
    
    @token_required
    def create_lab_result(self):
        """Crear nuevo resultado de laboratorio"""
        try:
            data = request.get_json()
            
            # Validar datos requeridos
            required_fields = ['patient_id', 'patient_name', 'exam_type', 'exam_date']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'message': f'El campo {field} es requerido'
                    }), 400
            
            result = self.lab_result_service.create_lab_result(data)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Resultado de laboratorio creado exitosamente',
                    'data': result['lab_result']
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'message': result['message']
                }), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    @token_required
    def get_lab_results(self):
        """Obtener lista de resultados de laboratorio"""
        try:
            # Parámetros de consulta
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            patient_id = request.args.get('patient_id')
            status = request.args.get('status')
            exam_type = request.args.get('exam_type')
            
            filters = {
                'patient_id': patient_id,
                'status': status,
                'exam_type': exam_type
            }
            
            result = self.lab_result_service.get_lab_results(
                page=page, 
                per_page=per_page, 
                filters=filters
            )
            
            return jsonify({
                'success': True,
                'data': result['lab_results'],
                'pagination': result['pagination']
            }), 200
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    @token_required
    def get_lab_result(self, result_id):
        """Obtener un resultado de laboratorio específico"""
        try:
            result = self.lab_result_service.get_lab_result_by_id(result_id)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'data': result['lab_result']
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': result['message']
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    @token_required
    def update_lab_result(self, result_id):
        """Actualizar resultado de laboratorio"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Datos requeridos para la actualización'
                }), 400
            
            result = self.lab_result_service.update_lab_result(result_id, data)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Resultado de laboratorio actualizado exitosamente',
                    'data': result['lab_result']
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': result['message']
                }), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    @token_required
    def delete_lab_result(self, result_id):
        """Eliminar resultado de laboratorio"""
        try:
            result = self.lab_result_service.delete_lab_result(result_id)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Resultado de laboratorio eliminado exitosamente'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': result['message']
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    @token_required
    def update_lab_result_status(self, result_id):
        """Actualizar estado del resultado de laboratorio"""
        try:
            data = request.get_json()
            
            if not data.get('status'):
                return jsonify({
                    'success': False,
                    'message': 'El campo status es requerido'
                }), 400
            
            result = self.lab_result_service.update_lab_result_status(
                result_id, 
                data['status']
            )
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Estado actualizado exitosamente',
                    'data': result['lab_result']
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': result['message']
                }), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
