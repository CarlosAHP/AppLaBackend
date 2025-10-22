"""
Pruebas unitarias para autenticación
"""

import unittest
from unittest.mock import patch, MagicMock
from app.services.auth_service import AuthService
from app.models.user import User


class TestAuthService(unittest.TestCase):
    """Pruebas para AuthService"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.auth_service = AuthService()
    
    def test_authenticate_user_success(self):
        """Probar autenticación exitosa"""
        # Mock del usuario
        mock_user = MagicMock()
        mock_user.username = 'testuser'
        mock_user.is_active = True
        mock_user.check_password.return_value = True
        mock_user.to_dict.return_value = {'id': 1, 'username': 'testuser'}
        
        with patch('app.services.auth_service.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = mock_user
            
            with patch.object(self.auth_service, 'generate_token', return_value='mock_token'):
                result = self.auth_service.authenticate_user('testuser', 'password')
                
                self.assertTrue(result['success'])
                self.assertEqual(result['user']['username'], 'testuser')
                self.assertEqual(result['token'], 'mock_token')
    
    def test_authenticate_user_not_found(self):
        """Probar autenticación con usuario no encontrado"""
        with patch('app.services.auth_service.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = None
            
            result = self.auth_service.authenticate_user('nonexistent', 'password')
            
            self.assertFalse(result['success'])
            self.assertEqual(result['message'], 'Usuario no encontrado')
    
    def test_authenticate_user_inactive(self):
        """Probar autenticación con usuario inactivo"""
        mock_user = MagicMock()
        mock_user.is_active = False
        
        with patch('app.services.auth_service.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = mock_user
            
            result = self.auth_service.authenticate_user('testuser', 'password')
            
            self.assertFalse(result['success'])
            self.assertEqual(result['message'], 'Usuario inactivo')
    
    def test_authenticate_user_wrong_password(self):
        """Probar autenticación con contraseña incorrecta"""
        mock_user = MagicMock()
        mock_user.is_active = True
        mock_user.check_password.return_value = False
        
        with patch('app.services.auth_service.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = mock_user
            
            result = self.auth_service.authenticate_user('testuser', 'wrongpassword')
            
            self.assertFalse(result['success'])
            self.assertEqual(result['message'], 'Contraseña incorrecta')
    
    def test_register_user_success(self):
        """Probar registro exitoso de usuario"""
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        with patch('app.services.auth_service.User.query') as mock_query:
            # Mock para verificar que no existe el usuario
            mock_query.filter_by.return_value.first.return_value = None
            
            with patch('app.services.auth_service.User') as mock_user_class:
                mock_user = MagicMock()
                mock_user.to_dict.return_value = {'id': 1, 'username': 'newuser'}
                mock_user_class.return_value = mock_user
                
                result = self.auth_service.register_user(user_data)
                
                self.assertTrue(result['success'])
                self.assertEqual(result['user']['username'], 'newuser')
    
    def test_register_user_username_exists(self):
        """Probar registro con username existente"""
        user_data = {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        mock_existing_user = MagicMock()
        
        with patch('app.services.auth_service.User.query') as mock_query:
            # Mock para verificar que el username ya existe
            mock_query.filter_by.return_value.first.return_value = mock_existing_user
            
            result = self.auth_service.register_user(user_data)
            
            self.assertFalse(result['success'])
            self.assertEqual(result['message'], 'El nombre de usuario ya existe')
    
    def test_generate_token(self):
        """Probar generación de token"""
        with patch('jwt.encode') as mock_encode:
            mock_encode.return_value = 'mock_token'
            
            token = self.auth_service.generate_token(1)
            
            self.assertEqual(token, 'mock_token')
            mock_encode.assert_called_once()
    
    def test_verify_token_success(self):
        """Probar verificación exitosa de token"""
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {'user_id': 1}
            
            result = self.auth_service.verify_token('valid_token')
            
            self.assertTrue(result['success'])
            self.assertEqual(result['user_id'], 1)
    
    def test_verify_token_expired(self):
        """Probar verificación de token expirado"""
        with patch('jwt.decode') as mock_decode:
            from jwt import ExpiredSignatureError
            mock_decode.side_effect = ExpiredSignatureError('Token expired')
            
            result = self.auth_service.verify_token('expired_token')
            
            self.assertFalse(result['success'])
            self.assertEqual(result['message'], 'Token expirado')


class TestUserModel(unittest.TestCase):
    """Pruebas para el modelo User"""
    
    def test_set_password(self):
        """Probar establecimiento de contraseña"""
        user = User()
        user.set_password('testpassword')
        
        self.assertIsNotNone(user.password_hash)
        self.assertNotEqual(user.password_hash, 'testpassword')
    
    def test_check_password(self):
        """Probar verificación de contraseña"""
        user = User()
        user.set_password('testpassword')
        
        self.assertTrue(user.check_password('testpassword'))
        self.assertFalse(user.check_password('wrongpassword'))
    
    def test_to_dict(self):
        """Probar conversión a diccionario"""
        user = User(
            id=1,
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role='user',
            is_active=True
        )
        
        user_dict = user.to_dict()
        
        self.assertEqual(user_dict['id'], 1)
        self.assertEqual(user_dict['username'], 'testuser')
        self.assertEqual(user_dict['email'], 'test@example.com')
        self.assertEqual(user_dict['first_name'], 'Test')
        self.assertEqual(user_dict['last_name'], 'User')
        self.assertEqual(user_dict['role'], 'user')
        self.assertTrue(user_dict['is_active'])


if __name__ == '__main__':
    unittest.main()
