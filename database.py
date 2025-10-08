"""
Configuración y manejo de la base de datos
"""

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()


def init_database(app):
    """Inicializar la base de datos con la aplicación Flask"""
    
    # Configuración específica para PostgreSQL
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql://'):
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'pool_size': 10,
            'max_overflow': 20,
            'connect_args': {
                'connect_timeout': 10,
                'application_name': 'lab_esperanza_api',
                'options': '-c timezone=UTC'
            }
        }
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    
    return db


def create_tables():
    """Crear todas las tablas en la base de datos"""
    from app.models import User, Patient, LabResult, Payment, Sync
    
    try:
        db.create_all()
        print("✅ Tablas creadas exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error al crear tablas: {str(e)}")
        return False


def test_connection():
    """Probar la conexión a la base de datos"""
    try:
        # Intentar una consulta simple
        result = db.session.execute('SELECT 1').fetchone()
        if result:
            print("✅ Conexión a la base de datos exitosa")
            return True
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {str(e)}")
        return False
    
    return False


def get_database_info():
    """Obtener información de la base de datos"""
    try:
        # Obtener información de la conexión
        result = db.session.execute("""
            SELECT 
                current_database() as database_name,
                current_user as user_name,
                version() as version,
                inet_server_addr() as server_address,
                inet_server_port() as server_port
        """).fetchone()
        
        if result:
            return {
                'database_name': result[0],
                'user_name': result[1],
                'version': result[2],
                'server_address': result[3],
                'server_port': result[4],
                'connection_string': db.engine.url.__to_string__(hide_password=True)
            }
    except Exception as e:
        print(f"❌ Error al obtener información de la base de datos: {str(e)}")
        return None
    
    return None
