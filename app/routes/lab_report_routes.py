"""
Rutas para reportes de laboratorio
"""

from flask import Blueprint
from app.controllers.lab_report_controller import LabReportController
from app.middleware.auth_middleware import token_required

# Crear blueprint
lab_report_bp = Blueprint('lab_reports', __name__, url_prefix='/api/reports')

# Instanciar controlador
controller = LabReportController()


@lab_report_bp.route('', methods=['POST'])
@token_required
def create_report():
    """
    POST /api/reports
    Crear nuevo reporte
    
    Body:
    {
        "order_number": "ORD-001",
        "patient_name": "Juan Pérez",
        "patient_age": 35,
        "patient_gender": "M",
        "doctor_name": "Dr. García",
        "reception_date": "2024-01-15",
        "html_content": "<html>...</html>",
        "selected_tests": [
            {
                "name": "Hemograma",
                "filename": "hematologia.html"
            }
        ],
        "status": "draft"
    }
    
    Response:
    {
        "success": true,
        "message": "Reporte creado exitosamente",
        "data": { ... }
    }
    """
    return controller.create_report()


@lab_report_bp.route('/<int:report_id>', methods=['PUT'])
@token_required
def update_report(report_id):
    """
    PUT /api/reports/{id}
    Actualizar reporte existente
    
    Body:
    {
        "patient_name": "Juan Pérez Actualizado",
        "html_content": "<html>...</html>",
        "status": "final"
    }
    
    Response:
    {
        "success": true,
        "message": "Reporte actualizado exitosamente",
        "data": { ... }
    }
    """
    return controller.update_report(report_id)


@lab_report_bp.route('/<int:report_id>', methods=['GET'])
@token_required
def get_report(report_id):
    """
    GET /api/reports/{id}
    Obtener reporte por ID
    
    Query Parameters:
    - include_html: true/false (default: true)
    
    Response:
    {
        "success": true,
        "data": { ... }
    }
    """
    return controller.get_report(report_id)


@lab_report_bp.route('/patient/<string:patient_name>', methods=['GET'])
@token_required
def get_reports_by_patient(patient_name):
    """
    GET /api/reports/patient/{patient_name}
    Buscar reportes por nombre de paciente
    
    Query Parameters:
    - limit: número máximo de resultados (default: 50, max: 100)
    - include_html: true/false (default: false)
    
    Response:
    {
        "success": true,
        "data": [ ... ],
        "count": 5
    }
    """
    return controller.get_reports_by_patient(patient_name)


@lab_report_bp.route('/date-range', methods=['GET'])
@token_required
def get_reports_by_date_range():
    """
    GET /api/reports/date-range
    Buscar reportes por rango de fechas
    
    Query Parameters:
    - start_date: YYYY-MM-DD (required)
    - end_date: YYYY-MM-DD (required)
    - include_html: true/false (default: false)
    
    Response:
    {
        "success": true,
        "data": [ ... ],
        "count": 10,
        "date_range": {
            "start_date": "2024-01-01",
            "end_date": "2024-01-31"
        }
    }
    """
    return controller.get_reports_by_date_range()


@lab_report_bp.route('/stats', methods=['GET'])
@token_required
def get_reports_stats():
    """
    GET /api/reports/stats
    Obtener estadísticas de reportes
    
    Response:
    {
        "success": true,
        "data": {
            "reports": {
                "total_reports": 150,
                "unique_patients": 120,
                "unique_doctors": 15,
                "draft_reports": 25,
                "final_reports": 100,
                "printed_reports": 25
            },
            "system": {
                "permissions": { ... },
                "backup_enabled": true,
                "max_file_size": 10485760
            }
        }
    }
    """
    return controller.get_reports_stats()


@lab_report_bp.route('/<int:report_id>', methods=['DELETE'])
@token_required
def delete_report(report_id):
    """
    DELETE /api/reports/{id}
    Eliminar reporte (solo reportes en estado 'draft')
    
    Response:
    {
        "success": true,
        "message": "Reporte eliminado exitosamente"
    }
    """
    return controller.delete_report(report_id)


@lab_report_bp.route('/<int:report_id>/file-info', methods=['GET'])
@token_required
def get_file_info(report_id):
    """
    GET /api/reports/{id}/file-info
    Obtener información del archivo del reporte
    
    Response:
    {
        "success": true,
        "data": {
            "file_path": "/path/to/file.html",
            "file_name": "ORD-001_Juan_Perez_20240115_143022.html",
            "file_exists": true,
            "file_size": 1024,
            "created_at": "2024-01-15T14:30:22",
            "updated_at": "2024-01-15T14:30:22"
        }
    }
    """
    return controller.get_file_info(report_id)


@lab_report_bp.route('/backup', methods=['POST'])
@token_required
def create_backup():
    """
    POST /api/reports/backup
    Crear backup de reportes
    
    Query Parameters:
    - date: YYYY-MM-DD (opcional, default: hoy)
    
    Response:
    {
        "success": true,
        "message": "Backup creado exitosamente",
        "data": {
            "backup_path": "/path/to/backup.zip",
            "backup_date": "2024-01-15"
        }
    }
    """
    return controller.create_backup()


@lab_report_bp.route('/backup/cleanup', methods=['DELETE'])
@token_required
def cleanup_backups():
    """
    DELETE /api/reports/backup/cleanup
    Limpiar backups antiguos
    
    Response:
    {
        "success": true,
        "message": "Limpieza completada: 5 archivos eliminados",
        "data": {
            "deleted_count": 5
        }
    }
    """
    return controller.cleanup_backups()


@lab_report_bp.route('/system/validate', methods=['GET'])
@token_required
def validate_system():
    """
    GET /api/reports/system/validate
    Validar sistema de archivos
    
    Response:
    {
        "success": true,
        "data": {
            "is_valid": true,
            "permissions": {
                "base_directory_exists": true,
                "base_directory_readable": true,
                "base_directory_writable": true,
                "sufficient_space": true,
                "free_space_bytes": 1073741824
            },
            "base_directory": "/path/to/reports",
            "backup_enabled": true
        }
    }
    """
    return controller.validate_system()


# Rutas adicionales para funcionalidades específicas

@lab_report_bp.route('/<int:report_id>/status', methods=['PATCH'])
@token_required
def update_report_status(report_id):
    """
    PATCH /api/reports/{id}/status
    Actualizar solo el estado del reporte
    
    Body:
    {
        "status": "final"
    }
    
    Response:
    {
        "success": true,
        "message": "Estado actualizado exitosamente",
        "data": { ... }
    }
    """
    try:
        from flask import request, jsonify
        
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({
                'error': 'VALIDATION_ERROR',
                'message': 'Campo status es requerido'
            }), 400
        
        # Actualizar solo el estado
        update_data = {'status': data['status']}
        return controller.update_report(report_id)
        
    except Exception as e:
        return jsonify({
            'error': 'INTERNAL_ERROR',
            'message': 'Error interno del servidor'
        }), 500


@lab_report_bp.route('/search', methods=['GET'])
@token_required
def search_reports():
    """
    GET /api/reports/search
    Búsqueda avanzada de reportes
    
    Query Parameters:
    - q: término de búsqueda
    - order_number: número de orden
    - patient_name: nombre del paciente
    - doctor_name: nombre del doctor
    - status: estado del reporte
    - start_date: fecha de inicio
    - end_date: fecha de fin
    - limit: límite de resultados
    - include_html: true/false
    
    Response:
    {
        "success": true,
        "data": [ ... ],
        "count": 10,
        "filters": { ... }
    }
    """
    try:
        from flask import request, jsonify
        from app.models.lab_report import LabReport
        from sqlalchemy import and_, or_
        
        # Obtener parámetros de búsqueda
        search_term = request.args.get('q', '').strip()
        order_number = request.args.get('order_number', '').strip()
        patient_name = request.args.get('patient_name', '').strip()
        doctor_name = request.args.get('doctor_name', '').strip()
        status = request.args.get('status', '').strip()
        start_date_str = request.args.get('start_date', '').strip()
        end_date_str = request.args.get('end_date', '').strip()
        limit = min(int(request.args.get('limit', 50)), 100)
        include_html = request.args.get('include_html', 'false').lower() == 'true'
        
        # Construir consulta
        query = LabReport.query
        
        # Aplicar filtros
        filters = []
        
        if search_term:
            filters.append(
                or_(
                    LabReport.order_number.ilike(f'%{search_term}%'),
                    LabReport.patient_name.ilike(f'%{search_term}%'),
                    LabReport.doctor_name.ilike(f'%{search_term}%')
                )
            )
        
        if order_number:
            filters.append(LabReport.order_number.ilike(f'%{order_number}%'))
        
        if patient_name:
            filters.append(LabReport.patient_name.ilike(f'%{patient_name}%'))
        
        if doctor_name:
            filters.append(LabReport.doctor_name.ilike(f'%{doctor_name}%'))
        
        if status:
            filters.append(LabReport.status == status)
        
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                filters.append(LabReport.reception_date >= start_date)
            except ValueError:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': 'Formato de fecha de inicio inválido'
                }), 400
        
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                filters.append(LabReport.reception_date <= end_date)
            except ValueError:
                return jsonify({
                    'error': 'VALIDATION_ERROR',
                    'message': 'Formato de fecha de fin inválido'
                }), 400
        
        # Aplicar filtros
        if filters:
            query = query.filter(and_(*filters))
        
        # Ordenar y limitar
        reports = query.order_by(LabReport.created_at.desc()).limit(limit).all()
        
        # Convertir a diccionarios
        reports_data = []
        for report in reports:
            if include_html:
                reports_data.append(report.to_dict())
            else:
                reports_data.append(report.to_dict_summary())
        
        # Respuesta
        return jsonify({
            'success': True,
            'data': reports_data,
            'count': len(reports_data),
            'filters': {
                'search_term': search_term,
                'order_number': order_number,
                'patient_name': patient_name,
                'doctor_name': doctor_name,
                'status': status,
                'start_date': start_date_str,
                'end_date': end_date_str,
                'limit': limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'INTERNAL_ERROR',
            'message': 'Error interno del servidor'
        }), 500


@lab_report_bp.route('/recent', methods=['GET'])
@token_required
def get_recent_reports():
    """
    GET /api/reports/recent
    Obtener reportes recientes
    
    Query Parameters:
    - limit: número de reportes (default: 10, max: 50)
    - include_html: true/false (default: false)
    
    Response:
    {
        "success": true,
        "data": [ ... ],
        "count": 10
    }
    """
    try:
        from flask import request, jsonify
        from app.models.lab_report import LabReport
        
        # Obtener parámetros
        limit = min(int(request.args.get('limit', 10)), 50)
        include_html = request.args.get('include_html', 'false').lower() == 'true'
        
        # Obtener reportes recientes
        reports = LabReport.query.order_by(
            LabReport.created_at.desc()
        ).limit(limit).all()
        
        # Convertir a diccionarios
        reports_data = []
        for report in reports:
            if include_html:
                reports_data.append(report.to_dict())
            else:
                reports_data.append(report.to_dict_summary())
        
        # Respuesta
        return jsonify({
            'success': True,
            'data': reports_data,
            'count': len(reports_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'INTERNAL_ERROR',
            'message': 'Error interno del servidor'
        }), 500













