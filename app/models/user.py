"""
Modelo de Usuario para el sistema de laboratorio
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Date
from werkzeug.security import generate_password_hash, check_password_hash
from database import db


class User(db.Model):
    """Modelo de Usuario"""
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(String(20), default='secretary')  # admin, secretary, doctor, technician
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Nuevos campos del perfil
    address = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(20), nullable=True)  # masculino, femenino, otro
    emergency_contact = Column(String(255), nullable=True)
    emergency_phone = Column(String(20), nullable=True)
    medical_history = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    current_medications = Column(Text, nullable=True)
    profile_image_url = Column(String(500), nullable=True)
    
    def set_password(self, password: str) -> None:
        """Establecer contraseña hasheada"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self) -> dict:
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Nuevos campos del perfil
            'address': self.address,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'emergency_contact': self.emergency_contact,
            'emergency_phone': self.emergency_phone,
            'medical_history': self.medical_history,
            'allergies': self.allergies,
            'current_medications': self.current_medications,
            'profile_image_url': self.profile_image_url
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
