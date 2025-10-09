"""
Configuración global de la aplicación
"""

import os
from datetime import timedelta


class Config:
    """Configuración base"""
    
    # Configuración de la aplicación
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Configuración de base de datos
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://admin:MgYNGdCzjIoTX4MNnmL2oQBDZkhUmKQN@dpg-d36akq0gjchc73c5aumg-a.oregon-postgres.render.com/dbesperanza'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'connect_timeout': 10,
            'application_name': 'lab_esperanza_api'
        }
    }
    
    # Configuración de JWT
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    TOKEN_EXPIRATION = 86400  # 24 horas en segundos
    
    # Configuración de paginación
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    
    # Configuración de sincronización
    SYNC_MAX_RETRY_COUNT = 3
    SYNC_RETRY_DELAY = 300  # 5 minutos en segundos
    
    # Configuración de archivos
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Configuración de reportes HTML
    REPORTS_FOLDER = os.environ.get('REPORTS_FOLDER') or 'reports'
    REPORTS_BASE_PATH = os.environ.get('REPORTS_BASE_PATH') or os.path.join(os.getcwd(), 'reports')
    REPORTS_BACKUP_ENABLED = os.environ.get('REPORTS_BACKUP_ENABLED', 'True').lower() == 'true'
    REPORTS_BACKUP_RETENTION_DAYS = int(os.environ.get('REPORTS_BACKUP_RETENTION_DAYS', 730))  # 2 años
    REPORTS_MAX_FILE_SIZE = int(os.environ.get('REPORTS_MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB
    
    # Configuración de archivos HTML del frontend
    FRONTEND_HTML_FOLDER = os.environ.get('FRONTEND_HTML_FOLDER') or 'frontend_html'
    FRONTEND_HTML_BASE_PATH = os.environ.get('FRONTEND_HTML_BASE_PATH') or os.path.join(os.getcwd(), 'frontend_html')
    FRONTEND_HTML_MAX_FILE_SIZE = int(os.environ.get('FRONTEND_HTML_MAX_FILE_SIZE', 5 * 1024 * 1024))  # 5MB
    FRONTEND_HTML_ALLOWED_EXTENSIONS = {'html', 'htm'}
    FRONTEND_HTML_BACKUP_ENABLED = os.environ.get('FRONTEND_HTML_BACKUP_ENABLED', 'True').lower() == 'true'
    
    # Configuración de CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
    
    # Configuración de email (para notificaciones)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Configuración de API externa (para sincronización)
    EXTERNAL_API_URL = os.environ.get('EXTERNAL_API_URL')
    EXTERNAL_API_KEY = os.environ.get('EXTERNAL_API_KEY')
    EXTERNAL_API_TIMEOUT = int(os.environ.get('EXTERNAL_API_TIMEOUT', 30))
    
    # Configuración de cache
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
    
    # Configuración de rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '100 per hour')
    
    # Configuración de seguridad
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuración de backup
    BACKUP_ENABLED = os.environ.get('BACKUP_ENABLED', 'False').lower() == 'true'
    BACKUP_SCHEDULE = os.environ.get('BACKUP_SCHEDULE', '0 2 * * *')  # Diario a las 2 AM
    BACKUP_RETENTION_DAYS = int(os.environ.get('BACKUP_RETENTION_DAYS', 30))


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://admin:MgYNGdCzjIoTX4MNnmL2oQBDZkhUmKQN@dpg-d36akq0gjchc73c5aumg-a.oregon-postgres.render.com/dbesperanza'
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Configuración para producción"""
    
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    LOG_LEVEL = 'WARNING'
    
    def __init__(self):
        # En producción, estas variables deben estar definidas
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY debe estar definida en producción")
        
        if not os.environ.get('DATABASE_URL'):
            raise ValueError("DATABASE_URL debe estar definida en producción")


class TestingConfig(Config):
    """Configuración para testing"""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Para testing usar SQLite en memoria
    WTF_CSRF_ENABLED = False
    LOG_LEVEL = 'ERROR'


# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
