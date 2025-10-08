"""
Servicio de Resultados de Laboratorio
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from app.models.lab_result import LabResult
from app.services.sync_service import SyncService
from database import db


class LabResultService:
    """Servicio para manejar la lógica de resultados de laboratorio"""
    
    def __init__(self):
        self.sync_service = SyncService()
    
    def create_lab_result(self, lab_result_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nuevo resultado de laboratorio"""
        try:
            # Crear nuevo resultado
            lab_result = LabResult(
                patient_id=lab_result_data['patient_id'],
                patient_name=lab_result_data['patient_name'],
                patient_dni=lab_result_data.get('patient_dni'),
                patient_age=lab_result_data.get('patient_age'),
                patient_gender=lab_result_data.get('patient_gender'),
                exam_type=lab_result_data['exam_type'],
                exam_code=lab_result_data.get('exam_code'),
                exam_date=datetime.fromisoformat(lab_result_data['exam_date'].replace('Z', '+00:00')),
                technician_id=lab_result_data.get('technician_id'),
                doctor_id=lab_result_data.get('doctor_id'),
                status='pending'
            )
            
            # Guardar en base de datos
            db.session.add(lab_result)
            db.session.commit()
            
            # Crear log de sincronización
            self.sync_service.create_sync_log(
                sync_type='lab_result',
                entity_id=lab_result.id,
                entity_type='LabResult',
                operation='create',
                data_after=lab_result.to_dict()
            )
            
            return {
                'success': True,
                'lab_result': lab_result.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al crear resultado: {str(e)}'
            }
    
    def get_lab_results(self, page: int = 1, per_page: int = 10, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Obtener lista de resultados de laboratorio con paginación"""
        try:
            query = LabResult.query
            
            # Aplicar filtros
            if filters:
                if filters.get('patient_id'):
                    query = query.filter(LabResult.patient_id == filters['patient_id'])
                if filters.get('status'):
                    query = query.filter(LabResult.status == filters['status'])
                if filters.get('exam_type'):
                    query = query.filter(LabResult.exam_type.ilike(f"%{filters['exam_type']}%"))
            
            # Ordenar por fecha de creación descendente
            query = query.order_by(LabResult.created_at.desc())
            
            # Paginación
            pagination = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            lab_results = [result.to_dict() for result in pagination.items]
            
            return {
                'success': True,
                'lab_results': lab_results,
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
                'message': f'Error al obtener resultados: {str(e)}'
            }
    
    def get_lab_result_by_id(self, result_id: int) -> Dict[str, Any]:
        """Obtener resultado de laboratorio por ID"""
        try:
            lab_result = LabResult.query.get(result_id)
            
            if not lab_result:
                return {
                    'success': False,
                    'message': 'Resultado de laboratorio no encontrado'
                }
            
            return {
                'success': True,
                'lab_result': lab_result.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener resultado: {str(e)}'
            }
    
    def update_lab_result(self, result_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar resultado de laboratorio"""
        try:
            lab_result = LabResult.query.get(result_id)
            
            if not lab_result:
                return {
                    'success': False,
                    'message': 'Resultado de laboratorio no encontrado'
                }
            
            # Guardar datos antes de la actualización
            data_before = lab_result.to_dict()
            
            # Actualizar campos permitidos
            allowed_fields = [
                'patient_name', 'patient_dni', 'patient_age', 'patient_gender',
                'exam_type', 'exam_code', 'results', 'normal_values', 
                'observations', 'technician_id', 'doctor_id'
            ]
            
            for field in allowed_fields:
                if field in update_data:
                    if field in ['results', 'normal_values'] and isinstance(update_data[field], dict):
                        setattr(lab_result, field, update_data[field])
                    else:
                        setattr(lab_result, field, update_data[field])
            
            # Actualizar timestamp
            lab_result.updated_at = datetime.utcnow()
            
            # Guardar cambios
            db.session.commit()
            
            # Crear log de sincronización
            self.sync_service.create_sync_log(
                sync_type='lab_result',
                entity_id=lab_result.id,
                entity_type='LabResult',
                operation='update',
                data_before=data_before,
                data_after=lab_result.to_dict()
            )
            
            return {
                'success': True,
                'lab_result': lab_result.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al actualizar resultado: {str(e)}'
            }
    
    def delete_lab_result(self, result_id: int) -> Dict[str, Any]:
        """Eliminar resultado de laboratorio"""
        try:
            lab_result = LabResult.query.get(result_id)
            
            if not lab_result:
                return {
                    'success': False,
                    'message': 'Resultado de laboratorio no encontrado'
                }
            
            # Guardar datos antes de la eliminación
            data_before = lab_result.to_dict()
            
            # Eliminar de base de datos
            db.session.delete(lab_result)
            db.session.commit()
            
            # Crear log de sincronización
            self.sync_service.create_sync_log(
                sync_type='lab_result',
                entity_id=result_id,
                entity_type='LabResult',
                operation='delete',
                data_before=data_before
            )
            
            return {
                'success': True,
                'message': 'Resultado eliminado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al eliminar resultado: {str(e)}'
            }
    
    def update_lab_result_status(self, result_id: int, status: str) -> Dict[str, Any]:
        """Actualizar estado del resultado de laboratorio"""
        try:
            lab_result = LabResult.query.get(result_id)
            
            if not lab_result:
                return {
                    'success': False,
                    'message': 'Resultado de laboratorio no encontrado'
                }
            
            # Validar estado
            valid_statuses = ['pending', 'completed', 'reviewed', 'delivered']
            if status not in valid_statuses:
                return {
                    'success': False,
                    'message': f'Estado inválido. Estados válidos: {", ".join(valid_statuses)}'
                }
            
            # Guardar datos antes de la actualización
            data_before = lab_result.to_dict()
            
            # Actualizar estado
            lab_result.status = status
            
            # Si se marca como completado, establecer fecha de resultado
            if status == 'completed' and not lab_result.result_date:
                lab_result.result_date = datetime.utcnow()
            
            lab_result.updated_at = datetime.utcnow()
            
            # Guardar cambios
            db.session.commit()
            
            # Crear log de sincronización
            self.sync_service.create_sync_log(
                sync_type='lab_result',
                entity_id=lab_result.id,
                entity_type='LabResult',
                operation='update',
                data_before=data_before,
                data_after=lab_result.to_dict()
            )
            
            return {
                'success': True,
                'lab_result': lab_result.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al actualizar estado: {str(e)}'
            }
    
    def get_lab_results_by_patient(self, patient_id: str) -> Dict[str, Any]:
        """Obtener resultados de laboratorio por paciente"""
        try:
            lab_results = LabResult.query.filter_by(patient_id=patient_id).order_by(LabResult.exam_date.desc()).all()
            
            return {
                'success': True,
                'lab_results': [result.to_dict() for result in lab_results]
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener resultados del paciente: {str(e)}'
            }
