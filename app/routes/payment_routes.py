"""
Rutas de Pagos
"""

from flask import Blueprint
from app.controllers.payment_controller import PaymentController

# Crear Blueprint para rutas de pagos
payment_bp = Blueprint('payments', __name__, url_prefix='/api/payments')

# Instanciar controlador
payment_controller = PaymentController()


@payment_bp.route('', methods=['POST'])
def create_payment():
    """Ruta para crear nuevo pago"""
    return payment_controller.create_payment()


@payment_bp.route('', methods=['GET'])
def get_payments():
    """Ruta para obtener lista de pagos"""
    return payment_controller.get_payments()


@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    """Ruta para obtener un pago específico"""
    return payment_controller.get_payment(payment_id)


@payment_bp.route('/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    """Ruta para actualizar pago"""
    return payment_controller.update_payment(payment_id)


@payment_bp.route('/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    """Ruta para eliminar pago"""
    return payment_controller.delete_payment(payment_id)


@payment_bp.route('/<int:payment_id>/status', methods=['PUT'])
def update_payment_status(payment_id):
    """Ruta para actualizar estado del pago"""
    return payment_controller.update_payment_status(payment_id)


@payment_bp.route('/summary', methods=['GET'])
def get_payment_summary():
    """Ruta para obtener resumen de pagos"""
    return payment_controller.get_payment_summary()
