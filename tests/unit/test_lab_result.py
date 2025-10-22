"""
Pruebas unitarias para resultados de laboratorio
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.services.lab_result_service import LabResultService
from app.models.lab_result import LabResult


class TestLabResultService(unittest.TestCase):
    """Pruebas para LabResultService"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.lab_result_service = LabResultService()
    
    def test_create_lab_result_success(self):
        """Probar creación exitosa de resultado de laboratorio"""
        lab_result_data = {
            'patient_id': 'P001',
            'patient_name': 'Juan Pérez',
            'patient_dni': '12345678',
            'patient_age': 30,
            'patient_gender': 'M',
            'exam_type': 'Hemograma',
            'exam_code': 'HEM001',
            'exam_date': '2024-01-15T10:00:00Z',
            'technician_id': 1
        }
        
        with patch('app.services.lab_result_service.LabResult') as mock_lab_result_class:
            mock_lab_result = MagicMock()
            mock_lab_result.id = 1
            mock_lab_result.to_dict.return_value = {'id': 1, 'patient_name': 'Juan Pérez'}
            mock_lab_result_class.return_value = mock_lab_result
            
            with patch.object(self.lab_result_service.sync_service, 'create_sync_log'):
                result = self.lab_result_service.create_lab_result(lab_result_data)
                
                self.assertTrue(result['success'])
                self.assertEqual(result['lab_result']['patient_name'], 'Juan Pérez')
    
    def test_create_lab_result_missing_required_fields(self):
        """Probar creación con campos requeridos faltantes"""
        lab_result_data = {
            'patient_name': 'Juan Pérez',
            'exam_type': 'Hemograma'
            # Faltan patient_id y exam_date
        }
        
        result = self.lab_result_service.create_lab_result(lab_result_data)
        
        self.assertFalse(result['success'])
        self.assertIn('Error al crear resultado', result['message'])
    
    def test_get_lab_results_with_filters(self):
        """Probar obtención de resultados con filtros"""
        mock_pagination = MagicMock()
        mock_pagination.items = [MagicMock(), MagicMock()]
        mock_pagination.page = 1
        mock_pagination.pages = 1
        mock_pagination.per_page = 10
        mock_pagination.total = 2
        mock_pagination.has_next = False
        mock_pagination.has_prev = False
        
        with patch('app.services.lab_result_service.LabResult.query') as mock_query:
            mock_query.filter.return_value = mock_query
            mock_query.filter_by.return_value = mock_query
            mock_query.ilike.return_value = mock_query
            mock_query.order_by.return_value = mock_query
            mock_query.paginate.return_value = mock_pagination
            
            # Mock para to_dict
            for item in mock_pagination.items:
                item.to_dict.return_value = {'id': 1, 'patient_name': 'Test'}
            
            result = self.lab_result_service.get_lab_results(
                page=1,
                per_page=10,
                filters={'patient_id': 'P001', 'status': 'pending'}
            )
            
            self.assertTrue(result['success'])
            self.assertEqual(len(result['lab_results']), 2)
            self.assertEqual(result['pagination']['total'], 2)
    
    def test_get_lab_result_by_id_success(self):
        """Probar obtención de resultado por ID exitosa"""
        mock_lab_result = MagicMock()
        mock_lab_result.to_dict.return_value = {'id': 1, 'patient_name': 'Juan Pérez'}
        
        with patch('app.services.lab_result_service.LabResult.query') as mock_query:
            mock_query.get.return_value = mock_lab_result
            
            result = self.lab_result_service.get_lab_result_by_id(1)
            
            self.assertTrue(result['success'])
            self.assertEqual(result['lab_result']['patient_name'], 'Juan Pérez')
    
    def test_get_lab_result_by_id_not_found(self):
        """Probar obtención de resultado por ID no encontrado"""
        with patch('app.services.lab_result_service.LabResult.query') as mock_query:
            mock_query.get.return_value = None
            
            result = self.lab_result_service.get_lab_result_by_id(999)
            
            self.assertFalse(result['success'])
            self.assertEqual(result['message'], 'Resultado de laboratorio no encontrado')
    
    def test_update_lab_result_success(self):
        """Probar actualización exitosa de resultado"""
        mock_lab_result = MagicMock()
        mock_lab_result.to_dict.return_value = {'id': 1, 'patient_name': 'Juan Pérez Actualizado'}
        
        with patch('app.services.lab_result_service.LabResult.query') as mock_query:
            mock_query.get.return_value = mock_lab_result
            
            with patch.object(self.lab_result_service.sync_service, 'create_sync_log'):
                update_data = {'patient_name': 'Juan Pérez Actualizado'}
                result = self.lab_result_service.update_lab_result(1, update_data)
                
                self.assertTrue(result['success'])
                self.assertEqual(result['lab_result']['patient_name'], 'Juan Pérez Actualizado')
    
    def test_update_lab_result_status_success(self):
        """Probar actualización exitosa de estado"""
        mock_lab_result = MagicMock()
        mock_lab_result.result_date = None
        mock_lab_result.to_dict.return_value = {'id': 1, 'status': 'completed'}
        
        with patch('app.services.lab_result_service.LabResult.query') as mock_query:
            mock_query.get.return_value = mock_lab_result
            
            with patch.object(self.lab_result_service.sync_service, 'create_sync_log'):
                result = self.lab_result_service.update_lab_result_status(1, 'completed')
                
                self.assertTrue(result['success'])
                self.assertEqual(result['lab_result']['status'], 'completed')
    
    def test_update_lab_result_status_invalid(self):
        """Probar actualización con estado inválido"""
        mock_lab_result = MagicMock()
        
        with patch('app.services.lab_result_service.LabResult.query') as mock_query:
            mock_query.get.return_value = mock_lab_result
            
            result = self.lab_result_service.update_lab_result_status(1, 'invalid_status')
            
            self.assertFalse(result['success'])
            self.assertIn('Estado inválido', result['message'])
    
    def test_delete_lab_result_success(self):
        """Probar eliminación exitosa de resultado"""
        mock_lab_result = MagicMock()
        mock_lab_result.to_dict.return_value = {'id': 1, 'patient_name': 'Juan Pérez'}
        
        with patch('app.services.lab_result_service.LabResult.query') as mock_query:
            mock_query.get.return_value = mock_lab_result
            
            with patch.object(self.lab_result_service.sync_service, 'create_sync_log'):
                result = self.lab_result_service.delete_lab_result(1)
                
                self.assertTrue(result['success'])
                self.assertEqual(result['message'], 'Resultado eliminado exitosamente')


class TestLabResultModel(unittest.TestCase):
    """Pruebas para el modelo LabResult"""
    
    def test_lab_result_creation(self):
        """Probar creación de resultado de laboratorio"""
        lab_result = LabResult(
            patient_id='P001',
            patient_name='Juan Pérez',
            patient_dni='12345678',
            patient_age=30,
            patient_gender='M',
            exam_type='Hemograma',
            exam_code='HEM001',
            exam_date=datetime.now(),
            status='pending'
        )
        
        self.assertEqual(lab_result.patient_id, 'P001')
        self.assertEqual(lab_result.patient_name, 'Juan Pérez')
        self.assertEqual(lab_result.exam_type, 'Hemograma')
        self.assertEqual(lab_result.status, 'pending')
    
    def test_lab_result_to_dict(self):
        """Probar conversión a diccionario"""
        exam_date = datetime.now()
        lab_result = LabResult(
            id=1,
            patient_id='P001',
            patient_name='Juan Pérez',
            exam_type='Hemograma',
            exam_date=exam_date,
            status='pending'
        )
        
        result_dict = lab_result.to_dict()
        
        self.assertEqual(result_dict['id'], 1)
        self.assertEqual(result_dict['patient_id'], 'P001')
        self.assertEqual(result_dict['patient_name'], 'Juan Pérez')
        self.assertEqual(result_dict['exam_type'], 'Hemograma')
        self.assertEqual(result_dict['status'], 'pending')
        self.assertIsNotNone(result_dict['exam_date'])
    
    def test_lab_result_repr(self):
        """Probar representación string del resultado"""
        lab_result = LabResult(
            patient_name='Juan Pérez',
            exam_type='Hemograma'
        )
        
        repr_str = repr(lab_result)
        self.assertIn('Juan Pérez', repr_str)
        self.assertIn('Hemograma', repr_str)


if __name__ == '__main__':
    unittest.main()
