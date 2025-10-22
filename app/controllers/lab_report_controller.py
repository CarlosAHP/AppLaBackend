"""
Controlador para reportes de laboratorio
"""

import logging
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from flask import request, jsonify, current_app
from sqlalchemy.exc import IntegrityError

from app.services.lab_report_service import LabReportService
from app.config import Config
from database import db

# Configurar logging
logger = logging.getLogger(__name__)


class LabReportController:
    """Controlador para manejo de reportes de laboratorio"""
    
    def __init__(self):
        self.service = LabReportService(Config())
    
    def create_report(self) -> tuple:
        """
        POST /api/reports
        Crear nuevo reporte
        """
        try:
            # Obtener datos del request
            data = request.get_json()
            if not data:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': 'Datos JSON requeridos'
                }), 400
            
            # Obtener usuario autenticado (asumiendo que está en el token)
            created_by = getattr(request, 'user_id', None)
            if not created_by:
                return jsonify({
                    'error': 'AUTHENTICATION_ERROR',
                    'message': 'Usuario no autenticado'
                }), 401
            
            # Validar campos requeridos
            required_fields = ['order_number', 'patient_name', 'html_content', 'selected_tests']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            
            if missing_fields:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
                }), 400
            
            # Crear reporte
            lab_report = self.service.create_report(data, created_by)
            
            # Respuesta exitosa
            return jsonify({
                'success': True,
                'message': 'Reporte creado exitosamente',
                'data': lab_report.to_dict()
            }), 201
            
        except ValueError as e:
            logger.warning(f"Error de validación al crear reporte: {str(e)}")
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': str(e)
            }), 400
            
        except IntegrityError as e:
            logger.warning(f"Error de integridad al crear reporte: {str(e)}")
            return jsonify({
                'error': 'DATABASE_ERROR',
                'message': 'El número de orden ya existe'
            }), 409
            
        except PermissionError as e:
            logger.error(f"Error de permisos al crear reporte: {str(e)}")
            return jsonify({
                'error': 'PERMISSION_ERROR',
                'message': 'Sin permisos para crear archivos'
            }), 403
            
        except Exception as e:
            logger.error(f"Error inesperado al crear reporte: {str(e)}")
            return jsonify({
                'error': 'INTERNAL_ERROR',
                'message': 'Error interno del servidor'
            }), 500
    
    def update_report(self, report_id: int) -> tuple:
        """
        PUT /api/reports/{id}
        Actualizar reporte existente
        """
        try:
            # Obtener datos del request
            data = request.get_json()
            if not data:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': 'Datos JSON requeridos'
                }), 400
            
            # Actualizar reporte
            lab_report = self.service.update_report(report_id, data)
            
            # Respuesta exitosa
            return jsonify({
                'success': True,
                'message': 'Reporte actualizado exitosamente',
                'data': lab_report.to_dict()
            }), 200
            
        except ValueError as e:
            logger.warning(f"Error de validación al actualizar reporte {report_id}: {str(e)}")
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': str(e)
            }), 400
            
        except Exception as e:
            logger.error(f"Error inesperado al actualizar reporte {report_id}: {str(e)}")
            return jsonify({
                'error': 'INTERNAL_ERROR',
                'message': 'Error interno del servidor'
            }), 500
    
    def get_report(self, report_id: int) -> tuple:
        """
        GET /api/reports/{id}
        Obtener reporte por ID
        """
        try:
            # Verificar si incluir contenido HTML
            include_html = request.args.get('include_html', 'true').lower() == 'true'
            
            # Obtener reporte
            lab_report = self.service.get_report(report_id, include_html)
            
            if not lab_report:
                return jsonify({
                    'error': 'NOT_FOUND',
                    'message': f'Reporte con ID {report_id} no encontrado'
                }), 404
            
            # Respuesta exitosa
            return jsonify({
                'success': True,
                'data': lab_report.to_dict() if include_html else lab_report.to_dict_summary()
            }), 200
            
        except Exception as e:
            logger.error(f"Error inesperado al obtener reporte {report_id}: {str(e)}")
            return jsonify({
                'error': 'INTERNAL_ERROR',
                'message': 'Error interno del servidor'
            }), 500
    
    def get_reports_by_patient(self, patient_name: str) -> tuple:
        """
        GET /api/reports/patient/{patient_name}
        Buscar reportes por paciente
        """
        try:
            # Obtener parámetros de paginación
            limit = min(int(request.args.get('limit', 50)), 100)
            include_html = request.args.get('include_html', 'false').lower() == 'true'
            
            # Buscar reportes
            reports = self.service.get_reports_by_patient(patient_name, limit)
            
            # Convertir a diccionarios
            reports_data = []
            for report in reports:
                if include_html:
                    reports_data.append(report.to_dict())
                else:
                    reports_data.append(report.to_dict_summary())
            
            # Respuesta exitosa
            return jsonify({
                'success': True,
                'data': reports_data,
                'count': len(reports_data)
            }), 200
            
        except Exception as e:
            logger.error(f"Error inesperado al buscar reportes por paciente {patient_name}: {str(e)}")
            return jsonify({
                'error': 'INTERNAL_ERROR',
                'message': 'Error interno del servidor'
            }), 500
    
    def get_reports_by_date_range(self) -> tuple:
        """
        GET /api/reports/date-range
        Buscar reportes por rango de fechas
        """
        try:
            # Obtener parámetros
            start_date_str = request.args.get('start_date')
            end_date_str = request.args.get('end_date')
            include_html = request.args.get('include_html', 'false').lower() == 'true'
            
            if not start_date_str or not end_date_str:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': 'Parámetros start_date y end_date son requeridos'
                }), 400
            
            # Parsear fechas
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': 'Formato de fecha inválido. Use YYYY-MM-DD'
                }), 400
            
            # Validar rango de fechas
            if start_date > end_date:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': 'La fecha de inicio no puede ser mayor a la fecha de fin'
                }), 400
            
            # Limitar rango a máximo 1 año
            if (end_date - start_date).days > 365:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': 'El rango de fechas no puede exceder 1 año'
                }), 400
            
            # Buscar reportes
            reports = self.service.get_reports_by_date_range(start_date, end_date)
            
            # Convertir a diccionarios
            reports_data = []
            for report in reports:
                if include_html:
                    reports_data.append(report.to_dict())
                else:
                    reports_data.append(report.to_dict_summary())
            
            # Respuesta exitosa
            return jsonify({
                'success': True,
                'data': reports_data,
                'count': len(reports_data),
                'date_range': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                }
            }), 200
            
        except Exception as e:
            logger.error(f"Error inesperado al buscar reportes por rango de fechas: {str(e)}")
            return jsonify({
                'error': 'INTERNAL_ERROR',
                'message': 'Error interno del servidor'
            }), 500
    
    def get_reports_stats(self) -> tuple:
        """
        GET /api/reports/stats
        Obtener estadísticas de reportes
        """
        try:
            # Obtener estadísticas
            stats = self.service.get_reports_stats()
            
            # Obtener información adicional
            permissions = self.service.validate_file_permissions()
            
            # Respuesta exitosa
            return jsonify({
                'success': True,
                'data': {
                    'reports': stats,
                    'system': {
                        'permissions': permissions,
                        'backup_enabled': self.service.backup_enabled,
                        'max_file_size': self.service.max_file_size
                    }
                }
            }), 200
            
        except Exception as e:
            logger.error(f"Error inesperado al obtener estadísticas: {str(e)}")
            return jsonify({
                'error': 'INTERNAL_ERROR',
                'message': 'Error interno del servidor'
            }), 500
    
    def delete_report(self, report_id: int) -> tuple:
        """
        DELETE /api/reports/{id}
        Eliminar reporte
        """
        try:
            # Eliminar reporte
            success = self.service.delete_report(report_id)
            
            if not success:
                return jsonify({
                    'error': 'NOT_FOUND',
                    'message': f'Reporte con ID {report_id} no encontrado'
                }), 404
            
            # Respuesta exitosa
            return jsonify({
                'success': True,
                'message': 'Reporte eliminado exitosamente'
            }), 200
            
        except ValueError as e:
            logger.warning(f"Error de validación al eliminar reporte {report_id}: {str(e)}")
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': str(e)
            }), 400
            
        except Exception as e:
            logger.error(f"Error inesperado al eliminar reporte {report_id}: {str(e)}")
            return jsonify({
                'error': 'INTERNAL_ERROR',
                'message': 'Error interno del servidor'
            }), 500
    
    def get_file_info(self, report_id: int) -> tuple:
        """
        GET /api/reports/{id}/file-info
        Obtener información del archivo del reporte
        """
        try:
            # Obtener información del archivo
            file_info = self.service.get_file_info(report_id)
            
            # Respuesta exitosa
            return jsonify({
                'success': True,
                'data': file_info
            }), 200
            
        except ValueError as e:
            logger.warning(f"Error al obtener información del archivo {report_id}: {str(e)}")
            return jsonify({
                'error': 'NOT_FOUND',
                'message': str(e)
            }), 404
            
        except Exception as e:
            logger.error(f"Error inesperado al obtener información del archivo {report_id}: {str(e)}")
            return jsonify({
                'error': 'INTERNAL_ERROR',
                'message': 'Error interno del servidor'
            }), 500
    
    def create_backup(self) -> tuple:
        """
        POST /api/reports/backup
        Crear backup de reportes
        """
        try:
            # Obtener fecha del backup (opcional)
            backup_date_str = request.args.get('date')
            backup_date = None
            
            if backup_date_str:
                try:
                    backup_date = datetime.strptime(backup_date_str, '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({
                        'error': 'VALIDATION_ERROR',
                        'message': 'Formato de fecha inválido. Use YYYY-MM-DD'
                    }), 400
            
            # Crear backup
            backup_path = self.service.backup_reports(backup_date)
            
            # Respuesta exitosa
            return jsonify({
                'success': True,
                'message': 'Backup creado exitosamente',
                'data': {
                    'backup_path': backup_path,
                    'backup_date': backup_date.isoformat() if backup_date else date.today().isoformat()
                }
            }), 200
            
        except ValueError as e:
            logger.warning(f"Error al crear backup: {str(e)}")
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': str(e)
            }), 400
            
        except Exception as e:
            logger.error(f"Error inesperado al crear backup: {str(e)}")
            return jsonify({
                'error': 'INTERNAL_ERROR',
                'message': 'Error interno del servidor'
            }), 500
    
    def cleanup_backups(self) -> tuple:
        """
        DELETE /api/reports/backup/cleanup
        Limpiar backups antiguos
        """
        try:
            # Limpiar backups antiguos
            deleted_count = self.service.cleanup_old_backups()
            
            # Respuesta exitosa
            return jsonify({
                'success': True,
                'message': f'Limpieza completada: {deleted_count} archivos eliminados',
                'data': {
                    'deleted_count': deleted_count
                }
            }), 200
            
        except Exception as e:
            logger.error(f"Error inesperado al limpiar backups: {str(e)}")
            return jsonify({
                'error': 'INTERNAL_ERROR',
                'message': 'Error interno del servidor'
            }), 500
    
    def validate_system(self) -> tuple:
        """
        GET /api/reports/system/validate
        Validar sistema de archivos
        """
        try:
            # Validar permisos
            permissions = self.service.validate_file_permissions()
            
            # Verificar directorio base
            base_dir_exists = self.service.reports_base_path.exists()
            
            # Respuesta
            is_valid = all([
                permissions['base_directory_exists'],
                permissions['base_directory_readable'],
                permissions['base_directory_writable'],
                permissions['sufficient_space']
            ])
            
            return jsonify({
                'success': True,
                'data': {
                    'is_valid': is_valid,
                    'permissions': permissions,
                    'base_directory': str(self.service.reports_base_path),
                    'backup_enabled': self.service.backup_enabled
                }
            }), 200
            
        except Exception as e:
            logger.error(f"Error inesperado al validar sistema: {str(e)}")
            return jsonify({
                'error': 'INTERNAL_ERROR',
                'message': 'Error interno del servidor'
            }), 500













