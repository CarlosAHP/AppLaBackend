"""
Modelo de Pagos
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import db


class Payment(db.Model):
    """Modelo de Pagos"""
    
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Información del pago
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default='PEN')  # Moneda (PEN, USD, etc.)
    payment_method = Column(String(50), nullable=False)  # cash, card, transfer, etc.
    payment_reference = Column(String(100), nullable=True)  # Referencia del pago
    
    # Información del paciente/examen
    patient_id = Column(String(50), nullable=False)
    patient_name = Column(String(100), nullable=False)
    lab_result_id = Column(Integer, ForeignKey('lab_results.id'), nullable=True)
    
    # Estado del pago
    status = Column(String(20), default='pending')  # pending, completed, failed, refunded
    
    # Información adicional
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Fechas
    payment_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    lab_result = relationship("LabResult")
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'payment_reference': self.payment_reference,
            'patient_id': self.patient_id,
            'patient_name': self.patient_name,
            'lab_result_id': self.lab_result_id,
            'status': self.status,
            'description': self.description,
            'notes': self.notes,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Payment {self.patient_name} - {self.amount} {self.currency}>'
