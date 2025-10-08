"""
Modelo de Paciente para el sistema de laboratorio
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Date, Numeric
from database import db


class Patient(db.Model):
    """Modelo de Paciente"""
    
    __tablename__ = 'patients'
    
    # Campos básicos de identificación
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_code = Column(String(20), unique=True, nullable=False)  # Código único del paciente
    dpi = Column(String(20), unique=True, nullable=True)  # Documento Personal de Identificación
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)  # Segundo nombre
    email = Column(String(120), nullable=True)
    phone = Column(String(20), nullable=True)
    phone_secondary = Column(String(20), nullable=True)  # Teléfono secundario
    
    # Información personal
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)  # masculino, femenino, otro
    marital_status = Column(String(20), nullable=True)  # soltero, casado, divorciado, viudo
    occupation = Column(String(100), nullable=True)
    nationality = Column(String(50), default='Guatemalteco')
    
    # Información de contacto
    address = Column(Text, nullable=True)
    city = Column(String(50), nullable=True)
    department = Column(String(50), nullable=True)  # Departamento/Estado
    postal_code = Column(String(10), nullable=True)
    
    # Información médica
    blood_type = Column(String(5), nullable=True)  # A+, A-, B+, B-, AB+, AB-, O+, O-
    allergies = Column(Text, nullable=True)
    medical_history = Column(Text, nullable=True)
    current_medications = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    
    # Contacto de emergencia
    emergency_contact_name = Column(String(100), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    emergency_contact_relationship = Column(String(50), nullable=True)  # padre, madre, esposo, etc.
    
    # Información del seguro
    insurance_company = Column(String(100), nullable=True)
    insurance_policy_number = Column(String(50), nullable=True)
    insurance_phone = Column(String(20), nullable=True)
    
    # Información adicional
    notes = Column(Text, nullable=True)
    profile_image_url = Column(String(500), nullable=True)
    
    # Campos de control
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True)  # ID del usuario que creó el paciente
    
    def get_full_name(self) -> str:
        """Obtener el nombre completo del paciente"""
        full_name = f"{self.first_name} {self.last_name}"
        if self.middle_name:
            full_name = f"{self.first_name} {self.middle_name} {self.last_name}"
        return full_name
    
    def get_age(self) -> Optional[int]:
        """Calcular la edad del paciente"""
        if not self.date_of_birth:
            return None
        
        today = datetime.now().date()
        age = today.year - self.date_of_birth.year
        
        # Ajustar si el cumpleaños aún no ha pasado este año
        if today.month < self.date_of_birth.month or \
           (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
            
        return age
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'patient_code': self.patient_code,
            'dpi': self.dpi,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'full_name': self.get_full_name(),
            'email': self.email,
            'phone': self.phone,
            'phone_secondary': self.phone_secondary,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.get_age(),
            'gender': self.gender,
            'marital_status': self.marital_status,
            'occupation': self.occupation,
            'nationality': self.nationality,
            'address': self.address,
            'city': self.city,
            'department': self.department,
            'postal_code': self.postal_code,
            'blood_type': self.blood_type,
            'allergies': self.allergies,
            'medical_history': self.medical_history,
            'current_medications': self.current_medications,
            'chronic_conditions': self.chronic_conditions,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'emergency_contact_relationship': self.emergency_contact_relationship,
            'insurance_company': self.insurance_company,
            'insurance_policy_number': self.insurance_policy_number,
            'insurance_phone': self.insurance_phone,
            'notes': self.notes,
            'profile_image_url': self.profile_image_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }
    
    def to_dict_basic(self) -> dict:
        """Convertir a diccionario básico (solo información esencial)"""
        return {
            'id': self.id,
            'patient_code': self.patient_code,
            'dpi': self.dpi,
            'full_name': self.get_full_name(),
            'phone': self.phone,
            'email': self.email,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.get_age(),
            'gender': self.gender,
            'is_active': self.is_active
        }
    
    @staticmethod
    def generate_patient_code() -> str:
        """Generar un código único para el paciente"""
        from datetime import datetime
        import random
        
        # Formato: P + año + mes + día + 3 dígitos aleatorios
        now = datetime.now()
        random_suffix = random.randint(100, 999)
        return f"P{now.year}{now.month:02d}{now.day:02d}{random_suffix}"
    
    def __repr__(self):
        return f'<Patient {self.patient_code}: {self.get_full_name()}>'
