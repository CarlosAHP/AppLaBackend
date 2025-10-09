"""
Servicio para manejo de archivos HTML del frontend
"""

import os
import json
import shutil
import zipfile
from datetime import datetime
from typing import List, Dict, Optional, Any
from app.config import Config

class FrontendHTMLService:
    """Servicio para manejo de archivos HTML del frontend"""
    
    def __init__(self, config: Config):
        self.config = config
        self.html_base_path = config.FRONTEND_HTML_BASE_PATH
        self.max_file_size = config.FRONTEND_HTML_MAX_FILE_SIZE
        self.allowed_extensions = config.FRONTEND_HTML_ALLOWED_EXTENSIONS
        self.backup_enabled = config.FRONTEND_HTML_BACKUP_ENABLED
        
        # Crear directorio base si no existe
        self._ensure_base_directory()
    
    def _ensure_base_directory(self):
        """Asegurar que el directorio base existe"""
        if not os.path.exists(self.html_base_path):
            os.makedirs(self.html_base_path, exist_ok=True)
    
    def create_directory_structure(self) -> str:
        """Crear estructura de directorios por fecha (YYYY/MM)"""
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        
        directory_path = os.path.join(self.html_base_path, year, month)
        os.makedirs(directory_path, exist_ok=True)
        
        return directory_path
    
    def generate_file_name(self, original_filename: str, prefix: str = "frontend") -> str:
        """Generar nombre único para el archivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        
        # Obtener extensión
        _, ext = os.path.splitext(original_filename)
        if not ext:
            ext = ".html"
        
        return f"{prefix}_{original_filename}_{timestamp}_{unique_id}{ext}"
    
    def validate_html_content(self, html_content: str) -> bool:
        """Validar contenido HTML"""
        if len(html_content) > self.max_file_size:
            raise ValueError(f"El contenido HTML excede el tamaño máximo de {self.max_file_size} bytes")
        
        if not html_content.strip():
            raise ValueError("El contenido HTML no puede estar vacío")
        
        return True
    
    def save_html_file(self, html_content: str, file_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Guardar archivo HTML con metadatos"""
        try:
            # Validar contenido
            self.validate_html_content(html_content)
            
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Crear HTML completo con metadatos embebidos
            full_html = self._create_full_html(html_content, metadata)
            
            # Guardar archivo HTML
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            # Preparar metadatos para guardar - procesar todos los campos del frontend
            meta_data = {
                # Campos básicos del frontend
                'patient_name': metadata.get('patient_name'),
                'order_number': metadata.get('order_number'),
                'doctor_name': metadata.get('doctor_name'),
                'notes': metadata.get('notes', ''),
                
                # Campos adicionales del frontend
                'patient_age': metadata.get('patient_age'),
                'patient_gender': metadata.get('patient_gender'),
                'reception_date': metadata.get('reception_date'),
                'tests': metadata.get('tests', []),
                'created_by': metadata.get('created_by'),
                'source': metadata.get('source', 'frontend'),
                'prefix': metadata.get('prefix', 'frontend'),
                'original_filename': metadata.get('original_filename'),
                
                # Campos del sistema
                'uploaded_at': datetime.now().isoformat(),
                'file_size': len(full_html),
                'status': metadata.get('status', 'pending'),  # Estado por defecto
                'created_at': metadata.get('created_at', datetime.now().isoformat()),  # Usar el del frontend o crear uno nuevo
                
                # Nuevos campos de edición
                'edit_count': metadata.get('edit_count', 0),  # Número de veces editado
                'is_modified': metadata.get('is_modified', False),  # Boolean que indica si fue modificado
                'edit_history': metadata.get('edit_history', []),  # Array con historial de ediciones
                'last_edit_date': metadata.get('last_edit_date')  # Fecha de la última edición
            }
            
            # Filtrar valores None para mantener solo los campos válidos
            meta_data = {k: v for k, v in meta_data.items() if v is not None}
            
            # Guardar metadatos
            meta_file_path = f"{file_path}.meta"
            with open(meta_file_path, 'w', encoding='utf-8') as f:
                json.dump(meta_data, f, indent=2, ensure_ascii=False)
            
            # Crear backup si está habilitado
            if self.backup_enabled:
                self._create_backup(file_path)
            
            return {
                'filename': os.path.basename(file_path),
                'file_path': file_path,
                'size': len(full_html),
                'uploaded_at': meta_data['uploaded_at'],
                'metadata': meta_data
            }
            
        except Exception as e:
            raise Exception(f"Error al guardar archivo HTML: {str(e)}")
    
    def _create_full_html(self, html_content: str, metadata: Dict[str, Any]) -> str:
        """Crear HTML completo con metadatos embebidos"""
        # Crear comentario con metadatos
        meta_comment = f"""
<!-- 
Frontend HTML Metadata:
{json.dumps(metadata, indent=2, ensure_ascii=False)}
-->
"""
        
        # Insertar metadatos al inicio del HTML
        if html_content.strip().startswith('<!DOCTYPE') or html_content.strip().startswith('<html'):
            # Insertar después de la declaración DOCTYPE o al inicio
            if html_content.strip().startswith('<!DOCTYPE'):
                lines = html_content.split('\n')
                lines.insert(1, meta_comment)
                return '\n'.join(lines)
            else:
                return meta_comment + html_content
        else:
            # Envolver en estructura HTML básica
            return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Laboratorio</title>
    {meta_comment}
</head>
<body>
{html_content}
</body>
</html>"""
    
    def get_html_content(self, file_path: str) -> str:
        """Obtener contenido HTML de un archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error al leer archivo HTML: {str(e)}")
    
    def get_file_metadata(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Obtener metadatos de un archivo"""
        meta_file_path = f"{file_path}.meta"
        try:
            if os.path.exists(meta_file_path):
                with open(meta_file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            raise Exception(f"Error al leer metadatos: {str(e)}")
    
    def list_html_files(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Listar archivos HTML con metadatos"""
        files = []
        
        try:
            # Recorrer directorios por fecha
            for year in os.listdir(self.html_base_path):
                year_path = os.path.join(self.html_base_path, year)
                if not os.path.isdir(year_path):
                    continue
                
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if not os.path.isdir(month_path):
                        continue
                    
                    # Buscar archivos HTML
                    for filename in os.listdir(month_path):
                        if filename.endswith('.html') and not filename.endswith('.meta'):
                            file_path = os.path.join(month_path, filename)
                            
                            # Obtener información del archivo
                            stat = os.stat(file_path)
                            metadata = self.get_file_metadata(file_path) or {}
                            
                            files.append({
                                'filename': filename,
                                'file_path': file_path,
                                'size': stat.st_size,
                                'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                                'modified_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                'metadata': metadata
                            })
            
            # Ordenar por fecha de modificación (más recientes primero)
            files.sort(key=lambda x: x['modified_at'], reverse=True)
            
            return files[offset:offset + limit]
            
        except Exception as e:
            raise Exception(f"Error al listar archivos: {str(e)}")
    
    def update_html_file(self, file_path: str, html_content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar archivo HTML existente"""
        try:
            # Validar contenido
            self.validate_html_content(html_content)
            
            # Crear HTML completo con metadatos embebidos
            full_html = self._create_full_html(html_content, metadata)
            
            # Guardar archivo HTML
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            # Obtener metadatos existentes
            existing_metadata = self.get_file_metadata(file_path) or {}
            
            # Crear entrada de historial de edición
            edit_entry = {
                'edit_date': datetime.now().isoformat(),
                'edited_by': metadata.get('edited_by', existing_metadata.get('created_by', 'unknown')),
                'edit_reason': metadata.get('edit_reason', 'Actualización de contenido'),
                'file_size_before': existing_metadata.get('file_size', 0),
                'file_size_after': len(full_html),
                'changes_summary': metadata.get('changes_summary', 'Contenido HTML actualizado')
            }
            
            # Actualizar metadatos con información de edición
            existing_metadata.update(metadata)
            existing_metadata.update({
                'updated_at': datetime.now().isoformat(),
                'file_size': len(full_html),
                'edit_count': existing_metadata.get('edit_count', 0) + 1,
                'is_modified': True,
                'last_edit_date': edit_entry['edit_date']
            })
            
            # Agregar entrada al historial de ediciones
            edit_history = existing_metadata.get('edit_history', [])
            edit_history.append(edit_entry)
            existing_metadata['edit_history'] = edit_history
            
            # Guardar metadatos actualizados
            meta_file_path = f"{file_path}.meta"
            with open(meta_file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_metadata, f, indent=2, ensure_ascii=False)
            
            return {
                'filename': os.path.basename(file_path),
                'file_path': file_path,
                'size': len(full_html),
                'updated_at': existing_metadata['updated_at'],
                'edit_count': existing_metadata['edit_count'],
                'is_modified': existing_metadata['is_modified'],
                'last_edit_date': existing_metadata['last_edit_date'],
                'metadata': existing_metadata
            }
            
        except Exception as e:
            raise Exception(f"Error al actualizar archivo HTML: {str(e)}")
    
    def delete_html_file(self, file_path: str) -> bool:
        """Eliminar archivo HTML y sus metadatos"""
        try:
            # Eliminar archivo HTML
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Eliminar archivo de metadatos
            meta_file_path = f"{file_path}.meta"
            if os.path.exists(meta_file_path):
                os.remove(meta_file_path)
            
            return True
            
        except Exception as e:
            raise Exception(f"Error al eliminar archivo: {str(e)}")
    
    def search_html_files(self, query: str = None, patient_name: str = None, 
                         order_number: str = None, doctor_name: str = None,
                         status: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Buscar archivos HTML con filtros"""
        all_files = self.list_html_files(limit=1000)  # Obtener todos los archivos
        filtered_files = []
        
        for file_info in all_files:
            metadata = file_info.get('metadata', {})
            
            # Aplicar filtros
            if query and query.lower() not in file_info['filename'].lower():
                continue
            
            if patient_name and patient_name.lower() not in metadata.get('patient_name', '').lower():
                continue
            
            if order_number and order_number.lower() not in metadata.get('order_number', '').lower():
                continue
            
            if doctor_name and doctor_name.lower() not in metadata.get('doctor_name', '').lower():
                continue
            
            if status and metadata.get('status') != status:
                continue
            
            filtered_files.append(file_info)
        
        return filtered_files[:limit]
    
    def backup_html_files(self) -> str:
        """Crear backup de archivos HTML"""
        try:
            backup_dir = os.path.join(self.html_base_path, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"frontend_html_backup_{timestamp}.zip"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(self.html_base_path):
                    # Excluir directorio de backups
                    if 'backups' in dirs:
                        dirs.remove('backups')
                    
                    for file in files:
                        if file.endswith('.html') or file.endswith('.meta'):
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, self.html_base_path)
                            zipf.write(file_path, arcname)
            
            return backup_path
            
        except Exception as e:
            raise Exception(f"Error al crear backup: {str(e)}")
    
    def cleanup_old_backups(self, days: int = 30):
        """Limpiar backups antiguos"""
        try:
            backup_dir = os.path.join(self.html_base_path, 'backups')
            if not os.path.exists(backup_dir):
                return
            
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            for filename in os.listdir(backup_dir):
                if filename.endswith('.zip'):
                    file_path = os.path.join(backup_dir, filename)
                    if os.path.getmtime(file_path) < cutoff_date:
                        os.remove(file_path)
                        
        except Exception as e:
            raise Exception(f"Error al limpiar backups: {str(e)}")
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Obtener información detallada de un archivo"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError("Archivo no encontrado")
            
            stat = os.stat(file_path)
            metadata = self.get_file_metadata(file_path) or {}
            
            return {
                'filename': os.path.basename(file_path),
                'file_path': file_path,
                'size': stat.st_size,
                'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'metadata': metadata
            }
            
        except Exception as e:
            raise Exception(f"Error al obtener información del archivo: {str(e)}")
    
    def validate_file_permissions(self) -> Dict[str, Any]:
        """Validar permisos del sistema de archivos"""
        try:
            # Verificar permisos de escritura
            test_file = os.path.join(self.html_base_path, 'test_permissions.tmp')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            
            # Verificar espacio disponible
            stat = os.statvfs(self.html_base_path) if hasattr(os, 'statvfs') else None
            free_space = stat.f_frsize * stat.f_bavail if stat else None
            
            return {
                'writable': True,
                'free_space': free_space,
                'base_path': self.html_base_path
            }
            
        except Exception as e:
            return {
                'writable': False,
                'error': str(e),
                'base_path': self.html_base_path
            }
    
    # Métodos específicos para manejo de estados
    
    def update_file_status(self, file_path: str, new_status: str) -> Dict[str, Any]:
        """Actualizar el estado de un archivo"""
        try:
            if new_status not in ['pending', 'completed', 'cancelled']:
                raise ValueError("Estado inválido. Debe ser: pending, completed, o cancelled")
            
            # Obtener metadatos actuales
            metadata = self.get_file_metadata(file_path)
            if not metadata:
                raise FileNotFoundError("Metadatos no encontrados")
            
            # Actualizar estado y timestamps
            metadata['status'] = new_status
            metadata['updated_at'] = datetime.now().isoformat()
            
            if new_status == 'completed':
                metadata['completed_at'] = datetime.now().isoformat()
            elif new_status == 'cancelled':
                metadata['cancelled_at'] = datetime.now().isoformat()
            
            # Guardar metadatos actualizados
            meta_file_path = f"{file_path}.meta"
            with open(meta_file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return {
                'filename': os.path.basename(file_path),
                'status': new_status,
                'updated_at': metadata['updated_at'],
                'metadata': metadata
            }
            
        except Exception as e:
            raise Exception(f"Error al actualizar estado: {str(e)}")
    
    def get_pending_files(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtener archivos pendientes ordenados por fecha de creación (más antiguos primero)"""
        try:
            all_files = self.list_html_files(limit=1000)
            pending_files = []
            
            for file_info in all_files:
                metadata = file_info.get('metadata', {})
                if metadata.get('status') == 'pending':
                    pending_files.append(file_info)
            
            # Ordenar por fecha de creación (más antiguos primero)
            pending_files.sort(key=lambda x: x.get('metadata', {}).get('created_at', x.get('created_at', '')), reverse=False)
            
            return pending_files[:limit]
            
        except Exception as e:
            raise Exception(f"Error al obtener archivos pendientes: {str(e)}")
    
    def get_completed_files(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtener archivos completados ordenados por fecha de finalización (más recientes primero)"""
        try:
            all_files = self.list_html_files(limit=1000)
            completed_files = []
            
            for file_info in all_files:
                metadata = file_info.get('metadata', {})
                if metadata.get('status') == 'completed':
                    completed_files.append(file_info)
            
            # Ordenar por fecha de finalización (más recientes primero)
            completed_files.sort(key=lambda x: x.get('metadata', {}).get('completed_at', ''), reverse=True)
            
            return completed_files[:limit]
            
        except Exception as e:
            raise Exception(f"Error al obtener archivos completados: {str(e)}")
    
    def get_files_by_status(self, status: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtener archivos por estado específico"""
        try:
            all_files = self.list_html_files(limit=1000)
            filtered_files = []
            
            for file_info in all_files:
                metadata = file_info.get('metadata', {})
                if metadata.get('status') == status:
                    filtered_files.append(file_info)
            
            # Ordenar según el estado
            if status == 'pending':
                # Pendientes: más antiguos primero
                filtered_files.sort(key=lambda x: x.get('metadata', {}).get('created_at', x.get('created_at', '')), reverse=False)
            elif status == 'completed':
                # Completados: más recientes primero
                filtered_files.sort(key=lambda x: x.get('metadata', {}).get('completed_at', ''), reverse=True)
            else:
                # Otros estados: por fecha de modificación
                filtered_files.sort(key=lambda x: x.get('modified_at', ''), reverse=True)
            
            return filtered_files[:limit]
            
        except Exception as e:
            raise Exception(f"Error al obtener archivos por estado: {str(e)}")
    
    def get_status_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas por estado"""
        try:
            all_files = self.list_html_files(limit=1000)
            stats = {
                'total_files': len(all_files),
                'by_status': {
                    'pending': 0,
                    'completed': 0,
                    'cancelled': 0,
                    'unknown': 0
                },
                'pending_count': 0,
                'completed_count': 0,
                'cancelled_count': 0
            }
            
            for file_info in all_files:
                metadata = file_info.get('metadata', {})
                status = metadata.get('status', 'unknown')
                
                if status in stats['by_status']:
                    stats['by_status'][status] += 1
                
                if status == 'pending':
                    stats['pending_count'] += 1
                elif status == 'completed':
                    stats['completed_count'] += 1
                elif status == 'cancelled':
                    stats['cancelled_count'] += 1
            
            return stats
            
        except Exception as e:
            raise Exception(f"Error al obtener estadísticas: {str(e)}")
    
    def _create_backup(self, file_path: str):
        """Crear backup de un archivo específico"""
        try:
            backup_dir = os.path.join(self.html_base_path, 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            # Crear backup del archivo individual
            filename = os.path.basename(file_path)
            backup_filename = f"backup_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            shutil.copy2(file_path, backup_path)
            
        except Exception as e:
            # No fallar si el backup no se puede crear
            print(f"Warning: No se pudo crear backup: {str(e)}")
    
    # Métodos específicos para manejo de ediciones
    
    def get_edit_history(self, file_path: str) -> List[Dict[str, Any]]:
        """Obtener historial de ediciones de un archivo"""
        try:
            metadata = self.get_file_metadata(file_path)
            if not metadata:
                return []
            
            return metadata.get('edit_history', [])
            
        except Exception as e:
            raise Exception(f"Error al obtener historial de ediciones: {str(e)}")
    
    def get_edit_stats(self, file_path: str) -> Dict[str, Any]:
        """Obtener estadísticas de edición de un archivo"""
        try:
            metadata = self.get_file_metadata(file_path)
            if not metadata:
                return {
                    'edit_count': 0,
                    'is_modified': False,
                    'last_edit_date': None,
                    'edit_history': []
                }
            
            return {
                'edit_count': metadata.get('edit_count', 0),
                'is_modified': metadata.get('is_modified', False),
                'last_edit_date': metadata.get('last_edit_date'),
                'edit_history': metadata.get('edit_history', [])
            }
            
        except Exception as e:
            raise Exception(f"Error al obtener estadísticas de edición: {str(e)}")
    
    def mark_as_modified(self, file_path: str, edited_by: str = None, edit_reason: str = None) -> Dict[str, Any]:
        """Marcar un archivo como modificado sin cambiar el contenido"""
        try:
            metadata = self.get_file_metadata(file_path)
            if not metadata:
                raise FileNotFoundError("Metadatos no encontrados")
            
            # Crear entrada de historial de edición
            edit_entry = {
                'edit_date': datetime.now().isoformat(),
                'edited_by': edited_by or metadata.get('created_by', 'unknown'),
                'edit_reason': edit_reason or 'Archivo marcado como modificado',
                'file_size_before': metadata.get('file_size', 0),
                'file_size_after': metadata.get('file_size', 0),
                'changes_summary': 'Archivo marcado como modificado sin cambios de contenido'
            }
            
            # Actualizar metadatos
            metadata.update({
                'updated_at': datetime.now().isoformat(),
                'edit_count': metadata.get('edit_count', 0) + 1,
                'is_modified': True,
                'last_edit_date': edit_entry['edit_date']
            })
            
            # Agregar entrada al historial de ediciones
            edit_history = metadata.get('edit_history', [])
            edit_history.append(edit_entry)
            metadata['edit_history'] = edit_history
            
            # Guardar metadatos actualizados
            meta_file_path = f"{file_path}.meta"
            with open(meta_file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return {
                'filename': os.path.basename(file_path),
                'edit_count': metadata['edit_count'],
                'is_modified': metadata['is_modified'],
                'last_edit_date': metadata['last_edit_date'],
                'edit_entry': edit_entry
            }
            
        except Exception as e:
            raise Exception(f"Error al marcar archivo como modificado: {str(e)}")
    
    def reset_edit_tracking(self, file_path: str) -> Dict[str, Any]:
        """Resetear el seguimiento de ediciones de un archivo"""
        try:
            metadata = self.get_file_metadata(file_path)
            if not metadata:
                raise FileNotFoundError("Metadatos no encontrados")
            
            # Resetear campos de edición
            metadata.update({
                'updated_at': datetime.now().isoformat(),
                'edit_count': 0,
                'is_modified': False,
                'last_edit_date': None,
                'edit_history': []
            })
            
            # Guardar metadatos actualizados
            meta_file_path = f"{file_path}.meta"
            with open(meta_file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return {
                'filename': os.path.basename(file_path),
                'edit_count': 0,
                'is_modified': False,
                'last_edit_date': None,
                'edit_history': []
            }
            
        except Exception as e:
            raise Exception(f"Error al resetear seguimiento de ediciones: {str(e)}")
    
    def get_modified_files(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtener archivos que han sido modificados"""
        try:
            all_files = self.list_html_files(limit=1000)
            modified_files = []
            
            for file_info in all_files:
                metadata = file_info.get('metadata', {})
                if metadata.get('is_modified', False):
                    modified_files.append(file_info)
            
            # Ordenar por fecha de última edición (más recientes primero)
            modified_files.sort(key=lambda x: x.get('metadata', {}).get('last_edit_date', ''), reverse=True)
            
            return modified_files[:limit]
            
        except Exception as e:
            raise Exception(f"Error al obtener archivos modificados: {str(e)}")
    
    def get_edit_stats_summary(self) -> Dict[str, Any]:
        """Obtener resumen de estadísticas de edición de todos los archivos"""
        try:
            all_files = self.list_html_files(limit=1000)
            stats = {
                'total_files': len(all_files),
                'modified_files': 0,
                'unmodified_files': 0,
                'total_edits': 0,
                'average_edits_per_file': 0,
                'most_edited_file': None,
                'recent_edits': []
            }
            
            max_edits = 0
            recent_edits = []
            
            for file_info in all_files:
                metadata = file_info.get('metadata', {})
                edit_count = metadata.get('edit_count', 0)
                is_modified = metadata.get('is_modified', False)
                last_edit_date = metadata.get('last_edit_date')
                
                if is_modified:
                    stats['modified_files'] += 1
                else:
                    stats['unmodified_files'] += 1
                
                stats['total_edits'] += edit_count
                
                if edit_count > max_edits:
                    max_edits = edit_count
                    stats['most_edited_file'] = {
                        'filename': file_info['filename'],
                        'edit_count': edit_count,
                        'last_edit_date': last_edit_date
                    }
                
                if last_edit_date:
                    recent_edits.append({
                        'filename': file_info['filename'],
                        'last_edit_date': last_edit_date,
                        'edit_count': edit_count
                    })
            
            # Calcular promedio de ediciones
            if stats['total_files'] > 0:
                stats['average_edits_per_file'] = round(stats['total_edits'] / stats['total_files'], 2)
            
            # Ordenar ediciones recientes por fecha
            recent_edits.sort(key=lambda x: x['last_edit_date'], reverse=True)
            stats['recent_edits'] = recent_edits[:10]  # Últimas 10 ediciones
            
            return stats
            
        except Exception as e:
            raise Exception(f"Error al obtener resumen de estadísticas de edición: {str(e)}")