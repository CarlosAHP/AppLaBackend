"""
Pruebas unitarias para pagos
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.services.payment_service import PaymentService
from app.models.payment import Payment


class TestPaymentService(unittest.TestCase):
    """Pruebas para PaymentService"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.payment_service = PaymentService()
    
    def test_create_payment_success(self):
        """Probar creación exitosa de pago"""
        payment_data = {
            'amount': 150.00,
            'currency': 'PEN',
            'payment_method': 'cash',
            'patient_id': 'P001',
            'patient_name': 'Juan Pérez',
            'description': 'Pago por hemograma'
        }
        
        with patch('app.services.payment_service.Payment') as mock_payment_class:
            mock_payment = MagicMock()
            mock_payment.id = 1
            mock_payment.to_dict.return_value = {'id': 1, 'amount': 150.00}
            mock_payment_class.return_value = mock_payment
            
            with patch.object(self.payment_service.sync_service, 'create_sync_log'):
                result = self.payment_service.create_payment(payment_data)
                
                self.assertTrue(result['success'])
                self.assertEqual(result['payment']['amount'], 150.00)
    
    def test_create_payment_missing_required_fields(self):
        """Probar creación con campos requeridos faltantes"""
        payment_data = {
            'amount': 150.00,
            'patient_name': 'Juan Pérez'
            # Faltan payment_method y patient_id
        }
        
        result = self.payment_service.create_payment(payment_data)
        
        self.assertFalse(result['success'])
        self.assertIn('Error al crear pago', result['message'])
    
    def test_get_payments_with_filters(self):
        """Probar obtención de pagos con filtros"""
        mock_pagination = MagicMock()
        mock_pagination.items = [MagicMock(), MagicMock()]
        mock_pagination.page = 1
        mock_pagination.pages = 1
        mock_pagination.per_page = 10
        mock_pagination.total = 2
        mock_pagination.has_next = False
        mock_pagination.has_prev = False
        
        with patch('app.services.payment_service.Payment.query') as mock_query:
            mock_query.filter.return_value = mock_query
            mock_query.filter_by.return_value = mock_query
            mock_query.order_by.return_value = mock_query
            mock_query.paginate.return_value = mock_pagination
            
            # Mock para to_dict
            for item in mock_pagination.items:
                item.to_dict.return_value = {'id': 1, 'amount': 150.00}
            
            result = self.payment_service.get_payments(
                page=1,
                per_page=10,
                filters={'patient_id': 'P001', 'status': 'completed'}
            )
            
            self.assertTrue(result['success'])
            self.assertEqual(len(result['payments']), 2)
            self.assertEqual(result['pagination']['total'], 2)
    
    def test_get_payment_by_id_success(self):
        """Probar obtención de pago por ID exitosa"""
        mock_payment = MagicMock()
        mock_payment.to_dict.return_value = {'id': 1, 'amount': 150.00}
        
        with patch('app.services.payment_service.Payment.query') as mock_query:
            mock_query.get.return_value = mock_payment
            
            result = self.payment_service.get_payment_by_id(1)
            
            self.assertTrue(result['success'])
            self.assertEqual(result['payment']['amount'], 150.00)
    
    def test_get_payment_by_id_not_found(self):
        """Probar obtención de pago por ID no encontrado"""
        with patch('app.services.payment_service.Payment.query') as mock_query:
            mock_query.get.return_value = None
            
            result = self.payment_service.get_payment_by_id(999)
            
            self.assertFalse(result['success'])
            self.assertEqual(result['message'], 'Pago no encontrado')
    
    def test_update_payment_success(self):
        """Probar actualización exitosa de pago"""
        mock_payment = MagicMock()
        mock_payment.to_dict.return_value = {'id': 1, 'amount': 200.00}
        
        with patch('app.services.payment_service.Payment.query') as mock_query:
            mock_query.get.return_value = mock_payment
            
            with patch.object(self.payment_service.sync_service, 'create_sync_log'):
                update_data = {'amount': 200.00}
                result = self.payment_service.update_payment(1, update_data)
                
                self.assertTrue(result['success'])
                self.assertEqual(result['payment']['amount'], 200.00)
    
    def test_update_payment_status_success(self):
        """Probar actualización exitosa de estado"""
        mock_payment = MagicMock()
        mock_payment.payment_date = None
        mock_payment.to_dict.return_value = {'id': 1, 'status': 'completed'}
        
        with patch('app.services.payment_service.Payment.query') as mock_query:
            mock_query.get.return_value = mock_payment
            
            with patch.object(self.payment_service.sync_service, 'create_sync_log'):
                result = self.payment_service.update_payment_status(1, 'completed')
                
                self.assertTrue(result['success'])
                self.assertEqual(result['payment']['status'], 'completed')
    
    def test_update_payment_status_invalid(self):
        """Probar actualización con estado inválido"""
        mock_payment = MagicMock()
        
        with patch('app.services.payment_service.Payment.query') as mock_query:
            mock_query.get.return_value = mock_payment
            
            result = self.payment_service.update_payment_status(1, 'invalid_status')
            
            self.assertFalse(result['success'])
            self.assertIn('Estado inválido', result['message'])
    
    def test_get_payment_summary(self):
        """Probar obtención de resumen de pagos"""
        mock_payments = [
            MagicMock(amount=100.00, status='completed', payment_method='cash'),
            MagicMock(amount=150.00, status='completed', payment_method='card'),
            MagicMock(amount=75.00, status='pending', payment_method='cash')
        ]
        
        with patch('app.services.payment_service.Payment.query') as mock_query:
            mock_query.filter.return_value = mock_query
            mock_query.filter_by.return_value = mock_query
            mock_query.all.return_value = mock_payments
            
            result = self.payment_service.get_payment_summary()
            
            self.assertTrue(result['success'])
            self.assertEqual(result['summary']['total_amount'], 325.00)
            self.assertEqual(result['summary']['total_count'], 3)
            self.assertIn('status_summary', result['summary'])
            self.assertIn('method_summary', result['summary'])
    
    def test_delete_payment_success(self):
        """Probar eliminación exitosa de pago"""
        mock_payment = MagicMock()
        mock_payment.to_dict.return_value = {'id': 1, 'amount': 150.00}
        
        with patch('app.services.payment_service.Payment.query') as mock_query:
            mock_query.get.return_value = mock_payment
            
            with patch.object(self.payment_service.sync_service, 'create_sync_log'):
                result = self.payment_service.delete_payment(1)
                
                self.assertTrue(result['success'])
                self.assertEqual(result['message'], 'Pago eliminado exitosamente')


class TestPaymentModel(unittest.TestCase):
    """Pruebas para el modelo Payment"""
    
    def test_payment_creation(self):
        """Probar creación de pago"""
        payment = Payment(
            amount=150.00,
            currency='PEN',
            payment_method='cash',
            patient_id='P001',
            patient_name='Juan Pérez',
            status='pending'
        )
        
        self.assertEqual(payment.amount, 150.00)
        self.assertEqual(payment.currency, 'PEN')
        self.assertEqual(payment.payment_method, 'cash')
        self.assertEqual(payment.patient_id, 'P001')
        self.assertEqual(payment.patient_name, 'Juan Pérez')
        self.assertEqual(payment.status, 'pending')
    
    def test_payment_to_dict(self):
        """Probar conversión a diccionario"""
        payment_date = datetime.now()
        payment = Payment(
            id=1,
            amount=150.00,
            currency='PEN',
            payment_method='cash',
            patient_id='P001',
            patient_name='Juan Pérez',
            status='completed',
            payment_date=payment_date
        )
        
        result_dict = payment.to_dict()
        
        self.assertEqual(result_dict['id'], 1)
        self.assertEqual(result_dict['amount'], 150.00)
        self.assertEqual(result_dict['currency'], 'PEN')
        self.assertEqual(result_dict['payment_method'], 'cash')
        self.assertEqual(result_dict['patient_id'], 'P001')
        self.assertEqual(result_dict['patient_name'], 'Juan Pérez')
        self.assertEqual(result_dict['status'], 'completed')
        self.assertIsNotNone(result_dict['payment_date'])
    
    def test_payment_repr(self):
        """Probar representación string del pago"""
        payment = Payment(
            patient_name='Juan Pérez',
            amount=150.00,
            currency='PEN'
        )
        
        repr_str = repr(payment)
        self.assertIn('Juan Pérez', repr_str)
        self.assertIn('150.0', repr_str)
        self.assertIn('PEN', repr_str)


if __name__ == '__main__':
    unittest.main()
