"""
Servicio de Autenticación
"""

import jwt
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.config import Config
from database import db


class AuthService:
    """Servicio para manejar la lógica de autenticación"""
    
    def __init__(self):
        self.secret_key = Config.SECRET_KEY
        self.token_expiration = Config.TOKEN_EXPIRATION
        self.valid_roles = ['admin', 'secretary', 'doctor', 'technician']
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Autenticar usuario con username y password"""
        try:
            # Buscar usuario por username
            user = User.query.filter_by(username=username).first()
            
            if not user:
                return {
                    'success': False,
                    'message': 'Usuario no encontrado'
                }
            
            if not user.is_active:
                return {
                    'success': False,
                    'message': 'Usuario inactivo'
                }
            
            # Verificar contraseña
            if not user.check_password(password):
                return {
                    'success': False,
                    'message': 'Contraseña incorrecta'
                }
            
            # Generar token JWT
            token = self.generate_token(user.id)
            
            return {
                'success': True,
                'user': user.to_dict(),
                'token': token
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error en autenticación: {str(e)}'
            }
    
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Registrar nuevo usuario"""
        try:
            # Verificar si el username ya existe
            if User.query.filter_by(username=user_data['username']).first():
                return {
                    'success': False,
                    'message': 'El nombre de usuario ya existe'
                }
            
            # Verificar si el email ya existe
            if User.query.filter_by(email=user_data['email']).first():
                return {
                    'success': False,
                    'message': 'El email ya está registrado'
                }
            
            # Validar rol
            if user_data.get('role') not in self.valid_roles:
                return {
                    'success': False,
                    'message': f'Rol inválido. Roles válidos: {", ".join(self.valid_roles)}'
                }
            
            # Crear nuevo usuario
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data.get('phone'),
                role=user_data.get('role', 'secretary')  # Default a secretary en lugar de user
            )
            
            # Establecer contraseña
            user.set_password(user_data['password'])
            
            # Guardar en base de datos
            db.session.add(user)
            db.session.commit()
            
            return {
                'success': True,
                'user': user.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error en registro: {str(e)}'
            }
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Obtener usuario por ID"""
        try:
            user = User.query.get(user_id)
            
            if not user:
                return {
                    'success': False,
                    'message': 'Usuario no encontrado'
                }
            
            return {
                'success': True,
                'user': user.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener usuario: {str(e)}'
            }
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualizar datos del usuario"""
        try:
            user = User.query.get(user_id)
            
            if not user:
                return {
                    'success': False,
                    'message': 'Usuario no encontrado'
                }
            
            # Validar campos únicos si se están actualizando
            if 'username' in user_data and user_data['username'] != user.username:
                existing_user = User.query.filter_by(username=user_data['username']).first()
                if existing_user and existing_user.id != user_id:
                    return {
                        'success': False,
                        'message': 'El nombre de usuario ya existe'
                    }
            
            if 'email' in user_data and user_data['email'] != user.email:
                existing_user = User.query.filter_by(email=user_data['email']).first()
                if existing_user and existing_user.id != user_id:
                    return {
                        'success': False,
                        'message': 'El email ya está registrado'
                    }
            
            # Validar rol si se está actualizando
            if 'role' in user_data and user_data['role'] not in self.valid_roles:
                return {
                    'success': False,
                    'message': f'Rol inválido. Roles válidos: {", ".join(self.valid_roles)}'
                }
            
            # Actualizar TODOS los campos permitidos (excepto campos de sistema)
            allowed_fields = [
                'username', 'email', 'first_name', 'last_name', 'phone', 'role', 'is_active',
                'address', 'date_of_birth', 'gender', 
                'emergency_contact', 'emergency_phone',
                'medical_history', 'allergies', 'current_medications',
                'profile_image_url'
            ]
            for field in allowed_fields:
                if field in user_data:
                    setattr(user, field, user_data[field])
            
            # Actualizar timestamp
            user.updated_at = datetime.utcnow()
            
            # Guardar cambios
            db.session.commit()
            
            return {
                'success': True,
                'user': user.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al actualizar usuario: {str(e)}'
            }
    
    def generate_token(self, user_id: int) -> str:
        """Generar token JWT"""
        try:
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=self.token_expiration),
                'iat': datetime.utcnow()
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm='HS256')
            return token
            
        except Exception as e:
            raise Exception(f'Error al generar token: {str(e)}')
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verificar token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            if not user_id:
                return {
                    'success': False,
                    'message': 'Token inválido'
                }
            
            return {
                'success': True,
                'user_id': user_id
            }
            
        except jwt.ExpiredSignatureError:
            return {
                'success': False,
                'message': 'Token expirado'
            }
        except jwt.InvalidTokenError:
            return {
                'success': False,
                'message': 'Token inválido'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al verificar token: {str(e)}'
            }
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> Dict[str, Any]:
        """Cambiar contraseña del usuario"""
        try:
            user = User.query.get(user_id)
            
            if not user:
                return {
                    'success': False,
                    'message': 'Usuario no encontrado'
                }
            
            # Verificar contraseña actual
            if not user.check_password(old_password):
                return {
                    'success': False,
                    'message': 'Contraseña actual incorrecta'
                }
            
            # Establecer nueva contraseña
            user.set_password(new_password)
            user.updated_at = datetime.utcnow()
            
            # Guardar cambios
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Contraseña actualizada exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al cambiar contraseña: {str(e)}'
            }
    
    def validate_password(self, password: str) -> Dict[str, Any]:
        """Validar que la contraseña cumpla con los requisitos de seguridad"""
        try:
            if len(password) < 8:
                return {
                    'valid': False,
                    'message': 'La contraseña debe tener al menos 8 caracteres'
                }
            
            if not re.search(r'[A-Z]', password):
                return {
                    'valid': False,
                    'message': 'La contraseña debe contener al menos una letra mayúscula'
                }
            
            if not re.search(r'[a-z]', password):
                return {
                    'valid': False,
                    'message': 'La contraseña debe contener al menos una letra minúscula'
                }
            
            if not re.search(r'\d', password):
                return {
                    'valid': False,
                    'message': 'La contraseña debe contener al menos un número'
                }
            
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                return {
                    'valid': False,
                    'message': 'La contraseña debe contener al menos un carácter especial'
                }
            
            return {
                'valid': True,
                'message': 'Contraseña válida'
            }
            
        except Exception as e:
            return {
                'valid': False,
                'message': f'Error al validar contraseña: {str(e)}'
            }
    
    def get_user_roles(self) -> Dict[str, Any]:
        """Obtener lista de roles válidos"""
        return {
            'success': True,
            'roles': self.valid_roles,
            'descriptions': {
                'admin': 'Administrador - Acceso completo al sistema',
                'secretary': 'Secretaria - Ingreso de resultados de laboratorio',
                'doctor': 'Médico - Visualización de resultados',
                'technician': 'Técnico - Procesamiento de muestras'
            }
        }
