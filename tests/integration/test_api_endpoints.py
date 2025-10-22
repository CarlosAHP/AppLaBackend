"""
Pruebas de integración para endpoints de la API
"""

import unittest
import json
from unittest.mock import patch, MagicMock
from app import create_app
from app.config import TestingConfig


class TestAPIEndpoints(unittest.TestCase):
    """Pruebas de integración para endpoints"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Limpieza después de cada prueba"""
        self.app_context.pop()
    
    def test_auth_login_endpoint(self):
        """Probar endpoint de login"""
        with patch('app.controllers.auth_controller.AuthService') as mock_auth_service:
            mock_service = MagicMock()
            mock_service.authenticate_user.return_value = {
                'success': True,
                'user': {'id': 1, 'username': 'testuser'},
                'token': 'mock_token'
            }
            mock_auth_service.return_value = mock_service
            
            response = self.client.post('/api/auth/login', 
                                      json={'username': 'testuser', 'password': 'password'})
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['data']['user']['username'], 'testuser')
    
    def test_auth_register_endpoint(self):
        """Probar endpoint de registro"""
        with patch('app.controllers.auth_controller.AuthService') as mock_auth_service:
            mock_service = MagicMock()
            mock_service.register_user.return_value = {
                'success': True,
                'user': {'id': 1, 'username': 'newuser'}
            }
            mock_auth_service.return_value = mock_service
            
            user_data = {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'password123',
                'first_name': 'New',
                'last_name': 'User'
            }
            
            response = self.client.post('/api/auth/register', json=user_data)
            
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['data']['username'], 'newuser')
    
    def test_lab_result_create_endpoint(self):
        """Probar endpoint de creación de resultado de laboratorio"""
        with patch('app.controllers.lab_result_controller.LabResultService') as mock_service:
            mock_lab_service = MagicMock()
            mock_lab_service.create_lab_result.return_value = {
                'success': True,
                'lab_result': {'id': 1, 'patient_name': 'Juan Pérez'}
            }
            mock_service.return_value = mock_lab_service
            
            lab_result_data = {
                'patient_id': 'P001',
                'patient_name': 'Juan Pérez',
                'exam_type': 'Hemograma',
                'exam_date': '2024-01-15T10:00:00Z'
            }
            
            response = self.client.post('/api/lab-results', 
                                      json=lab_result_data,
                                      headers={'Authorization': 'Bearer mock_token'})
            
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['data']['patient_name'], 'Juan Pérez')
    
    def test_payment_create_endpoint(self):
        """Probar endpoint de creación de pago"""
        with patch('app.controllers.payment_controller.PaymentService') as mock_service:
            mock_payment_service = MagicMock()
            mock_payment_service.create_payment.return_value = {
                'success': True,
                'payment': {'id': 1, 'amount': 150.00}
            }
            mock_service.return_value = mock_payment_service
            
            payment_data = {
                'amount': 150.00,
                'payment_method': 'cash',
                'patient_id': 'P001',
                'patient_name': 'Juan Pérez'
            }
            
            response = self.client.post('/api/payments', 
                                      json=payment_data,
                                      headers={'Authorization': 'Bearer mock_token'})
            
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['data']['amount'], 150.00)
    
    def test_sync_logs_endpoint(self):
        """Probar endpoint de logs de sincronización"""
        with patch('app.controllers.sync_controller.SyncService') as mock_service:
            mock_sync_service = MagicMock()
            mock_sync_service.get_sync_logs.return_value = {
                'success': True,
                'sync_logs': [{'id': 1, 'status': 'success'}],
                'pagination': {'total': 1, 'page': 1}
            }
            mock_service.return_value = mock_sync_service
            
            response = self.client.get('/api/sync/logs',
                                     headers={'Authorization': 'Bearer mock_token'})
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(len(data['data']), 1)


if __name__ == '__main__':
    unittest.main()
