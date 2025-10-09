"""
Rutas para manejo de archivos HTML del frontend
"""

from flask import Blueprint
from app.controllers.frontend_html_controller import FrontendHTMLController

# Crear blueprint
frontend_html_bp = Blueprint('frontend_html', __name__)

# Crear instancia del controlador
controller = FrontendHTMLController()

# Rutas básicas
@frontend_html_bp.route('/upload', methods=['POST'])
def upload_html_file():
    return controller.upload_html_file()

@frontend_html_bp.route('/list', methods=['GET'])
def list_html_files():
    return controller.list_html_files()

@frontend_html_bp.route('/file/<filename>', methods=['GET'])
def serve_html_file(filename):
    return controller.serve_html_file(filename)

@frontend_html_bp.route('/content/<filename>', methods=['GET'])
def get_html_content(filename):
    return controller.get_html_content(filename)

@frontend_html_bp.route('/file/<filename>', methods=['PUT'])
def update_html_file(filename):
    return controller.update_html_file(filename)

@frontend_html_bp.route('/file/<filename>', methods=['DELETE'])
def delete_html_file(filename):
    return controller.delete_html_file(filename)

@frontend_html_bp.route('/info/<filename>', methods=['GET'])
def get_file_info(filename):
    return controller.get_file_info(filename)

@frontend_html_bp.route('/search', methods=['GET'])
def search_html_files():
    return controller.search_html_files()

@frontend_html_bp.route('/backup', methods=['POST'])
def create_backup():
    return controller.create_backup()

@frontend_html_bp.route('/system/validate', methods=['GET'])
def validate_system():
    return controller.validate_system()

@frontend_html_bp.route('/stats', methods=['GET'])
def get_stats():
    return controller.get_stats()

@frontend_html_bp.route('/recent', methods=['GET'])
def get_recent_files():
    return controller.get_recent_files()

@frontend_html_bp.route('/download/<filename>', methods=['GET'])
def download_html_file(filename):
    return controller.download_html_file(filename)

# Rutas específicas para manejo de estados
@frontend_html_bp.route('/pending', methods=['GET'])
def get_pending_files():
    return controller.get_pending_files()

@frontend_html_bp.route('/completed', methods=['GET'])
def get_completed_files():
    return controller.get_completed_files()

@frontend_html_bp.route('/status/<status>', methods=['GET'])
def get_files_by_status(status):
    return controller.get_files_by_status(status)

@frontend_html_bp.route('/file/<filename>/status', methods=['PATCH'])
def update_file_status(filename):
    return controller.update_file_status(filename)

@frontend_html_bp.route('/status-stats', methods=['GET'])
def get_status_stats():
    return controller.get_status_stats()

# Rutas específicas para manejo de ediciones
@frontend_html_bp.route('/file/<filename>/edit-history', methods=['GET'])
def get_edit_history(filename):
    return controller.get_edit_history(filename)

@frontend_html_bp.route('/file/<filename>/edit-stats', methods=['GET'])
def get_edit_stats(filename):
    return controller.get_edit_stats(filename)

@frontend_html_bp.route('/file/<filename>/mark-modified', methods=['POST'])
def mark_as_modified(filename):
    return controller.mark_as_modified(filename)

@frontend_html_bp.route('/file/<filename>/reset-edit-tracking', methods=['POST'])
def reset_edit_tracking(filename):
    return controller.reset_edit_tracking(filename)

@frontend_html_bp.route('/modified', methods=['GET'])
def get_modified_files():
    return controller.get_modified_files()

@frontend_html_bp.route('/edit-stats-summary', methods=['GET'])
def get_edit_stats_summary():
    return controller.get_edit_stats_summary()