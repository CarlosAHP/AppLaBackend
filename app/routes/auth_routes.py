"""
Rutas de Autenticación
"""

from flask import Blueprint
from app.controllers.auth_controller import AuthController
from app.middleware.auth_middleware import token_required, admin_required

# Crear Blueprint para rutas de autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Instanciar controlador
auth_controller = AuthController()


@auth_bp.route('/login', methods=['POST'])
def login():
    """Ruta para iniciar sesión"""
    return auth_controller.login()


@auth_bp.route('/register', methods=['POST'])
@admin_required
def register():
    """Ruta para registrar nuevo usuario (solo administradores)"""
    return auth_controller.register()


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """Ruta para cerrar sesión"""
    return auth_controller.logout()


@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Ruta para obtener perfil del usuario"""
    return auth_controller.get_profile()


@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Ruta para actualizar perfil del usuario"""
    return auth_controller.update_profile()


@auth_bp.route('/roles', methods=['GET'])
@token_required
def get_roles():
    """Ruta para obtener roles disponibles"""
    return auth_controller.get_roles()


@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """Ruta para verificar token"""
    return auth_controller.verify_token()
