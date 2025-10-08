"""
Modelo para reportes de laboratorio
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, validates
from database import db
import re
import os


class LabReport(db.Model):
    """Modelo para reportes de laboratorio"""
    
    __tablename__ = 'lab_reports'
    
    # Campos principales
    id = Column(Integer, primary_key=True)
    order_number = Column(String(50), nullable=False, unique=True, index=True)
    patient_name = Column(String(255), nullable=False, index=True)
    patient_age = Column(Integer)
    patient_gender = Column(String(1))
    doctor_name = Column(String(255))
    reception_date = Column(Date, index=True)
    
    # Campos de archivo
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    
    # Contenido y configuración
    selected_tests = Column(JSONB)
    html_content = Column(Text)
    status = Column(String(20), default='draft', index=True)
    
    # Metadatos
    created_by = Column(Integer, ForeignKey('users.id'), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    creator = relationship('User', backref='created_reports')
    tests = relationship('ReportTest', back_populates='report', cascade='all, delete-orphan')
    
    # Constraints
    __table_args__ = (
        CheckConstraint("patient_gender IN ('M', 'F')", name='check_patient_gender'),
        CheckConstraint("status IN ('draft', 'final', 'printed')", name='check_status'),
        CheckConstraint("patient_age >= 0 AND patient_age <= 150", name='check_patient_age'),
    )
    
    def __init__(self, **kwargs):
        super(LabReport, self).__init__(**kwargs)
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()
    
    @validates('order_number')
    def validate_order_number(self, key, order_number):
        """Validar número de orden"""
        if not order_number:
            raise ValueError("El número de orden es requerido")
        
        if len(order_number) < 3:
            raise ValueError("El número de orden debe tener al menos 3 caracteres")
        
        if len(order_number) > 50:
            raise ValueError("El número de orden no puede exceder 50 caracteres")
        
        # Validar formato (letras, números, guiones y guiones bajos)
        if not re.match(r'^[A-Za-z0-9_-]+$', order_number):
            raise ValueError("El número de orden solo puede contener letras, números, guiones y guiones bajos")
        
        return order_number.upper()
    
    @validates('patient_name')
    def validate_patient_name(self, key, patient_name):
        """Validar nombre del paciente"""
        if not patient_name:
            raise ValueError("El nombre del paciente es requerido")
        
        if len(patient_name.strip()) < 2:
            raise ValueError("El nombre del paciente debe tener al menos 2 caracteres")
        
        if len(patient_name) > 255:
            raise ValueError("El nombre del paciente no puede exceder 255 caracteres")
        
        return patient_name.strip().title()
    
    @validates('patient_age')
    def validate_patient_age(self, key, patient_age):
        """Validar edad del paciente"""
        if patient_age is not None:
            if not isinstance(patient_age, int):
                try:
                    patient_age = int(patient_age)
                except (ValueError, TypeError):
                    raise ValueError("La edad debe ser un número entero")
            
            if patient_age < 0 or patient_age > 150:
                raise ValueError("La edad debe estar entre 0 y 150 años")
        
        return patient_age
    
    @validates('patient_gender')
    def validate_patient_gender(self, key, patient_gender):
        """Validar género del paciente"""
        if patient_gender is not None:
            patient_gender = patient_gender.upper()
            if patient_gender not in ['M', 'F']:
                raise ValueError("El género debe ser 'M' o 'F'")
        
        return patient_gender
    
    @validates('file_path')
    def validate_file_path(self, key, file_path):
        """Validar ruta del archivo"""
        if not file_path:
            raise ValueError("La ruta del archivo es requerida")
        
        if len(file_path) > 500:
            raise ValueError("La ruta del archivo no puede exceder 500 caracteres")
        
        # Validar que no contenga caracteres peligrosos
        dangerous_chars = ['..', '~', '$', '`']
        for char in dangerous_chars:
            if char in file_path:
                raise ValueError(f"La ruta del archivo no puede contener '{char}'")
        
        return file_path
    
    @validates('file_name')
    def validate_file_name(self, key, file_name):
        """Validar nombre del archivo"""
        if not file_name:
            raise ValueError("El nombre del archivo es requerido")
        
        if len(file_name) > 255:
            raise ValueError("El nombre del archivo no puede exceder 255 caracteres")
        
        # Validar extensión
        if not file_name.lower().endswith('.html'):
            raise ValueError("El archivo debe tener extensión .html")
        
        # Validar caracteres en el nombre
        if not re.match(r'^[A-Za-z0-9._-]+\.html$', file_name):
            raise ValueError("El nombre del archivo contiene caracteres no válidos")
        
        return file_name
    
    @validates('selected_tests')
    def validate_selected_tests(self, key, selected_tests):
        """Validar pruebas seleccionadas"""
        if not selected_tests:
            raise ValueError("Debe seleccionar al menos una prueba")
        
        if not isinstance(selected_tests, (list, dict)):
            raise ValueError("Las pruebas seleccionadas deben ser una lista o diccionario")
        
        if isinstance(selected_tests, list) and len(selected_tests) == 0:
            raise ValueError("Debe seleccionar al menos una prueba")
        
        return selected_tests
    
    @validates('html_content')
    def validate_html_content(self, key, html_content):
        """Validar contenido HTML"""
        if not html_content:
            raise ValueError("El contenido HTML es requerido")
        
        if not isinstance(html_content, str):
            raise ValueError("El contenido HTML debe ser una cadena de texto")
        
        # Validar que contenga etiquetas HTML básicas
        if not re.search(r'<html|<body|<div|<table', html_content, re.IGNORECASE):
            raise ValueError("El contenido debe ser HTML válido")
        
        return html_content
    
    @validates('status')
    def validate_status(self, key, status):
        """Validar estado del reporte"""
        if status not in ['draft', 'final', 'printed']:
            raise ValueError("El estado debe ser 'draft', 'final' o 'printed'")
        
        return status
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'patient_name': self.patient_name,
            'patient_age': self.patient_age,
            'patient_gender': self.patient_gender,
            'doctor_name': self.doctor_name,
            'reception_date': self.reception_date.isoformat() if self.reception_date else None,
            'file_path': self.file_path,
            'file_name': self.file_name,
            'selected_tests': self.selected_tests,
            'html_content': self.html_content,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tests': [test.to_dict() for test in self.tests] if self.tests else []
        }
    
    def to_dict_summary(self) -> Dict[str, Any]:
        """Convertir a diccionario resumido (sin HTML content)"""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'patient_name': self.patient_name,
            'patient_age': self.patient_age,
            'patient_gender': self.patient_gender,
            'doctor_name': self.doctor_name,
            'reception_date': self.reception_date.isoformat() if self.reception_date else None,
            'file_path': self.file_path,
            'file_name': self.file_name,
            'selected_tests': self.selected_tests,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_status(self, new_status: str) -> bool:
        """Actualizar estado del reporte"""
        if new_status not in ['draft', 'final', 'printed']:
            return False
        
        self.status = new_status
        self.updated_at = datetime.utcnow()
        return True
    
    def is_editable(self) -> bool:
        """Verificar si el reporte es editable"""
        return self.status == 'draft'
    
    def can_print(self) -> bool:
        """Verificar si el reporte puede imprimirse"""
        return self.status in ['final', 'printed']
    
    def get_file_size(self) -> Optional[int]:
        """Obtener tamaño del archivo en bytes"""
        try:
            if os.path.exists(self.file_path):
                return os.path.getsize(self.file_path)
        except Exception:
            pass
        return None
    
    def file_exists(self) -> bool:
        """Verificar si el archivo existe en el sistema de archivos"""
        try:
            return os.path.exists(self.file_path)
        except Exception:
            return False
    
    @classmethod
    def get_by_order_number(cls, order_number: str) -> Optional['LabReport']:
        """Buscar reporte por número de orden"""
        return cls.query.filter_by(order_number=order_number.upper()).first()
    
    @classmethod
    def get_by_patient_name(cls, patient_name: str, limit: int = 50) -> List['LabReport']:
        """Buscar reportes por nombre de paciente"""
        return cls.query.filter(
            cls.patient_name.ilike(f'%{patient_name}%')
        ).order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def get_by_date_range(cls, start_date: date, end_date: date) -> List['LabReport']:
        """Buscar reportes por rango de fechas"""
        return cls.query.filter(
            cls.reception_date >= start_date,
            cls.reception_date <= end_date
        ).order_by(cls.reception_date.desc()).all()
    
    @classmethod
    def get_by_status(cls, status: str) -> List['LabReport']:
        """Buscar reportes por estado"""
        return cls.query.filter_by(status=status).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_stats(cls) -> Dict[str, Any]:
        """Obtener estadísticas de reportes"""
        from sqlalchemy import func
        
        stats = db.session.query(
            func.count(cls.id).label('total_reports'),
            func.count(func.distinct(cls.patient_name)).label('unique_patients'),
            func.count(func.distinct(cls.doctor_name)).label('unique_doctors'),
            func.count(cls.id).filter(cls.status == 'draft').label('draft_reports'),
            func.count(cls.id).filter(cls.status == 'final').label('final_reports'),
            func.count(cls.id).filter(cls.status == 'printed').label('printed_reports')
        ).first()
        
        return {
            'total_reports': stats.total_reports or 0,
            'unique_patients': stats.unique_patients or 0,
            'unique_doctors': stats.unique_doctors or 0,
            'draft_reports': stats.draft_reports or 0,
            'final_reports': stats.final_reports or 0,
            'printed_reports': stats.printed_reports or 0
        }
    
    def __repr__(self):
        return f'<LabReport {self.order_number} - {self.patient_name}>'


class ReportTest(db.Model):
    """Modelo para pruebas individuales de un reporte"""
    
    __tablename__ = 'report_tests'
    
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('lab_reports.id', ondelete='CASCADE'), nullable=False, index=True)
    test_name = Column(String(255), nullable=False, index=True)
    test_filename = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    report = relationship('LabReport', back_populates='tests')
    
    @validates('test_name')
    def validate_test_name(self, key, test_name):
        """Validar nombre de la prueba"""
        if not test_name:
            raise ValueError("El nombre de la prueba es requerido")
        
        if len(test_name.strip()) < 2:
            raise ValueError("El nombre de la prueba debe tener al menos 2 caracteres")
        
        return test_name.strip()
    
    @validates('test_filename')
    def validate_test_filename(self, key, test_filename):
        """Validar nombre del archivo de prueba"""
        if test_filename and not test_filename.lower().endswith('.html'):
            raise ValueError("El archivo de prueba debe tener extensión .html")
        
        return test_filename
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'report_id': self.report_id,
            'test_name': self.test_name,
            'test_filename': self.test_filename,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<ReportTest {self.test_name} - Report {self.report_id}>'

