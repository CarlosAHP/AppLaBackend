"""
Archivo principal para ejecutar la aplicación
"""

import os
from flask import Flask
from flask_cors import CORS
from app.config import config
from app.routes import auth_bp, patient_bp, lab_result_bp, payment_bp, sync_bp
from app.routes.lab_tests_routes import lab_tests_bp
from app.routes.lab_report_routes import lab_report_bp
from app.routes.frontend_html_routes import frontend_html_bp
from app.routes.medical_interpretation_routes import medical_interpretation_bp
from database import init_database, test_connection, get_database_info


def create_app(config_name=None):
    """Factory function para crear la aplicación Flask"""
    
    # Obtener configuración
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Cargar configuración
    if config_name == 'production':
        # Para producción, instanciar la clase
        app.config.from_object(config[config_name]())
    else:
        # Para desarrollo y testing, usar la clase directamente
        app.config.from_object(config[config_name])
    
    # Inicializar base de datos
    db = init_database(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(lab_result_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(sync_bp)
    app.register_blueprint(lab_tests_bp)
    app.register_blueprint(lab_report_bp)
    app.register_blueprint(frontend_html_bp, url_prefix='/api/frontend-html')
    app.register_blueprint(medical_interpretation_bp)
    
    # Ruta de salud
    @app.route('/health')
    def health_check():
        """Endpoint de salud de la aplicación"""
        db_status = test_connection()
        db_info = get_database_info() if db_status else None
        
        return {
            'status': 'healthy' if db_status else 'unhealthy',
            'message': 'Laboratorio Esperanza API está funcionando correctamente',
            'version': '1.0.0',
            'database': {
                'connected': db_status,
                'info': db_info
            }
        }, 200 if db_status else 503
    
    # Ruta raíz
    @app.route('/')
    def index():
        """Endpoint raíz de la API"""
        return {
            'message': 'Bienvenido a la API del Laboratorio Esperanza',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'patients': '/api/patients',
                'lab_results': '/api/lab-results',
                'payments': '/api/payments',
                'sync': '/api/sync',
                'lab_tests': '/api/lab-tests',
                'reports': '/api/reports',
                'frontend_html': '/api/frontend-html',
                'medical_interpret': '/api/medical-interpret',
                'health': '/health'
            }
        }, 200
    
    # Manejo de errores
    @app.errorhandler(404)
    def not_found(error):
        """Manejo de error 404"""
        return {
            'success': False,
            'message': 'Endpoint no encontrado',
            'error': 'Not Found'
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Manejo de error 500"""
        return {
            'success': False,
            'message': 'Error interno del servidor',
            'error': 'Internal Server Error'
        }, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        """Manejo de error 400"""
        return {
            'success': False,
            'message': 'Solicitud incorrecta',
            'error': 'Bad Request'
        }, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Manejo de error 401"""
        return {
            'success': False,
            'message': 'No autorizado',
            'error': 'Unauthorized'
        }, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Manejo de error 403"""
        return {
            'success': False,
            'message': 'Acceso prohibido',
            'error': 'Forbidden'
        }, 403
    
    return app


if __name__ == '__main__':
    # Crear aplicación
    app = create_app()
    
    # Ejecutar aplicación
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"Iniciando Laboratorio Esperanza API en puerto {port}")
    print(f"Modo debug: {debug}")
    print(f"URL: http://localhost:{port}")
    print(f"Health check: http://localhost:{port}/health")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        load_dotenv=False
    )
