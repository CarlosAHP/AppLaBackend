"""
Controlador de Pagos
"""

from flask import request, jsonify
from app.services.payment_service import PaymentService
from app.controllers.auth_controller import token_required


class PaymentController:
    """Controlador para manejar pagos"""
    
    def __init__(self):
        self.payment_service = PaymentService()
    
    @token_required
    def create_payment(self):
        """Crear nuevo pago"""
        try:
            data = request.get_json()
            
            # Validar datos requeridos
            required_fields = ['amount', 'payment_method', 'patient_id', 'patient_name']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'message': f'El campo {field} es requerido'
                    }), 400
            
            result = self.payment_service.create_payment(data)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Pago creado exitosamente',
                    'data': result['payment']
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
    def get_payments(self):
        """Obtener lista de pagos"""
        try:
            # Parámetros de consulta
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            patient_id = request.args.get('patient_id')
            status = request.args.get('status')
            payment_method = request.args.get('payment_method')
            
            filters = {
                'patient_id': patient_id,
                'status': status,
                'payment_method': payment_method
            }
            
            result = self.payment_service.get_payments(
                page=page, 
                per_page=per_page, 
                filters=filters
            )
            
            return jsonify({
                'success': True,
                'data': result['payments'],
                'pagination': result['pagination']
            }), 200
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    @token_required
    def get_payment(self, payment_id):
        """Obtener un pago específico"""
        try:
            result = self.payment_service.get_payment_by_id(payment_id)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'data': result['payment']
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
    def update_payment(self, payment_id):
        """Actualizar pago"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Datos requeridos para la actualización'
                }), 400
            
            result = self.payment_service.update_payment(payment_id, data)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Pago actualizado exitosamente',
                    'data': result['payment']
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
    def delete_payment(self, payment_id):
        """Eliminar pago"""
        try:
            result = self.payment_service.delete_payment(payment_id)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Pago eliminado exitosamente'
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
    def update_payment_status(self, payment_id):
        """Actualizar estado del pago"""
        try:
            data = request.get_json()
            
            if not data.get('status'):
                return jsonify({
                    'success': False,
                    'message': 'El campo status es requerido'
                }), 400
            
            result = self.payment_service.update_payment_status(
                payment_id, 
                data['status']
            )
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Estado del pago actualizado exitosamente',
                    'data': result['payment']
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
    def get_payment_summary(self):
        """Obtener resumen de pagos"""
        try:
            # Parámetros de consulta
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            patient_id = request.args.get('patient_id')
            
            result = self.payment_service.get_payment_summary(
                start_date=start_date,
                end_date=end_date,
                patient_id=patient_id
            )
            
            return jsonify({
                'success': True,
                'data': result['summary']
            }), 200
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
