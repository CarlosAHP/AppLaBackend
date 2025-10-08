"""
Servicio para manejar operaciones de pacientes
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_
from database import db
from app.models.patient import Patient


class PatientService:
    """Servicio para operaciones de pacientes"""
    
    @staticmethod
    def create_patient(patient_data: Dict[str, Any], created_by: Optional[int] = None) -> Dict[str, Any]:
        """
        Crear un nuevo paciente
        
        Args:
            patient_data: Datos del paciente
            created_by: ID del usuario que crea el paciente
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            # Generar código único del paciente si no se proporciona
            if not patient_data.get('patient_code'):
                patient_data['patient_code'] = Patient.generate_patient_code()
            
            # Crear el paciente
            patient = Patient(
                patient_code=patient_data['patient_code'],
                dpi=patient_data.get('dpi'),
                first_name=patient_data['first_name'],
                last_name=patient_data['last_name'],
                middle_name=patient_data.get('middle_name'),
                email=patient_data.get('email'),
                phone=patient_data.get('phone'),
                phone_secondary=patient_data.get('phone_secondary'),
                date_of_birth=patient_data.get('date_of_birth'),
                gender=patient_data.get('gender'),
                marital_status=patient_data.get('marital_status'),
                occupation=patient_data.get('occupation'),
                nationality=patient_data.get('nationality', 'Guatemalteco'),
                address=patient_data.get('address'),
                city=patient_data.get('city'),
                department=patient_data.get('department'),
                postal_code=patient_data.get('postal_code'),
                blood_type=patient_data.get('blood_type'),
                allergies=patient_data.get('allergies'),
                medical_history=patient_data.get('medical_history'),
                current_medications=patient_data.get('current_medications'),
                chronic_conditions=patient_data.get('chronic_conditions'),
                emergency_contact_name=patient_data.get('emergency_contact_name'),
                emergency_contact_phone=patient_data.get('emergency_contact_phone'),
                emergency_contact_relationship=patient_data.get('emergency_contact_relationship'),
                insurance_company=patient_data.get('insurance_company'),
                insurance_policy_number=patient_data.get('insurance_policy_number'),
                insurance_phone=patient_data.get('insurance_phone'),
                notes=patient_data.get('notes'),
                profile_image_url=patient_data.get('profile_image_url'),
                created_by=created_by
            )
            
            db.session.add(patient)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Paciente creado exitosamente',
                'data': patient.to_dict()
            }
            
        except IntegrityError as e:
            db.session.rollback()
            error_msg = str(e.orig)
            if 'patient_code' in error_msg:
                return {
                    'success': False,
                    'message': 'El código de paciente ya existe',
                    'error': 'DUPLICATE_PATIENT_CODE'
                }
            elif 'dpi' in error_msg:
                return {
                    'success': False,
                    'message': 'El DPI ya está registrado',
                    'error': 'DUPLICATE_DPI'
                }
            else:
                return {
                    'success': False,
                    'message': 'Error de integridad en los datos',
                    'error': 'INTEGRITY_ERROR'
                }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error al crear paciente: {str(e)}',
                'error': 'CREATE_ERROR'
            }
    
    @staticmethod
    def get_patient_by_id(patient_id: int) -> Dict[str, Any]:
        """
        Obtener paciente por ID
        
        Args:
            patient_id: ID del paciente
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            patient = Patient.query.filter_by(id=patient_id, is_active=True).first()
            
            if not patient:
                return {
                    'success': False,
                    'message': 'Paciente no encontrado',
                    'error': 'PATIENT_NOT_FOUND'
                }
            
            return {
                'success': True,
                'data': patient.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener paciente: {str(e)}',
                'error': 'GET_ERROR'
            }
    
    @staticmethod
    def get_patient_by_code(patient_code: str) -> Dict[str, Any]:
        """
        Obtener paciente por código
        
        Args:
            patient_code: Código del paciente
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            patient = Patient.query.filter_by(patient_code=patient_code, is_active=True).first()
            
            if not patient:
                return {
                    'success': False,
                    'message': 'Paciente no encontrado',
                    'error': 'PATIENT_NOT_FOUND'
                }
            
            return {
                'success': True,
                'data': patient.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener paciente: {str(e)}',
                'error': 'GET_ERROR'
            }
    
    @staticmethod
    def get_patient_by_dpi(dpi: str) -> Dict[str, Any]:
        """
        Obtener paciente por DPI
        
        Args:
            dpi: DPI del paciente
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            patient = Patient.query.filter_by(dpi=dpi, is_active=True).first()
            
            if not patient:
                return {
                    'success': False,
                    'message': 'Paciente no encontrado',
                    'error': 'PATIENT_NOT_FOUND'
                }
            
            return {
                'success': True,
                'data': patient.to_dict()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener paciente: {str(e)}',
                'error': 'GET_ERROR'
            }
    
    @staticmethod
    def search_patients(search_term: str, limit: int = 50) -> Dict[str, Any]:
        """
        Buscar pacientes por nombre, apellido, nombre completo, código o DPI
        
        Args:
            search_term: Término de búsqueda
            limit: Límite de resultados
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            # Limpiar el término de búsqueda
            search_term = search_term.strip()
            
            if not search_term:
                return {
                    'success': False,
                    'message': 'El término de búsqueda no puede estar vacío',
                    'error': 'EMPTY_SEARCH_TERM'
                }
            
            # Dividir el término de búsqueda en palabras individuales
            search_words = search_term.split()
            
            # Crear condiciones de búsqueda
            search_conditions = []
            
            # Búsqueda por código de paciente y DPI (búsqueda exacta)
            search_conditions.extend([
                Patient.patient_code.ilike(f'%{search_term}%'),
                Patient.dpi.ilike(f'%{search_term}%')
            ])
            
            # Búsqueda por nombre completo (término completo)
            search_conditions.append(
                db.func.concat(
                    Patient.first_name, ' ', 
                    db.func.coalesce(Patient.middle_name, ''), ' ',
                    Patient.last_name
                ).ilike(f'%{search_term}%')
            )
            
            # Búsqueda por cada palabra individual en nombre, segundo nombre y apellido
            for word in search_words:
                if len(word) >= 2:  # Solo palabras de 2 o más caracteres
                    search_conditions.extend([
                        Patient.first_name.ilike(f'%{word}%'),
                        Patient.last_name.ilike(f'%{word}%'),
                        Patient.middle_name.ilike(f'%{word}%')
                    ])
            
            # Ejecutar la búsqueda
            patients = Patient.query.filter(
                and_(
                    Patient.is_active == True,
                    or_(*search_conditions)
                )
            ).order_by(
                # Ordenar por relevancia: primero coincidencias exactas, luego parciales
                db.case(
                    (Patient.first_name.ilike(f'{search_term}%'), 1),
                    (Patient.last_name.ilike(f'{search_term}%'), 1),
                    (Patient.patient_code.ilike(f'{search_term}%'), 1),
                    (Patient.dpi.ilike(f'{search_term}%'), 1),
                    else_=2
                ),
                Patient.first_name,
                Patient.last_name
            ).limit(limit).all()
            
            return {
                'success': True,
                'data': [patient.to_dict_basic() for patient in patients],
                'total': len(patients),
                'search_term': search_term,
                'search_words': search_words
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al buscar pacientes: {str(e)}',
                'error': 'SEARCH_ERROR'
            }
    
    @staticmethod
    def get_all_patients(page: int = 1, per_page: int = 20, active_only: bool = True) -> Dict[str, Any]:
        """
        Obtener todos los pacientes con paginación
        
        Args:
            page: Número de página
            per_page: Elementos por página
            active_only: Solo pacientes activos
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            query = Patient.query
            
            if active_only:
                query = query.filter_by(is_active=True)
            
            # Ordenar por fecha de creación descendente
            query = query.order_by(Patient.created_at.desc())
            
            # Paginación
            pagination = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            patients = [patient.to_dict_basic() for patient in pagination.items]
            
            return {
                'success': True,
                'data': patients,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener pacientes: {str(e)}',
                'error': 'GET_ALL_ERROR'
            }
    
    @staticmethod
    def update_patient(patient_id: int, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar un paciente
        
        Args:
            patient_id: ID del paciente
            patient_data: Datos a actualizar
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            patient = Patient.query.filter_by(id=patient_id, is_active=True).first()
            
            if not patient:
                return {
                    'success': False,
                    'message': 'Paciente no encontrado',
                    'error': 'PATIENT_NOT_FOUND'
                }
            
            # Actualizar campos permitidos
            allowed_fields = [
                'dpi', 'first_name', 'last_name', 'middle_name', 'email',
                'phone', 'phone_secondary', 'date_of_birth', 'gender',
                'marital_status', 'occupation', 'nationality', 'address',
                'city', 'department', 'postal_code', 'blood_type',
                'allergies', 'medical_history', 'current_medications',
                'chronic_conditions', 'emergency_contact_name',
                'emergency_contact_phone', 'emergency_contact_relationship',
                'insurance_company', 'insurance_policy_number',
                'insurance_phone', 'notes', 'profile_image_url'
            ]
            
            for field in allowed_fields:
                if field in patient_data:
                    setattr(patient, field, patient_data[field])
            
            patient.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Paciente actualizado exitosamente',
                'data': patient.to_dict()
            }
            
        except IntegrityError as e:
            db.session.rollback()
            error_msg = str(e.orig)
            if 'dpi' in error_msg:
                return {
                    'success': False,
                    'message': 'El DPI ya está registrado por otro paciente',
                    'error': 'DUPLICATE_DPI'
                }
            else:
                return {
                    'success': False,
                    'message': 'Error de integridad en los datos',
                    'error': 'INTEGRITY_ERROR'
                }
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error al actualizar paciente: {str(e)}',
                'error': 'UPDATE_ERROR'
            }
    
    @staticmethod
    def deactivate_patient(patient_id: int) -> Dict[str, Any]:
        """
        Desactivar un paciente (soft delete)
        
        Args:
            patient_id: ID del paciente
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            patient = Patient.query.filter_by(id=patient_id, is_active=True).first()
            
            if not patient:
                return {
                    'success': False,
                    'message': 'Paciente no encontrado',
                    'error': 'PATIENT_NOT_FOUND'
                }
            
            patient.is_active = False
            patient.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Paciente desactivado exitosamente'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error al desactivar paciente: {str(e)}',
                'error': 'DEACTIVATE_ERROR'
            }
    
    @staticmethod
    def activate_patient(patient_id: int) -> Dict[str, Any]:
        """
        Reactivar un paciente
        
        Args:
            patient_id: ID del paciente
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            patient = Patient.query.filter_by(id=patient_id, is_active=False).first()
            
            if not patient:
                return {
                    'success': False,
                    'message': 'Paciente no encontrado',
                    'error': 'PATIENT_NOT_FOUND'
                }
            
            patient.is_active = True
            patient.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Paciente reactivado exitosamente'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error al reactivar paciente: {str(e)}',
                'error': 'ACTIVATE_ERROR'
            }
    
    @staticmethod
    def get_patient_statistics() -> Dict[str, Any]:
        """
        Obtener estadísticas de pacientes
        
        Returns:
            Dict con estadísticas
        """
        try:
            total_patients = Patient.query.count()
            active_patients = Patient.query.filter_by(is_active=True).count()
            inactive_patients = total_patients - active_patients
            
            # Pacientes por género
            gender_stats = db.session.query(
                Patient.gender,
                db.func.count(Patient.id)
            ).filter_by(is_active=True).group_by(Patient.gender).all()
            
            # Pacientes creados en los últimos 30 días
            from datetime import timedelta
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_patients = Patient.query.filter(
                Patient.created_at >= thirty_days_ago,
                Patient.is_active == True
            ).count()
            
            return {
                'success': True,
                'data': {
                    'total_patients': total_patients,
                    'active_patients': active_patients,
                    'inactive_patients': inactive_patients,
                    'recent_patients': recent_patients,
                    'gender_distribution': dict(gender_stats)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener estadísticas: {str(e)}',
                'error': 'STATS_ERROR'
            }
