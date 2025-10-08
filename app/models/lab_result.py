"""
Modelo de Resultados de Laboratorio
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import db


class LabResult(db.Model):
    """Modelo de Resultados de Laboratorio"""
    
    __tablename__ = 'lab_results'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(50), nullable=False)  # ID del paciente
    patient_name = Column(String(100), nullable=False)
    patient_dni = Column(String(20), nullable=True)
    patient_age = Column(Integer, nullable=True)
    patient_gender = Column(String(10), nullable=True)
    
    # Información del examen
    exam_type = Column(String(100), nullable=False)  # Tipo de examen
    exam_code = Column(String(50), nullable=True)    # Código del examen
    exam_date = Column(DateTime, nullable=False)
    result_date = Column(DateTime, nullable=True)
    
    # Resultados
    results = Column(JSON, nullable=True)  # Resultados en formato JSON
    normal_values = Column(JSON, nullable=True)  # Valores normales
    observations = Column(Text, nullable=True)
    
    # Estado del resultado
    status = Column(String(20), default='pending')  # pending, completed, reviewed, delivered
    
    # Información del laboratorio
    technician_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    doctor_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    # Metadatos
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    technician = relationship("User", foreign_keys=[technician_id])
    doctor = relationship("User", foreign_keys=[doctor_id])
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient_name,
            'patient_dni': self.patient_dni,
            'patient_age': self.patient_age,
            'patient_gender': self.patient_gender,
            'exam_type': self.exam_type,
            'exam_code': self.exam_code,
            'exam_date': self.exam_date.isoformat() if self.exam_date else None,
            'result_date': self.result_date.isoformat() if self.result_date else None,
            'results': self.results,
            'normal_values': self.normal_values,
            'observations': self.observations,
            'status': self.status,
            'technician_id': self.technician_id,
            'doctor_id': self.doctor_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<LabResult {self.patient_name} - {self.exam_type}>'
