"""
Controlador para manejo de archivos HTML del frontend
"""

from flask import request, jsonify, send_file
from app.services.frontend_html_service import FrontendHTMLService
from app.config import Config
from app.middleware.auth_middleware import token_required
import os

class FrontendHTMLController:
    """Controlador para archivos HTML del frontend"""
    
    def __init__(self):
        self.config = Config()
        self.service = FrontendHTMLService(self.config)
    
    @token_required
    def upload_html_file(self):
        """Subir archivo HTML desde el frontend"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'No se proporcionaron datos'
                }), 400
            
            html_content = data.get('html_content')
            if not html_content:
                return jsonify({
                    'success': False,
                    'message': 'El contenido HTML es requerido'
                }), 400
            
            # Crear estructura de directorios
            directory_path = self.service.create_directory_structure()
            
            # Generar nombre de archivo
            original_filename = data.get('original_filename', 'reporte.html')
            prefix = data.get('prefix', 'frontend')
            filename = self.service.generate_file_name(original_filename, prefix)
            
            # Ruta completa del archivo
            file_path = os.path.join(directory_path, filename)
            
            # Preparar metadatos - incluir todos los campos del frontend
            metadata = {
                # Campos básicos
                'patient_name': data.get('patient_name'),
                'order_number': data.get('order_number'),
                'doctor_name': data.get('doctor_name'),
                'notes': data.get('notes', ''),
                
                # Campos adicionales del frontend
                'patient_age': data.get('patient_age'),
                'patient_gender': data.get('patient_gender'),
                'reception_date': data.get('reception_date'),
                'tests': data.get('tests', []),
                'created_by': data.get('created_by'),
                'source': data.get('source', 'frontend'),
                'prefix': data.get('prefix', 'frontend'),
                'original_filename': data.get('original_filename'),
                'created_at': data.get('created_at'),
                
                # Estado por defecto
                'status': data.get('status', 'pending'),
                
                # Nuevos campos de edición
                'edit_count': data.get('edit_count', 0),
                'is_modified': data.get('is_modified', False),
                'edit_history': data.get('edit_history', []),
                'last_edit_date': data.get('last_edit_date')
            }
            
            # Guardar archivo
            result = self.service.save_html_file(html_content, file_path, metadata)
            
            return jsonify({
                'success': True,
                'message': 'Archivo HTML subido exitosamente',
                'data': result
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al subir archivo: {str(e)}'
            }), 500
    
    @token_required
    def list_html_files(self):
        """Listar archivos HTML"""
        try:
            limit = int(request.args.get('limit', 50))
            offset = int(request.args.get('offset', 0))
            
            files = self.service.list_html_files(limit=limit, offset=offset)
            
            return jsonify({
                'success': True,
                'data': files,
                'count': len(files),
                'message': f'Se encontraron {len(files)} archivos'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al listar archivos: {str(e)}'
            }), 500
    
    @token_required
    def serve_html_file(self, filename):
        """Servir archivo HTML directamente"""
        try:
            # Buscar el archivo en la estructura de directorios
            for year in os.listdir(self.service.html_base_path):
                year_path = os.path.join(self.service.html_base_path, year)
                if not os.path.isdir(year_path):
                    continue
                
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if not os.path.isdir(month_path):
                        continue
                    
                    file_path = os.path.join(month_path, filename)
                    if os.path.exists(file_path):
                        return send_file(file_path, mimetype='text/html')
            
            return jsonify({
                'success': False,
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al servir archivo: {str(e)}'
            }), 500
    
    @token_required
    def get_html_content(self, filename):
        """Obtener contenido HTML como JSON"""
        try:
            # Buscar el archivo
            for year in os.listdir(self.service.html_base_path):
                year_path = os.path.join(self.service.html_base_path, year)
                if not os.path.isdir(year_path):
                    continue
                
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if not os.path.isdir(month_path):
                        continue
                    
                    file_path = os.path.join(month_path, filename)
                    if os.path.exists(file_path):
                        content = self.service.get_html_content(file_path)
                        metadata = self.service.get_file_metadata(file_path)
                        
                        return jsonify({
                            'success': True,
                            'data': {
                                'filename': filename,
                                'content': content,
                                'metadata': metadata
                            }
                        })
            
            return jsonify({
                'success': False,
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener contenido: {str(e)}'
            }), 500
    
    @token_required
    def update_html_file(self, filename):
        """Actualizar archivo HTML existente"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'No se proporcionaron datos'
                }), 400
            
            # Buscar el archivo
            for year in os.listdir(self.service.html_base_path):
                year_path = os.path.join(self.service.html_base_path, year)
                if not os.path.isdir(year_path):
                    continue
                
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if not os.path.isdir(month_path):
                        continue
                    
                    file_path = os.path.join(month_path, filename)
                    if os.path.exists(file_path):
                        html_content = data.get('html_content')
                        metadata = data.get('metadata', {})
                        
                        if html_content:
                            result = self.service.update_html_file(file_path, html_content, metadata)
                        else:
                            # Solo actualizar metadatos
                            existing_metadata = self.service.get_file_metadata(file_path) or {}
                            existing_metadata.update(metadata)
                            existing_metadata['updated_at'] = self.service.get_file_metadata(file_path).get('updated_at')
                            
                            meta_file_path = f"{file_path}.meta"
                            import json
                            with open(meta_file_path, 'w', encoding='utf-8') as f:
                                json.dump(existing_metadata, f, indent=2, ensure_ascii=False)
                            
                            result = {
                                'filename': filename,
                                'file_path': file_path,
                                'metadata': existing_metadata
                            }
                        
                        return jsonify({
                            'success': True,
                            'message': 'Archivo actualizado exitosamente',
                            'data': result
                        })
            
            return jsonify({
                'success': False,
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al actualizar archivo: {str(e)}'
            }), 500
    
    @token_required
    def delete_html_file(self, filename):
        """Eliminar archivo HTML"""
        try:
            # Buscar el archivo
            for year in os.listdir(self.service.html_base_path):
                year_path = os.path.join(self.service.html_base_path, year)
                if not os.path.isdir(year_path):
                    continue
                
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if not os.path.isdir(month_path):
                        continue
                    
                    file_path = os.path.join(month_path, filename)
                    if os.path.exists(file_path):
                        self.service.delete_html_file(file_path)
                        
                        return jsonify({
                            'success': True,
                            'message': 'Archivo eliminado exitosamente'
                        })
            
            return jsonify({
                'success': False,
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al eliminar archivo: {str(e)}'
            }), 500
    
    @token_required
    def get_file_info(self, filename):
        """Obtener información detallada de un archivo"""
        try:
            # Buscar el archivo
            for year in os.listdir(self.service.html_base_path):
                year_path = os.path.join(self.service.html_base_path, year)
                if not os.path.isdir(year_path):
                    continue
                
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if not os.path.isdir(month_path):
                        continue
                    
                    file_path = os.path.join(month_path, filename)
                    if os.path.exists(file_path):
                        info = self.service.get_file_info(file_path)
                        
                        return jsonify({
                            'success': True,
                            'data': info
                        })
            
            return jsonify({
                'success': False,
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener información: {str(e)}'
            }), 500
    
    @token_required
    def search_html_files(self):
        """Buscar archivos HTML con filtros"""
        try:
            query = request.args.get('query')
            patient_name = request.args.get('patient_name')
            order_number = request.args.get('order_number')
            doctor_name = request.args.get('doctor_name')
            status = request.args.get('status')
            limit = int(request.args.get('limit', 50))
            
            files = self.service.search_html_files(
                query=query,
                patient_name=patient_name,
                order_number=order_number,
                doctor_name=doctor_name,
                status=status,
                limit=limit
            )
            
            return jsonify({
                'success': True,
                'data': files,
                'count': len(files),
                'filters': {
                    'query': query,
                    'patient_name': patient_name,
                    'order_number': order_number,
                    'doctor_name': doctor_name,
                    'status': status
                },
                'message': f'Se encontraron {len(files)} archivos'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al buscar archivos: {str(e)}'
            }), 500
    
    @token_required
    def create_backup(self):
        """Crear backup de archivos HTML"""
        try:
            backup_path = self.service.backup_html_files()
            
            return jsonify({
                'success': True,
                'message': 'Backup creado exitosamente',
                'data': {
                    'backup_path': backup_path,
                    'filename': os.path.basename(backup_path)
                }
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al crear backup: {str(e)}'
            }), 500
    
    @token_required
    def validate_system(self):
        """Validar sistema de archivos"""
        try:
            validation = self.service.validate_file_permissions()
            
            return jsonify({
                'success': True,
                'data': validation
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al validar sistema: {str(e)}'
            }), 500
    
    @token_required
    def get_stats(self):
        """Obtener estadísticas generales"""
        try:
            files = self.service.list_html_files(limit=1000)
            
            total_size = sum(file_info['size'] for file_info in files)
            
            stats = {
                'total_files': len(files),
                'total_size': total_size,
                'average_size': total_size / len(files) if files else 0,
                'oldest_file': min(files, key=lambda x: x['created_at'])['created_at'] if files else None,
                'newest_file': max(files, key=lambda x: x['created_at'])['created_at'] if files else None
            }
            
            return jsonify({
                'success': True,
                'data': stats
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener estadísticas: {str(e)}'
            }), 500
    
    @token_required
    def get_recent_files(self):
        """Obtener archivos recientes"""
        try:
            limit = int(request.args.get('limit', 10))
            files = self.service.list_html_files(limit=limit)
            
            return jsonify({
                'success': True,
                'data': files,
                'count': len(files),
                'message': f'Se encontraron {len(files)} archivos recientes'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener archivos recientes: {str(e)}'
            }), 500
    
    @token_required
    def download_html_file(self, filename):
        """Descargar archivo HTML"""
        try:
            # Buscar el archivo
            for year in os.listdir(self.service.html_base_path):
                year_path = os.path.join(self.service.html_base_path, year)
                if not os.path.isdir(year_path):
                    continue
                
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if not os.path.isdir(month_path):
                        continue
                    
                    file_path = os.path.join(month_path, filename)
                    if os.path.exists(file_path):
                        return send_file(file_path, as_attachment=True, download_name=filename)
            
            return jsonify({
                'success': False,
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al descargar archivo: {str(e)}'
            }), 500
    
    # Métodos específicos para manejo de estados
    
    @token_required
    def get_pending_files(self):
        """Obtener archivos pendientes"""
        try:
            limit = int(request.args.get('limit', 50))
            files = self.service.get_pending_files(limit=limit)
            
            return jsonify({
                'success': True,
                'data': files,
                'count': len(files),
                'status': 'pending',
                'message': f'Se encontraron {len(files)} archivos pendientes'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener archivos pendientes: {str(e)}'
            }), 500
    
    @token_required
    def get_completed_files(self):
        """Obtener archivos completados"""
        try:
            limit = int(request.args.get('limit', 50))
            files = self.service.get_completed_files(limit=limit)
            
            return jsonify({
                'success': True,
                'data': files,
                'count': len(files),
                'status': 'completed',
                'message': f'Se encontraron {len(files)} archivos completados'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener archivos completados: {str(e)}'
            }), 500
    
    @token_required
    def get_files_by_status(self, status):
        """Obtener archivos por estado específico"""
        try:
            limit = int(request.args.get('limit', 50))
            files = self.service.get_files_by_status(status, limit=limit)
            
            return jsonify({
                'success': True,
                'data': files,
                'count': len(files),
                'status': status,
                'message': f'Se encontraron {len(files)} archivos con estado {status}'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener archivos por estado: {str(e)}'
            }), 500
    
    @token_required
    def update_file_status(self, filename):
        """Actualizar estado de un archivo"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'No se proporcionaron datos'
                }), 400
            
            new_status = data.get('status')
            if not new_status:
                return jsonify({
                    'success': False,
                    'message': 'El estado es requerido'
                }), 400
            
            # Buscar el archivo
            for year in os.listdir(self.service.html_base_path):
                year_path = os.path.join(self.service.html_base_path, year)
                if not os.path.isdir(year_path):
                    continue
                
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if not os.path.isdir(month_path):
                        continue
                    
                    file_path = os.path.join(month_path, filename)
                    if os.path.exists(file_path):
                        result = self.service.update_file_status(file_path, new_status)
                        
                        return jsonify({
                            'success': True,
                            'message': f'Estado del archivo {filename} actualizado a {new_status}',
                            'data': result
                        })
            
            return jsonify({
                'success': False,
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al actualizar estado: {str(e)}'
            }), 500
    
    @token_required
    def get_status_stats(self):
        """Obtener estadísticas por estado"""
        try:
            stats = self.service.get_status_stats()
            
            return jsonify({
                'success': True,
                'data': stats
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener estadísticas: {str(e)}'
            }), 500
    
    # Métodos específicos para manejo de ediciones
    
    @token_required
    def get_edit_history(self, filename):
        """Obtener historial de ediciones de un archivo"""
        try:
            # Buscar el archivo
            for year in os.listdir(self.service.html_base_path):
                year_path = os.path.join(self.service.html_base_path, year)
                if not os.path.isdir(year_path):
                    continue
                
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if not os.path.isdir(month_path):
                        continue
                    
                    file_path = os.path.join(month_path, filename)
                    if os.path.exists(file_path):
                        edit_history = self.service.get_edit_history(file_path)
                        
                        return jsonify({
                            'success': True,
                            'data': {
                                'filename': filename,
                                'edit_history': edit_history,
                                'count': len(edit_history)
                            }
                        })
            
            return jsonify({
                'success': False,
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener historial de ediciones: {str(e)}'
            }), 500
    
    @token_required
    def get_edit_stats(self, filename):
        """Obtener estadísticas de edición de un archivo"""
        try:
            # Buscar el archivo
            for year in os.listdir(self.service.html_base_path):
                year_path = os.path.join(self.service.html_base_path, year)
                if not os.path.isdir(year_path):
                    continue
                
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if not os.path.isdir(month_path):
                        continue
                    
                    file_path = os.path.join(month_path, filename)
                    if os.path.exists(file_path):
                        edit_stats = self.service.get_edit_stats(file_path)
                        
                        return jsonify({
                            'success': True,
                            'data': {
                                'filename': filename,
                                'edit_stats': edit_stats
                            }
                        })
            
            return jsonify({
                'success': False,
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener estadísticas de edición: {str(e)}'
            }), 500
    
    @token_required
    def mark_as_modified(self, filename):
        """Marcar un archivo como modificado"""
        try:
            data = request.get_json() or {}
            edited_by = data.get('edited_by')
            edit_reason = data.get('edit_reason')
            
            # Buscar el archivo
            for year in os.listdir(self.service.html_base_path):
                year_path = os.path.join(self.service.html_base_path, year)
                if not os.path.isdir(year_path):
                    continue
                
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if not os.path.isdir(month_path):
                        continue
                    
                    file_path = os.path.join(month_path, filename)
                    if os.path.exists(file_path):
                        result = self.service.mark_as_modified(file_path, edited_by, edit_reason)
                        
                        return jsonify({
                            'success': True,
                            'message': f'Archivo {filename} marcado como modificado',
                            'data': result
                        })
            
            return jsonify({
                'success': False,
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al marcar archivo como modificado: {str(e)}'
            }), 500
    
    @token_required
    def reset_edit_tracking(self, filename):
        """Resetear el seguimiento de ediciones de un archivo"""
        try:
            # Buscar el archivo
            for year in os.listdir(self.service.html_base_path):
                year_path = os.path.join(self.service.html_base_path, year)
                if not os.path.isdir(year_path):
                    continue
                
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if not os.path.isdir(month_path):
                        continue
                    
                    file_path = os.path.join(month_path, filename)
                    if os.path.exists(file_path):
                        result = self.service.reset_edit_tracking(file_path)
                        
                        return jsonify({
                            'success': True,
                            'message': f'Seguimiento de ediciones reseteado para {filename}',
                            'data': result
                        })
            
            return jsonify({
                'success': False,
                'message': 'Archivo no encontrado'
            }), 404
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al resetear seguimiento de ediciones: {str(e)}'
            }), 500
    
    @token_required
    def get_modified_files(self):
        """Obtener archivos que han sido modificados"""
        try:
            limit = int(request.args.get('limit', 50))
            files = self.service.get_modified_files(limit=limit)
            
            return jsonify({
                'success': True,
                'data': files,
                'count': len(files),
                'message': f'Se encontraron {len(files)} archivos modificados'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener archivos modificados: {str(e)}'
            }), 500
    
    @token_required
    def get_edit_stats_summary(self):
        """Obtener resumen de estadísticas de edición"""
        try:
            stats = self.service.get_edit_stats_summary()
            
            return jsonify({
                'success': True,
                'data': stats
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error al obtener resumen de estadísticas de edición: {str(e)}'
            }), 500