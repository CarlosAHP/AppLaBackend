"""
Servicio de Pagos
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from app.models.payment import Payment
from app.services.sync_service import SyncService
from database import db


class PaymentService:
    """Servicio para manejar la lógica de pagos"""
    
    def __init__(self):
        self.sync_service = SyncService()
    
    def create_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nuevo pago"""
        try:
            # Crear nuevo pago
            payment = Payment(
                amount=payment_data['amount'],
                currency=payment_data.get('currency', 'PEN'),
                payment_method=payment_data['payment_method'],
                payment_reference=payment_data.get('payment_reference'),
                patient_id=payment_data['patient_id'],
                patient_name=payment_data['patient_name'],
                lab_result_id=payment_data.get('lab_result_id'),
                description=payment_data.get('description'),
                notes=payment_data.get('notes'),
                status='pending'
            )
            
            # Guardar en base de datos
            db.session.add(payment)
            db.session.commit()
            
            # Crear log de sincronización
            self.sync_service.create_sync_log(
                sync_type='payment',
                entity_id=payment.id,
                entity_type='Payment',
                operation='create',
                data_after=payment.to_dict()
            )
            
            return {
                'success': True,
                'payment': payment.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al crear pago: {str(e)}'
            }
    
    def get_payments(self, page: int = 1, per_page: int = 10, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Obtener lista de pagos con paginación"""
        try:
            query = Payment.query
            
            # Aplicar filtros
            if filters:
                if filters.get('patient_id'):
                    query = query.filter(Payment.patient_id == filters['patient_id'])
                if filters.get('status'):
                    query = query.filter(Payment.status == filters['status'])
                if filters.get('payment_method'):
                    query = query.filter(Payment.payment_method == filters['payment_method'])
            
            # Ordenar por fecha de creación descendente
            query = query.order_by(Payment.created_at.desc())
            
            # Paginación
            pagination = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            payments = [payment.to_dict() for payment in pagination.items]
            
            return {
                'success': True,
                'payments': payments,
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
                'message': f'Error al obtener pagos: {str(e)}'
            }
    
    def get_payment_by_id(self, payment_id: int) -> Dict[str, Any]:
        """Obtener pago por ID"""
        try:
            payment = Payment.query.get(payment_id)
            
            if not payment:
                return {
                    'success': False,
                    'message': 'Pago no encontrado'
                }
            
            return {
                'success': True,
                'payment': payment.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener pago: {str(e)}'
            }
    
    def update_payment(self, payment_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar pago"""
        try:
            payment = Payment.query.get(payment_id)
            
            if not payment:
                return {
                    'success': False,
                    'message': 'Pago no encontrado'
                }
            
            # Guardar datos antes de la actualización
            data_before = payment.to_dict()
            
            # Actualizar campos permitidos
            allowed_fields = [
                'amount', 'currency', 'payment_method', 'payment_reference',
                'patient_name', 'description', 'notes'
            ]
            
            for field in allowed_fields:
                if field in update_data:
                    setattr(payment, field, update_data[field])
            
            # Actualizar timestamp
            payment.updated_at = datetime.utcnow()
            
            # Guardar cambios
            db.session.commit()
            
            # Crear log de sincronización
            self.sync_service.create_sync_log(
                sync_type='payment',
                entity_id=payment.id,
                entity_type='Payment',
                operation='update',
                data_before=data_before,
                data_after=payment.to_dict()
            )
            
            return {
                'success': True,
                'payment': payment.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al actualizar pago: {str(e)}'
            }
    
    def delete_payment(self, payment_id: int) -> Dict[str, Any]:
        """Eliminar pago"""
        try:
            payment = Payment.query.get(payment_id)
            
            if not payment:
                return {
                    'success': False,
                    'message': 'Pago no encontrado'
                }
            
            # Guardar datos antes de la eliminación
            data_before = payment.to_dict()
            
            # Eliminar de base de datos
            db.session.delete(payment)
            db.session.commit()
            
            # Crear log de sincronización
            self.sync_service.create_sync_log(
                sync_type='payment',
                entity_id=payment_id,
                entity_type='Payment',
                operation='delete',
                data_before=data_before
            )
            
            return {
                'success': True,
                'message': 'Pago eliminado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al eliminar pago: {str(e)}'
            }
    
    def update_payment_status(self, payment_id: int, status: str) -> Dict[str, Any]:
        """Actualizar estado del pago"""
        try:
            payment = Payment.query.get(payment_id)
            
            if not payment:
                return {
                    'success': False,
                    'message': 'Pago no encontrado'
                }
            
            # Validar estado
            valid_statuses = ['pending', 'completed', 'failed', 'refunded']
            if status not in valid_statuses:
                return {
                    'success': False,
                    'message': f'Estado inválido. Estados válidos: {", ".join(valid_statuses)}'
                }
            
            # Guardar datos antes de la actualización
            data_before = payment.to_dict()
            
            # Actualizar estado
            payment.status = status
            
            # Si se marca como completado, establecer fecha de pago
            if status == 'completed' and not payment.payment_date:
                payment.payment_date = datetime.utcnow()
            
            payment.updated_at = datetime.utcnow()
            
            # Guardar cambios
            db.session.commit()
            
            # Crear log de sincronización
            self.sync_service.create_sync_log(
                sync_type='payment',
                entity_id=payment.id,
                entity_type='Payment',
                operation='update',
                data_before=data_before,
                data_after=payment.to_dict()
            )
            
            return {
                'success': True,
                'payment': payment.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al actualizar estado: {str(e)}'
            }
    
    def get_payment_summary(self, start_date: str = None, end_date: str = None, patient_id: str = None) -> Dict[str, Any]:
        """Obtener resumen de pagos"""
        try:
            query = Payment.query
            
            # Aplicar filtros de fecha
            if start_date:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                query = query.filter(Payment.created_at >= start_dt)
            
            if end_date:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                query = query.filter(Payment.created_at <= end_dt)
            
            # Aplicar filtro de paciente
            if patient_id:
                query = query.filter(Payment.patient_id == patient_id)
            
            payments = query.all()
            
            # Calcular estadísticas
            total_amount = sum(p.amount for p in payments)
            total_count = len(payments)
            
            # Agrupar por estado
            status_summary = {}
            for payment in payments:
                status = payment.status
                if status not in status_summary:
                    status_summary[status] = {'count': 0, 'amount': 0}
                status_summary[status]['count'] += 1
                status_summary[status]['amount'] += payment.amount
            
            # Agrupar por método de pago
            method_summary = {}
            for payment in payments:
                method = payment.payment_method
                if method not in method_summary:
                    method_summary[method] = {'count': 0, 'amount': 0}
                method_summary[method]['count'] += 1
                method_summary[method]['amount'] += payment.amount
            
            return {
                'success': True,
                'summary': {
                    'total_amount': total_amount,
                    'total_count': total_count,
                    'status_summary': status_summary,
                    'method_summary': method_summary,
                    'date_range': {
                        'start_date': start_date,
                        'end_date': end_date
                    }
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener resumen: {str(e)}'
            }
    
    def get_payments_by_patient(self, patient_id: str) -> Dict[str, Any]:
        """Obtener pagos por paciente"""
        try:
            payments = Payment.query.filter_by(patient_id=patient_id).order_by(Payment.created_at.desc()).all()
            
            return {
                'success': True,
                'payments': [payment.to_dict() for payment in payments]
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener pagos del paciente: {str(e)}'
            }
