"""
Middleware de Autenticación y Autorización
"""

from flask import request, jsonify, g
from functools import wraps
from app.services.auth_service import AuthService


class AuthMiddleware:
    """Middleware para manejar autenticación y autorización"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    def token_required(self, f):
        """Decorator para requerir autenticación"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            # Obtener token del header Authorization
            auth_header = request.headers.get('Authorization')
            if auth_header:
                try:
                    token = auth_header.split(" ")[1]  # Bearer <token>
                except IndexError:
                    return jsonify({
                        'success': False,
                        'message': 'Formato de token inválido'
                    }), 401
            
            if not token:
                return jsonify({
                    'success': False,
                    'message': 'Token de autenticación requerido'
                }), 401
            
            # Verificar token
            token_result = self.auth_service.verify_token(token)
            if not token_result['success']:
                return jsonify({
                    'success': False,
                    'message': token_result['message']
                }), 401
            
            # Obtener información del usuario
            user_result = self.auth_service.get_user_by_id(token_result['user_id'])
            if not user_result['success']:
                return jsonify({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }), 401
            
            # Verificar que el usuario esté activo
            if not user_result['user']['is_active']:
                return jsonify({
                    'success': False,
                    'message': 'Usuario inactivo'
                }), 401
            
            # Agregar información del usuario al contexto de Flask
            g.current_user = user_result['user']
            g.user_id = token_result['user_id']
            
            return f(*args, **kwargs)
        
        return decorated
    
    def role_required(self, *required_roles):
        """Decorator para requerir roles específicos"""
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                # Primero verificar autenticación
                auth_result = self.token_required(f)(*args, **kwargs)
                
                # Si hay error de autenticación, retornarlo
                if isinstance(auth_result, tuple) and auth_result[1] in [401, 403]:
                    return auth_result
                
                # Verificar rol
                user_role = g.current_user.get('role')
                if user_role not in required_roles:
                    return jsonify({
                        'success': False,
                        'message': f'Acceso denegado. Se requiere uno de los siguientes roles: {", ".join(required_roles)}'
                    }), 403
                
                return f(*args, **kwargs)
            
            return decorated
        return decorator
    
    def admin_required(self, f):
        """Decorator para requerir rol de administrador"""
        return self.role_required('admin')(f)
    
    def secretary_required(self, f):
        """Decorator para requerir rol de secretaria"""
        return self.role_required('secretary')(f)
    
    def doctor_required(self, f):
        """Decorator para requerir rol de médico"""
        return self.role_required('doctor')(f)
    
    def technician_required(self, f):
        """Decorator para requerir rol de técnico"""
        return self.role_required('technician')(f)
    
    def admin_or_secretary_required(self, f):
        """Decorator para requerir rol de administrador o secretaria"""
        return self.role_required('admin', 'secretary')(f)
    
    def medical_staff_required(self, f):
        """Decorator para requerir rol médico (doctor o technician)"""
        return self.role_required('doctor', 'technician')(f)


# Instancia global del middleware
auth_middleware = AuthMiddleware()

# Decorators de conveniencia
token_required = auth_middleware.token_required
role_required = auth_middleware.role_required
admin_required = auth_middleware.admin_required
secretary_required = auth_middleware.secretary_required
doctor_required = auth_middleware.doctor_required
technician_required = auth_middleware.technician_required
admin_or_secretary_required = auth_middleware.admin_or_secretary_required
medical_staff_required = auth_middleware.medical_staff_required

