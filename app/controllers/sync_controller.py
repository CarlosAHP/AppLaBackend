"""
Controlador de Sincronización
"""

from flask import request, jsonify
from app.services.sync_service import SyncService
from app.controllers.auth_controller import token_required


class SyncController:
    """Controlador para manejar sincronización de datos"""
    
    def __init__(self):
        self.sync_service = SyncService()
    
    @token_required
    def get_sync_logs(self):
        """Obtener logs de sincronización"""
        try:
            # Parámetros de consulta
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            sync_type = request.args.get('sync_type')
            status = request.args.get('status')
            entity_type = request.args.get('entity_type')
            
            filters = {
                'sync_type': sync_type,
                'status': status,
                'entity_type': entity_type
            }
            
            result = self.sync_service.get_sync_logs(
                page=page, 
                per_page=per_page, 
                filters=filters
            )
            
            return jsonify({
                'success': True,
                'data': result['sync_logs'],
                'pagination': result['pagination']
            }), 200
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    @token_required
    def get_sync_log(self, log_id):
        """Obtener un log de sincronización específico"""
        try:
            result = self.sync_service.get_sync_log_by_id(log_id)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'data': result['sync_log']
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
    def retry_sync(self, log_id):
        """Reintentar sincronización fallida"""
        try:
            result = self.sync_service.retry_sync(log_id)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Sincronización reintentada exitosamente',
                    'data': result['sync_log']
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
    def manual_sync(self):
        """Sincronización manual de datos"""
        try:
            data = request.get_json()
            
            if not data.get('entity_type') or not data.get('entity_id'):
                return jsonify({
                    'success': False,
                    'message': 'entity_type y entity_id son requeridos'
                }), 400
            
            result = self.sync_service.manual_sync(
                entity_type=data['entity_type'],
                entity_id=data['entity_id'],
                operation=data.get('operation', 'update')
            )
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Sincronización manual iniciada',
                    'data': result['sync_log']
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
    def get_sync_status(self):
        """Obtener estado general de sincronización"""
        try:
            result = self.sync_service.get_sync_status()
            
            return jsonify({
                'success': True,
                'data': result['status']
            }), 200
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    @token_required
    def bulk_sync(self):
        """Sincronización masiva de datos"""
        try:
            data = request.get_json()
            
            if not data.get('entity_type'):
                return jsonify({
                    'success': False,
                    'message': 'entity_type es requerido'
                }), 400
            
            result = self.sync_service.bulk_sync(
                entity_type=data['entity_type'],
                filters=data.get('filters', {}),
                operation=data.get('operation', 'update')
            )
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': f'Sincronización masiva iniciada para {result["count"]} registros',
                    'data': {
                        'count': result['count'],
                        'sync_logs': result['sync_logs']
                    }
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
