"""
Rutas de la API REST
"""

from .auth_routes import auth_bp
from .patient_routes import patient_bp
from .lab_result_routes import lab_result_bp
from .payment_routes import payment_bp
from .sync_routes import sync_bp

__all__ = ['auth_bp', 'patient_bp', 'lab_result_bp', 'payment_bp', 'sync_bp']
