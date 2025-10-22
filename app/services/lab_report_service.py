"""
Servicio para manejo de reportes de laboratorio
"""

import os
import shutil
import json
import logging
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import zipfile
import tempfile

from database import db
from app.models.lab_report import LabReport, ReportTest
from app.config import Config

# Configurar logging
logger = logging.getLogger(__name__)


class LabReportService:
    """Servicio para manejo de reportes de laboratorio"""
    
    def __init__(self, config: Config):
        self.config = config
        self.reports_base_path = Path(config.REPORTS_BASE_PATH)
        self.reports_folder = config.REPORTS_FOLDER
        self.max_file_size = config.REPORTS_MAX_FILE_SIZE
        self.backup_enabled = config.REPORTS_BACKUP_ENABLED
        self.backup_retention_days = config.REPORTS_BACKUP_RETENTION_DAYS
        
        # Crear directorio base si no existe
        self._ensure_base_directory()
    
    def _ensure_base_directory(self) -> None:
        """Asegurar que el directorio base existe"""
        try:
            self.reports_base_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directorio de reportes creado/verificado: {self.reports_base_path}")
        except Exception as e:
            logger.error(f"Error al crear directorio de reportes: {str(e)}")
            raise
    
    def create_directory_structure(self, year: int = None, month: int = None) -> str:
        """
        Crear estructura de directorios por fecha
        
        Args:
            year: Año (por defecto año actual)
            month: Mes (por defecto mes actual)
            
        Returns:
            str: Ruta del directorio creado
        """
        try:
            if year is None:
                year = datetime.now().year
            if month is None:
                month = datetime.now().month
            
            # Crear estructura: reports/YYYY/MM/
            directory_path = self.reports_base_path / str(year) / f"{month:02d}"
            directory_path.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Estructura de directorios creada: {directory_path}")
            return str(directory_path)
            
        except Exception as e:
            logger.error(f"Error al crear estructura de directorios: {str(e)}")
            raise
    
    def generate_file_name(self, order_number: str, patient_name: str, timestamp: datetime = None) -> str:
        """
        Generar nombre de archivo único
        
        Args:
            order_number: Número de orden
            patient_name: Nombre del paciente
            timestamp: Timestamp para el archivo (por defecto ahora)
            
        Returns:
            str: Nombre del archivo generado
        """
        try:
            if timestamp is None:
                timestamp = datetime.now()
            
            # Limpiar nombres para el archivo
            clean_order = order_number.replace(' ', '_').replace('/', '_')
            clean_patient = patient_name.replace(' ', '_').replace('/', '_')
            
            # Formato: ORDEN_PACIENTE_YYYYMMDD_HHMMSS.html
            date_str = timestamp.strftime("%Y%m%d_%H%M%S")
            file_name = f"{clean_order}_{clean_patient}_{date_str}.html"
            
            logger.debug(f"Nombre de archivo generado: {file_name}")
            return file_name
            
        except Exception as e:
            logger.error(f"Error al generar nombre de archivo: {str(e)}")
            raise
    
    def save_report_file(self, html_content: str, file_path: str) -> bool:
        """
        Guardar contenido HTML en archivo
        
        Args:
            html_content: Contenido HTML a guardar
            file_path: Ruta completa del archivo
            
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            # Validar tamaño del contenido
            content_size = len(html_content.encode('utf-8'))
            if content_size > self.max_file_size:
                raise ValueError(f"El contenido excede el tamaño máximo de {self.max_file_size} bytes")
            
            # Crear directorio padre si no existe
            file_path_obj = Path(file_path)
            file_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Validar que el directorio padre es seguro
            if not str(file_path_obj.parent).startswith(str(self.reports_base_path)):
                raise ValueError("Ruta de archivo no permitida")
            
            # Escribir archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Verificar que el archivo se escribió correctamente
            if not os.path.exists(file_path):
                raise Exception("El archivo no se creó correctamente")
            
            logger.info(f"Archivo guardado exitosamente: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error al guardar archivo {file_path}: {str(e)}")
            raise
    
    def create_report(self, report_data: Dict[str, Any], created_by: int) -> LabReport:
        """
        Crear nuevo reporte
        
        Args:
            report_data: Datos del reporte
            created_by: ID del usuario que crea el reporte
            
        Returns:
            LabReport: Reporte creado
        """
        try:
            # Validar datos requeridos
            required_fields = ['order_number', 'patient_name', 'html_content', 'selected_tests']
            for field in required_fields:
                if field not in report_data or not report_data[field]:
                    raise ValueError(f"Campo requerido faltante: {field}")
            
            # Verificar que el número de orden no existe
            existing_report = LabReport.get_by_order_number(report_data['order_number'])
            if existing_report:
                raise ValueError(f"Ya existe un reporte con el número de orden: {report_data['order_number']}")
            
            # Crear estructura de directorios
            directory_path = self.create_directory_structure()
            
            # Generar nombre de archivo
            file_name = self.generate_file_name(
                report_data['order_number'],
                report_data['patient_name']
            )
            
            # Ruta completa del archivo
            file_path = os.path.join(directory_path, file_name)
            
            # Guardar archivo HTML
            self.save_report_file(report_data['html_content'], file_path)
            
            # Crear objeto del reporte
            lab_report = LabReport(
                order_number=report_data['order_number'],
                patient_name=report_data['patient_name'],
                patient_age=report_data.get('patient_age'),
                patient_gender=report_data.get('patient_gender'),
                doctor_name=report_data.get('doctor_name'),
                reception_date=report_data.get('reception_date'),
                file_path=file_path,
                file_name=file_name,
                selected_tests=report_data['selected_tests'],
                html_content=report_data['html_content'],
                status=report_data.get('status', 'draft'),
                created_by=created_by
            )
            
            # Guardar en base de datos
            db.session.add(lab_report)
            db.session.flush()  # Para obtener el ID
            
            # Crear registros de pruebas si se proporcionan
            if isinstance(report_data['selected_tests'], list):
                for test_data in report_data['selected_tests']:
                    if isinstance(test_data, dict):
                        test_name = test_data.get('name', test_data.get('test_name', ''))
                        test_filename = test_data.get('filename', test_data.get('test_filename'))
                    else:
                        test_name = str(test_data)
                        test_filename = None
                    
                    if test_name:
                        report_test = ReportTest(
                            report_id=lab_report.id,
                            test_name=test_name,
                            test_filename=test_filename
                        )
                        db.session.add(report_test)
            
            db.session.commit()
            
            logger.info(f"Reporte creado exitosamente: {lab_report.order_number}")
            return lab_report
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al crear reporte: {str(e)}")
            raise
    
    def update_report(self, report_id: int, update_data: Dict[str, Any]) -> LabReport:
        """
        Actualizar reporte existente
        
        Args:
            report_id: ID del reporte
            update_data: Datos a actualizar
            
        Returns:
            LabReport: Reporte actualizado
        """
        try:
            # Buscar reporte
            lab_report = LabReport.query.get(report_id)
            if not lab_report:
                raise ValueError(f"Reporte con ID {report_id} no encontrado")
            
            # Verificar que es editable
            if not lab_report.is_editable():
                raise ValueError("El reporte no es editable en su estado actual")
            
            # Actualizar campos permitidos
            updatable_fields = [
                'patient_name', 'patient_age', 'patient_gender', 'doctor_name',
                'reception_date', 'selected_tests', 'html_content', 'status'
            ]
            
            for field in updatable_fields:
                if field in update_data:
                    setattr(lab_report, field, update_data[field])
            
            # Si se actualiza el contenido HTML, actualizar el archivo
            if 'html_content' in update_data:
                self.save_report_file(update_data['html_content'], lab_report.file_path)
            
            # Actualizar timestamp
            lab_report.updated_at = datetime.utcnow()
            
            # Actualizar pruebas si se proporcionan
            if 'selected_tests' in update_data:
                # Eliminar pruebas existentes
                ReportTest.query.filter_by(report_id=report_id).delete()
                
                # Crear nuevas pruebas
                if isinstance(update_data['selected_tests'], list):
                    for test_data in update_data['selected_tests']:
                        if isinstance(test_data, dict):
                            test_name = test_data.get('name', test_data.get('test_name', ''))
                            test_filename = test_data.get('filename', test_data.get('test_filename'))
                        else:
                            test_name = str(test_data)
                            test_filename = None
                        
                        if test_name:
                            report_test = ReportTest(
                                report_id=lab_report.id,
                                test_name=test_name,
                                test_filename=test_filename
                            )
                            db.session.add(report_test)
            
            db.session.commit()
            
            logger.info(f"Reporte actualizado exitosamente: {lab_report.order_number}")
            return lab_report
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al actualizar reporte {report_id}: {str(e)}")
            raise
    
    def get_report(self, report_id: int, include_html: bool = True) -> Optional[LabReport]:
        """
        Obtener reporte por ID
        
        Args:
            report_id: ID del reporte
            include_html: Si incluir el contenido HTML
            
        Returns:
            LabReport: Reporte encontrado o None
        """
        try:
            lab_report = LabReport.query.get(report_id)
            if lab_report and not include_html:
                # Retornar sin contenido HTML para ahorrar memoria
                return lab_report
            return lab_report
            
        except Exception as e:
            logger.error(f"Error al obtener reporte {report_id}: {str(e)}")
            raise
    
    def get_reports_by_patient(self, patient_name: str, limit: int = 50) -> List[LabReport]:
        """
        Buscar reportes por nombre de paciente
        
        Args:
            patient_name: Nombre del paciente
            limit: Límite de resultados
            
        Returns:
            List[LabReport]: Lista de reportes
        """
        try:
            return LabReport.get_by_patient_name(patient_name, limit)
            
        except Exception as e:
            logger.error(f"Error al buscar reportes por paciente {patient_name}: {str(e)}")
            raise
    
    def get_reports_by_date_range(self, start_date: date, end_date: date) -> List[LabReport]:
        """
        Buscar reportes por rango de fechas
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            List[LabReport]: Lista de reportes
        """
        try:
            return LabReport.get_by_date_range(start_date, end_date)
            
        except Exception as e:
            logger.error(f"Error al buscar reportes por rango de fechas: {str(e)}")
            raise
    
    def get_reports_stats(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de reportes
        
        Returns:
            Dict[str, Any]: Estadísticas
        """
        try:
            return LabReport.get_stats()
            
        except Exception as e:
            logger.error(f"Error al obtener estadísticas: {str(e)}")
            raise
    
    def delete_report(self, report_id: int) -> bool:
        """
        Eliminar reporte
        
        Args:
            report_id: ID del reporte
            
        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            lab_report = LabReport.query.get(report_id)
            if not lab_report:
                raise ValueError(f"Reporte con ID {report_id} no encontrado")
            
            # Verificar que es editable
            if not lab_report.is_editable():
                raise ValueError("Solo se pueden eliminar reportes en estado 'draft'")
            
            # Eliminar archivo físico
            if lab_report.file_exists():
                try:
                    os.remove(lab_report.file_path)
                    logger.info(f"Archivo eliminado: {lab_report.file_path}")
                except Exception as e:
                    logger.warning(f"No se pudo eliminar archivo {lab_report.file_path}: {str(e)}")
            
            # Eliminar de base de datos (cascade eliminará las pruebas)
            db.session.delete(lab_report)
            db.session.commit()
            
            logger.info(f"Reporte eliminado exitosamente: {lab_report.order_number}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al eliminar reporte {report_id}: {str(e)}")
            raise
    
    def backup_reports(self, backup_date: date = None) -> str:
        """
        Crear backup de reportes
        
        Args:
            backup_date: Fecha del backup (por defecto hoy)
            
        Returns:
            str: Ruta del archivo de backup creado
        """
        try:
            if not self.backup_enabled:
                raise ValueError("Backup no está habilitado")
            
            if backup_date is None:
                backup_date = date.today()
            
            # Crear directorio de backup
            backup_dir = self.reports_base_path / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            # Nombre del archivo de backup
            backup_filename = f"reports_backup_{backup_date.strftime('%Y%m%d')}.zip"
            backup_path = backup_dir / backup_filename
            
            # Crear archivo ZIP
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(self.reports_base_path):
                    # Excluir directorio de backups
                    if 'backups' in root:
                        continue
                    
                    for file in files:
                        if file.endswith('.html'):
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, self.reports_base_path)
                            zipf.write(file_path, arcname)
            
            logger.info(f"Backup creado exitosamente: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Error al crear backup: {str(e)}")
            raise
    
    def cleanup_old_backups(self) -> int:
        """
        Limpiar backups antiguos
        
        Returns:
            int: Número de archivos eliminados
        """
        try:
            if not self.backup_enabled:
                return 0
            
            backup_dir = self.reports_base_path / "backups"
            if not backup_dir.exists():
                return 0
            
            cutoff_date = date.today() - timedelta(days=self.backup_retention_days)
            deleted_count = 0
            
            for backup_file in backup_dir.glob("reports_backup_*.zip"):
                try:
                    # Extraer fecha del nombre del archivo
                    date_str = backup_file.stem.split('_')[-1]
                    backup_date = datetime.strptime(date_str, '%Y%m%d').date()
                    
                    if backup_date < cutoff_date:
                        backup_file.unlink()
                        deleted_count += 1
                        logger.info(f"Backup antiguo eliminado: {backup_file}")
                        
                except Exception as e:
                    logger.warning(f"Error al procesar backup {backup_file}: {str(e)}")
            
            logger.info(f"Limpieza de backups completada: {deleted_count} archivos eliminados")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error en limpieza de backups: {str(e)}")
            raise
    
    def get_file_info(self, report_id: int) -> Dict[str, Any]:
        """
        Obtener información del archivo del reporte
        
        Args:
            report_id: ID del reporte
            
        Returns:
            Dict[str, Any]: Información del archivo
        """
        try:
            lab_report = LabReport.query.get(report_id)
            if not lab_report:
                raise ValueError(f"Reporte con ID {report_id} no encontrado")
            
            file_info = {
                'file_path': lab_report.file_path,
                'file_name': lab_report.file_name,
                'file_exists': lab_report.file_exists(),
                'file_size': lab_report.get_file_size(),
                'created_at': lab_report.created_at.isoformat() if lab_report.created_at else None,
                'updated_at': lab_report.updated_at.isoformat() if lab_report.updated_at else None
            }
            
            return file_info
            
        except Exception as e:
            logger.error(f"Error al obtener información del archivo {report_id}: {str(e)}")
            raise
    
    def validate_file_permissions(self) -> Dict[str, bool]:
        """
        Validar permisos de archivos
        
        Returns:
            Dict[str, bool]: Estado de los permisos
        """
        try:
            permissions = {
                'base_directory_readable': os.access(self.reports_base_path, os.R_OK),
                'base_directory_writable': os.access(self.reports_base_path, os.W_OK),
                'base_directory_exists': self.reports_base_path.exists()
            }
            
            # Verificar espacio disponible
            try:
                statvfs = os.statvfs(self.reports_base_path)
                free_space = statvfs.f_frsize * statvfs.f_bavail
                permissions['sufficient_space'] = free_space > (100 * 1024 * 1024)  # 100MB mínimo
                permissions['free_space_bytes'] = free_space
            except Exception:
                permissions['sufficient_space'] = False
                permissions['free_space_bytes'] = 0
            
            return permissions
            
        except Exception as e:
            logger.error(f"Error al validar permisos: {str(e)}")
            return {
                'base_directory_readable': False,
                'base_directory_writable': False,
                'base_directory_exists': False,
                'sufficient_space': False,
                'free_space_bytes': 0
            }













