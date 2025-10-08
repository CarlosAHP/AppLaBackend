"""
Controlador de Autenticación
"""

from flask import request, jsonify
from functools import wraps
from app.services.auth_service import AuthService
from app.models.user import User


class AuthController:
    """Controlador para manejar la autenticación"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    def login(self):
        """Iniciar sesión"""
        try:
            data = request.get_json()
            
            if not data or not data.get('username') or not data.get('password'):
                return jsonify({
                    'success': False,
                    'message': 'Username y password son requeridos'
                }), 400
            
            username = data['username']
            password = data['password']
            
            result = self.auth_service.authenticate_user(username, password)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Login exitoso',
                    'data': {
                        'user': result['user'],
                        'token': result['token']
                    }
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': result['message']
                }), 401
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    def register(self):
        """Registrar nuevo usuario (solo administradores)"""
        try:
            # Verificar que el usuario que hace la petición sea administrador
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({
                    'success': False,
                    'message': 'Token de autenticación requerido'
                }), 401
            
            # Verificar token y rol de administrador
            token_result = self.auth_service.verify_token(auth_header.replace('Bearer ', ''))
            if not token_result['success']:
                return jsonify({
                    'success': False,
                    'message': 'Token inválido o expirado'
                }), 401
            
            # Verificar que el usuario sea administrador
            user_result = self.auth_service.get_user_by_id(token_result['user_id'])
            if not user_result['success'] or user_result['user']['role'] != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Solo los administradores pueden registrar usuarios'
                }), 403
            
            data = request.get_json()
            
            # Validar datos requeridos
            required_fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'message': f'El campo {field} es requerido'
                    }), 400
            
            # Validar rol válido
            valid_roles = ['admin', 'secretary', 'doctor', 'technician']
            if data['role'] not in valid_roles:
                return jsonify({
                    'success': False,
                    'message': f'Rol inválido. Roles válidos: {", ".join(valid_roles)}'
                }), 400
            
            # Validar contraseña segura
            password_validation = self.auth_service.validate_password(data['password'])
            if not password_validation['valid']:
                return jsonify({
                    'success': False,
                    'message': password_validation['message']
                }), 400
            
            result = self.auth_service.register_user(data)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Usuario registrado exitosamente',
                    'data': result['user']
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'message': result['message']
                }), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    def logout(self):
        """Cerrar sesión"""
        try:
            # En una implementación real, aquí invalidarías el token
            return jsonify({
                'success': True,
                'message': 'Sesión cerrada exitosamente'
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    def get_profile(self):
        """Obtener perfil del usuario autenticado"""
        try:
            # El usuario ya está disponible en g.current_user gracias al middleware
            from flask import g
            return jsonify({
                'success': True,
                'data': g.current_user
            }), 200
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    def update_profile(self):
        """Actualizar perfil del usuario"""
        try:
            # El user_id ya está disponible en g.user_id gracias al middleware
            from flask import g
            data = request.get_json()
            
            result = self.auth_service.update_user(g.user_id, data)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Perfil actualizado exitosamente',
                    'data': result['user']
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': result['message']
                }), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    def get_roles(self):
        """Obtener roles disponibles"""
        try:
            result = self.auth_service.get_user_roles()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500
    
    def verify_token(self):
        """Verificar token JWT"""
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({
                    'success': False,
                    'message': 'Token de autenticación requerido'
                }), 401
            
            token = auth_header.replace('Bearer ', '')
            result = self.auth_service.verify_token(token)
            
            if result['success']:
                # Obtener información del usuario
                user_result = self.auth_service.get_user_by_id(result['user_id'])
                if user_result['success']:
                    return jsonify({
                        'success': True,
                        'message': 'Token válido',
                        'data': {
                            'user': user_result['user']
                        }
                    }), 200
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Usuario no encontrado'
                    }), 401
            else:
                return jsonify({
                    'success': False,
                    'message': result['message']
                }), 401
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error en el servidor: {str(e)}'
            }), 500


def token_required(f):
    """Decorator para requerir autenticación"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token de autenticación requerido'
            }), 401
        
        # Aquí validarías el token JWT
        # Por simplicidad, asumimos que el token es válido
        
        return f(*args, **kwargs)
    
    return decorated
