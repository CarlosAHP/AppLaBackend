"""
Pruebas unitarias para sincronización
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.services.sync_service import SyncService
from app.models.sync import Sync


class TestSyncService(unittest.TestCase):
    """Pruebas para SyncService"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.sync_service = SyncService()
    
    def test_create_sync_log_success(self):
        """Probar creación exitosa de log de sincronización"""
        with patch('app.services.sync_service.Sync') as mock_sync_class:
            mock_sync_log = MagicMock()
            mock_sync_log.id = 1
            mock_sync_log.to_dict.return_value = {'id': 1, 'status': 'pending'}
            mock_sync_class.return_value = mock_sync_log
            
            with patch.object(self.sync_service, 'process_sync', return_value=True):
                result = self.sync_service.create_sync_log(
                    sync_type='lab_result',
                    entity_id=1,
                    entity_type='LabResult',
                    operation='create',
                    data_after={'id': 1, 'patient_name': 'Juan Pérez'}
                )
                
                self.assertTrue(result['success'])
                self.assertEqual(result['sync_log']['status'], 'pending')
    
    def test_get_sync_logs_with_filters(self):
        """Probar obtención de logs con filtros"""
        mock_pagination = MagicMock()
        mock_pagination.items = [MagicMock(), MagicMock()]
        mock_pagination.page = 1
        mock_pagination.pages = 1
        mock_pagination.per_page = 10
        mock_pagination.total = 2
        mock_pagination.has_next = False
        mock_pagination.has_prev = False
        
        with patch('app.services.sync_service.Sync.query') as mock_query:
            mock_query.filter.return_value = mock_query
            mock_query.filter_by.return_value = mock_query
            mock_query.order_by.return_value = mock_query
            mock_query.paginate.return_value = mock_pagination
            
            # Mock para to_dict
            for item in mock_pagination.items:
                item.to_dict.return_value = {'id': 1, 'status': 'success'}
            
            result = self.sync_service.get_sync_logs(
                page=1,
                per_page=10,
                filters={'sync_type': 'lab_result', 'status': 'success'}
            )
            
            self.assertTrue(result['success'])
            self.assertEqual(len(result['sync_logs']), 2)
            self.assertEqual(result['pagination']['total'], 2)
    
    def test_get_sync_log_by_id_success(self):
        """Probar obtención de log por ID exitosa"""
        mock_sync_log = MagicMock()
        mock_sync_log.to_dict.return_value = {'id': 1, 'status': 'success'}
        
        with patch('app.services.sync_service.Sync.query') as mock_query:
            mock_query.get.return_value = mock_sync_log
            
            result = self.sync_service.get_sync_log_by_id(1)
            
            self.assertTrue(result['success'])
            self.assertEqual(result['sync_log']['status'], 'success')
    
    def test_get_sync_log_by_id_not_found(self):
        """Probar obtención de log por ID no encontrado"""
        with patch('app.services.sync_service.Sync.query') as mock_query:
            mock_query.get.return_value = None
            
            result = self.sync_service.get_sync_log_by_id(999)
            
            self.assertFalse(result['success'])
            self.assertEqual(result['message'], 'Log de sincronización no encontrado')
    
    def test_retry_sync_success(self):
        """Probar reintento exitoso de sincronización"""
        mock_sync_log = MagicMock()
        mock_sync_log.status = 'failed'
        mock_sync_log.retry_count = 1
        mock_sync_log.to_dict.return_value = {'id': 1, 'status': 'pending', 'retry_count': 2}
        
        with patch('app.services.sync_service.Sync.query') as mock_query:
            mock_query.get.return_value = mock_sync_log
            
            with patch.object(self.sync_service, 'process_sync', return_value=True):
                result = self.sync_service.retry_sync(1)
                
                self.assertTrue(result['success'])
                self.assertEqual(result['sync_log']['retry_count'], 2)
    
    def test_retry_sync_already_successful(self):
        """Probar reintento de sincronización ya exitosa"""
        mock_sync_log = MagicMock()
        mock_sync_log.status = 'success'
        
        with patch('app.services.sync_service.Sync.query') as mock_query:
            mock_query.get.return_value = mock_sync_log
            
            result = self.sync_service.retry_sync(1)
            
            self.assertFalse(result['success'])
            self.assertEqual(result['message'], 'La sincronización ya fue exitosa')
    
    def test_retry_sync_max_retries_reached(self):
        """Probar reintento con máximo de reintentos alcanzado"""
        mock_sync_log = MagicMock()
        mock_sync_log.status = 'failed'
        mock_sync_log.retry_count = 3  # Máximo permitido
        
        with patch('app.services.sync_service.Sync.query') as mock_query:
            mock_query.get.return_value = mock_sync_log
            
            result = self.sync_service.retry_sync(1)
            
            self.assertFalse(result['success'])
            self.assertEqual(result['message'], 'Se ha alcanzado el número máximo de reintentos')
    
    def test_manual_sync_success(self):
        """Probar sincronización manual exitosa"""
        mock_entity = MagicMock()
        mock_entity.to_dict.return_value = {'id': 1, 'patient_name': 'Juan Pérez'}
        
        with patch.object(self.sync_service, 'get_entity_by_type_and_id', return_value=mock_entity):
            with patch('app.services.sync_service.Sync') as mock_sync_class:
                mock_sync_log = MagicMock()
                mock_sync_log.id = 1
                mock_sync_log.to_dict.return_value = {'id': 1, 'is_manual': True}
                mock_sync_class.return_value = mock_sync_log
                
                with patch.object(self.sync_service, 'process_sync', return_value=True):
                    result = self.sync_service.manual_sync('LabResult', 1, 'update')
                    
                    self.assertTrue(result['success'])
                    self.assertTrue(result['sync_log']['is_manual'])
    
    def test_manual_sync_entity_not_found(self):
        """Probar sincronización manual con entidad no encontrada"""
        with patch.object(self.sync_service, 'get_entity_by_type_and_id', return_value=None):
            result = self.sync_service.manual_sync('LabResult', 999, 'update')
            
            self.assertFalse(result['success'])
            self.assertIn('no encontrado', result['message'])
    
    def test_bulk_sync_success(self):
        """Probar sincronización masiva exitosa"""
        mock_entities = [MagicMock(), MagicMock()]
        for entity in mock_entities:
            entity.id = 1
            entity.to_dict.return_value = {'id': 1, 'patient_name': 'Test'}
        
        with patch.object(self.sync_service, 'get_entities_by_type_and_filters', return_value=mock_entities):
            with patch('app.services.sync_service.Sync') as mock_sync_class:
                mock_sync_log = MagicMock()
                mock_sync_log.id = 1
                mock_sync_log.to_dict.return_value = {'id': 1, 'status': 'pending'}
                mock_sync_class.return_value = mock_sync_log
                
                with patch.object(self.sync_service, 'process_sync', return_value=True):
                    result = self.sync_service.bulk_sync('LabResult', {'status': 'pending'}, 'update')
                    
                    self.assertTrue(result['success'])
                    self.assertEqual(result['count'], 2)
                    self.assertEqual(len(result['sync_logs']), 2)
    
    def test_bulk_sync_no_entities(self):
        """Probar sincronización masiva sin entidades"""
        with patch.object(self.sync_service, 'get_entities_by_type_and_filters', return_value=[]):
            result = self.sync_service.bulk_sync('LabResult', {}, 'update')
            
            self.assertFalse(result['success'])
            self.assertIn('No se encontraron entidades', result['message'])
    
    def test_get_sync_status(self):
        """Probar obtención de estado de sincronización"""
        with patch('app.services.sync_service.Sync.query') as mock_query:
            # Mock para count
            mock_query.count.return_value = 10
            mock_query.filter_by.return_value.count.return_value = 5
            
            # Mock para logs fallidos recientes
            mock_failed_logs = [MagicMock(), MagicMock()]
            for log in mock_failed_logs:
                log.to_dict.return_value = {'id': 1, 'status': 'failed'}
            
            mock_query.filter_by.return_value.order_by.return_value.limit.return_value.all.return_value = mock_failed_logs
            
            result = self.sync_service.get_sync_status()
            
            self.assertTrue(result['success'])
            self.assertIn('total_logs', result['status'])
            self.assertIn('pending_logs', result['status'])
            self.assertIn('success_logs', result['status'])
            self.assertIn('failed_logs', result['status'])
            self.assertIn('type_counts', result['status'])
            self.assertIn('recent_failed', result['status'])
    
    def test_process_sync_success(self):
        """Probar procesamiento exitoso de sincronización"""
        mock_sync_log = MagicMock()
        
        with patch('app.services.sync_service.Sync.query') as mock_query:
            mock_query.get.return_value = mock_sync_log
            
            with patch('random.random', return_value=0.5):  # Simular éxito
                result = self.sync_service.process_sync(1)
                
                self.assertTrue(result)
                self.assertEqual(mock_sync_log.status, 'success')
    
    def test_process_sync_failure(self):
        """Probar procesamiento fallido de sincronización"""
        mock_sync_log = MagicMock()
        
        with patch('app.services.sync_service.Sync.query') as mock_query:
            mock_query.get.return_value = mock_sync_log
            
            with patch('random.random', return_value=0.95):  # Simular fallo
                result = self.sync_service.process_sync(1)
                
                self.assertFalse(result)
                self.assertEqual(mock_sync_log.status, 'failed')


class TestSyncModel(unittest.TestCase):
    """Pruebas para el modelo Sync"""
    
    def test_sync_creation(self):
        """Probar creación de log de sincronización"""
        sync_log = Sync(
            sync_type='lab_result',
            entity_id=1,
            entity_type='LabResult',
            operation='create',
            status='pending'
        )
        
        self.assertEqual(sync_log.sync_type, 'lab_result')
        self.assertEqual(sync_log.entity_id, 1)
        self.assertEqual(sync_log.entity_type, 'LabResult')
        self.assertEqual(sync_log.operation, 'create')
        self.assertEqual(sync_log.status, 'pending')
    
    def test_sync_to_dict(self):
        """Probar conversión a diccionario"""
        sync_log = Sync(
            id=1,
            sync_type='lab_result',
            entity_id=1,
            entity_type='LabResult',
            operation='create',
            status='success',
            retry_count=0,
            is_manual=False
        )
        
        result_dict = sync_log.to_dict()
        
        self.assertEqual(result_dict['id'], 1)
        self.assertEqual(result_dict['sync_type'], 'lab_result')
        self.assertEqual(result_dict['entity_id'], 1)
        self.assertEqual(result_dict['entity_type'], 'LabResult')
        self.assertEqual(result_dict['operation'], 'create')
        self.assertEqual(result_dict['status'], 'success')
        self.assertEqual(result_dict['retry_count'], 0)
        self.assertFalse(result_dict['is_manual'])
    
    def test_sync_repr(self):
        """Probar representación string del log"""
        sync_log = Sync(
            sync_type='lab_result',
            entity_type='LabResult',
            entity_id=1
        )
        
        repr_str = repr(sync_log)
        self.assertIn('lab_result', repr_str)
        self.assertIn('LabResult', repr_str)
        self.assertIn('1', repr_str)


if __name__ == '__main__':
    unittest.main()
