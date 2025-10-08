"""
Servicio de Sincronización
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from app.models.sync import Sync
from app.models.lab_result import LabResult
from app.models.payment import Payment
from app.models.user import User
from database import db


class SyncService:
    """Servicio para manejar la lógica de sincronización"""
    
    def __init__(self):
        self.max_retry_count = 3
    
    def create_sync_log(self, sync_type: str, entity_id: int, entity_type: str, 
                       operation: str, data_before: Dict[str, Any] = None, 
                       data_after: Dict[str, Any] = None, source: str = None, 
                       destination: str = None) -> Dict[str, Any]:
        """Crear log de sincronización"""
        try:
            sync_log = Sync(
                sync_type=sync_type,
                entity_id=entity_id,
                entity_type=entity_type,
                operation=operation,
                data_before=data_before,
                data_after=data_after,
                source=source,
                destination=destination,
                status='pending'
            )
            
            # Guardar en base de datos
            db.session.add(sync_log)
            db.session.commit()
            
            # Intentar sincronización inmediata
            self.process_sync(sync_log.id)
            
            return {
                'success': True,
                'sync_log': sync_log.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al crear log de sincronización: {str(e)}'
            }
    
    def get_sync_logs(self, page: int = 1, per_page: int = 10, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Obtener logs de sincronización con paginación"""
        try:
            query = Sync.query
            
            # Aplicar filtros
            if filters:
                if filters.get('sync_type'):
                    query = query.filter(Sync.sync_type == filters['sync_type'])
                if filters.get('status'):
                    query = query.filter(Sync.status == filters['status'])
                if filters.get('entity_type'):
                    query = query.filter(Sync.entity_type == filters['entity_type'])
            
            # Ordenar por fecha de creación descendente
            query = query.order_by(Sync.created_at.desc())
            
            # Paginación
            pagination = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            sync_logs = [log.to_dict() for log in pagination.items]
            
            return {
                'success': True,
                'sync_logs': sync_logs,
                'pagination': {
                    'page': pagination.page,
                    'pages': pagination.pages,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener logs de sincronización: {str(e)}'
            }
    
    def get_sync_log_by_id(self, log_id: int) -> Dict[str, Any]:
        """Obtener log de sincronización por ID"""
        try:
            sync_log = Sync.query.get(log_id)
            
            if not sync_log:
                return {
                    'success': False,
                    'message': 'Log de sincronización no encontrado'
                }
            
            return {
                'success': True,
                'sync_log': sync_log.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener log de sincronización: {str(e)}'
            }
    
    def retry_sync(self, log_id: int) -> Dict[str, Any]:
        """Reintentar sincronización fallida"""
        try:
            sync_log = Sync.query.get(log_id)
            
            if not sync_log:
                return {
                    'success': False,
                    'message': 'Log de sincronización no encontrado'
                }
            
            if sync_log.status == 'success':
                return {
                    'success': False,
                    'message': 'La sincronización ya fue exitosa'
                }
            
            if sync_log.retry_count >= self.max_retry_count:
                return {
                    'success': False,
                    'message': 'Se ha alcanzado el número máximo de reintentos'
                }
            
            # Incrementar contador de reintentos
            sync_log.retry_count += 1
            sync_log.last_retry = datetime.utcnow()
            sync_log.status = 'pending'
            sync_log.updated_at = datetime.utcnow()
            
            # Guardar cambios
            db.session.commit()
            
            # Procesar sincronización
            self.process_sync(log_id)
            
            return {
                'success': True,
                'sync_log': sync_log.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al reintentar sincronización: {str(e)}'
            }
    
    def manual_sync(self, entity_type: str, entity_id: int, operation: str = 'update') -> Dict[str, Any]:
        """Sincronización manual de datos"""
        try:
            # Obtener entidad
            entity = self.get_entity_by_type_and_id(entity_type, entity_id)
            
            if not entity:
                return {
                    'success': False,
                    'message': f'{entity_type} con ID {entity_id} no encontrado'
                }
            
            # Crear log de sincronización manual
            sync_log = Sync(
                sync_type=entity_type.lower(),
                entity_id=entity_id,
                entity_type=entity_type,
                operation=operation,
                data_after=entity.to_dict(),
                status='pending',
                is_manual=True
            )
            
            # Guardar en base de datos
            db.session.add(sync_log)
            db.session.commit()
            
            # Procesar sincronización
            self.process_sync(sync_log.id)
            
            return {
                'success': True,
                'sync_log': sync_log.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error en sincronización manual: {str(e)}'
            }
    
    def bulk_sync(self, entity_type: str, filters: Dict[str, Any] = None, operation: str = 'update') -> Dict[str, Any]:
        """Sincronización masiva de datos"""
        try:
            # Obtener entidades según filtros
            entities = self.get_entities_by_type_and_filters(entity_type, filters)
            
            if not entities:
                return {
                    'success': False,
                    'message': 'No se encontraron entidades para sincronizar'
                }
            
            sync_logs = []
            
            for entity in entities:
                # Crear log de sincronización
                sync_log = Sync(
                    sync_type=entity_type.lower(),
                    entity_id=entity.id,
                    entity_type=entity_type,
                    operation=operation,
                    data_after=entity.to_dict(),
                    status='pending'
                )
                
                sync_logs.append(sync_log)
            
            # Guardar en base de datos
            db.session.add_all(sync_logs)
            db.session.commit()
            
            # Procesar sincronizaciones
            for sync_log in sync_logs:
                self.process_sync(sync_log.id)
            
            return {
                'success': True,
                'count': len(sync_logs),
                'sync_logs': [log.to_dict() for log in sync_logs]
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error en sincronización masiva: {str(e)}'
            }
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Obtener estado general de sincronización"""
        try:
            # Contar logs por estado
            total_logs = Sync.query.count()
            pending_logs = Sync.query.filter_by(status='pending').count()
            success_logs = Sync.query.filter_by(status='success').count()
            failed_logs = Sync.query.filter_by(status='failed').count()
            
            # Contar logs por tipo
            type_counts = {}
            for sync_type in ['lab_result', 'payment', 'user']:
                count = Sync.query.filter_by(sync_type=sync_type).count()
                type_counts[sync_type] = count
            
            # Obtener logs fallidos recientes
            recent_failed = Sync.query.filter_by(status='failed').order_by(Sync.created_at.desc()).limit(5).all()
            
            return {
                'success': True,
                'status': {
                    'total_logs': total_logs,
                    'pending_logs': pending_logs,
                    'success_logs': success_logs,
                    'failed_logs': failed_logs,
                    'type_counts': type_counts,
                    'recent_failed': [log.to_dict() for log in recent_failed]
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener estado de sincronización: {str(e)}'
            }
    
    def process_sync(self, sync_log_id: int) -> bool:
        """Procesar sincronización (simulado)"""
        try:
            sync_log = Sync.query.get(sync_log_id)
            
            if not sync_log:
                return False
            
            # Simular procesamiento de sincronización
            # En una implementación real, aquí se enviarían los datos a un sistema externo
            
            # Simular éxito o fallo aleatorio (90% éxito)
            import random
            success = random.random() < 0.9
            
            if success:
                sync_log.status = 'success'
                sync_log.synced_at = datetime.utcnow()
            else:
                sync_log.status = 'failed'
                sync_log.error_message = 'Error simulado en sincronización'
                sync_log.error_code = 'SYNC_ERROR'
            
            sync_log.updated_at = datetime.utcnow()
            
            # Guardar cambios
            db.session.commit()
            
            return success
            
        except Exception as e:
            # Marcar como fallido
            sync_log = Sync.query.get(sync_log_id)
            if sync_log:
                sync_log.status = 'failed'
                sync_log.error_message = str(e)
                sync_log.updated_at = datetime.utcnow()
                db.session.commit()
            
            return False
    
    def get_entity_by_type_and_id(self, entity_type: str, entity_id: int):
        """Obtener entidad por tipo e ID"""
        if entity_type == 'LabResult':
            return LabResult.query.get(entity_id)
        elif entity_type == 'Payment':
            return Payment.query.get(entity_id)
        elif entity_type == 'User':
            return User.query.get(entity_id)
        else:
            return None
    
    def get_entities_by_type_and_filters(self, entity_type: str, filters: Dict[str, Any] = None):
        """Obtener entidades por tipo y filtros"""
        if entity_type == 'LabResult':
            query = LabResult.query
            if filters:
                if filters.get('status'):
                    query = query.filter(LabResult.status == filters['status'])
            return query.all()
        elif entity_type == 'Payment':
            query = Payment.query
            if filters:
                if filters.get('status'):
                    query = query.filter(Payment.status == filters['status'])
            return query.all()
        elif entity_type == 'User':
            query = User.query
            if filters:
                if filters.get('is_active'):
                    query = query.filter(User.is_active == filters['is_active'])
            return query.all()
        else:
            return []
