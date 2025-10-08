"""
Rutas de Sincronización
"""

from flask import Blueprint
from app.controllers.sync_controller import SyncController

# Crear Blueprint para rutas de sincronización
sync_bp = Blueprint('sync', __name__, url_prefix='/api/sync')

# Instanciar controlador
sync_controller = SyncController()


@sync_bp.route('/logs', methods=['GET'])
def get_sync_logs():
    """Ruta para obtener logs de sincronización"""
    return sync_controller.get_sync_logs()


@sync_bp.route('/logs/<int:log_id>', methods=['GET'])
def get_sync_log(log_id):
    """Ruta para obtener un log de sincronización específico"""
    return sync_controller.get_sync_log(log_id)


@sync_bp.route('/logs/<int:log_id>/retry', methods=['POST'])
def retry_sync(log_id):
    """Ruta para reintentar sincronización fallida"""
    return sync_controller.retry_sync(log_id)


@sync_bp.route('/manual', methods=['POST'])
def manual_sync():
    """Ruta para sincronización manual de datos"""
    return sync_controller.manual_sync()


@sync_bp.route('/status', methods=['GET'])
def get_sync_status():
    """Ruta para obtener estado general de sincronización"""
    return sync_controller.get_sync_status()


@sync_bp.route('/bulk', methods=['POST'])
def bulk_sync():
    """Ruta para sincronización masiva de datos"""
    return sync_controller.bulk_sync()
