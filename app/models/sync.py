"""
Modelo de Sincronización
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean
from database import db


class Sync(db.Model):
    """Modelo de Sincronización para tracking de datos"""
    
    __tablename__ = 'sync_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Información de la sincronización
    sync_type = Column(String(50), nullable=False)  # lab_result, payment, user, etc.
    entity_id = Column(Integer, nullable=False)  # ID de la entidad sincronizada
    entity_type = Column(String(50), nullable=False)  # Tipo de entidad
    
    # Estado de la sincronización
    status = Column(String(20), default='pending')  # pending, success, failed, retry
    
    # Información del proceso
    operation = Column(String(20), nullable=False)  # create, update, delete
    source = Column(String(50), nullable=True)  # Origen de los datos
    destination = Column(String(50), nullable=True)  # Destino de los datos
    
    # Datos sincronizados
    data_before = Column(JSON, nullable=True)  # Datos antes de la sincronización
    data_after = Column(JSON, nullable=True)   # Datos después de la sincronización
    
    # Información de error
    error_message = Column(Text, nullable=True)
    error_code = Column(String(50), nullable=True)
    
    # Metadatos
    retry_count = Column(Integer, default=0)
    last_retry = Column(DateTime, nullable=True)
    is_manual = Column(Boolean, default=False)  # Si fue sincronización manual
    
    # Fechas
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    synced_at = Column(DateTime, nullable=True)
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'sync_type': self.sync_type,
            'entity_id': self.entity_id,
            'entity_type': self.entity_type,
            'status': self.status,
            'operation': self.operation,
            'source': self.source,
            'destination': self.destination,
            'data_before': self.data_before,
            'data_after': self.data_after,
            'error_message': self.error_message,
            'error_code': self.error_code,
            'retry_count': self.retry_count,
            'last_retry': self.last_retry.isoformat() if self.last_retry else None,
            'is_manual': self.is_manual,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'synced_at': self.synced_at.isoformat() if self.synced_at else None
        }
    
    def __repr__(self):
        return f'<Sync {self.sync_type} - {self.entity_type}:{self.entity_id}>'
