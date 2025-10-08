"""
Laboratorio Esperanza - Backend Application
"""

__version__ = "1.0.0"
__author__ = "Laboratorio Esperanza"


def create_app(config_name=None):
    """Factory function para crear la aplicación Flask"""
    from run import create_app as _create_app
    return _create_app(config_name)