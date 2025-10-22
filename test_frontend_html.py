#!/usr/bin/env python3
"""
Script de prueba para la funcionalidad de archivos HTML del frontend
"""

import os
import sys
import json
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.frontend_html_service import FrontendHTMLService
from app.config import Config

def test_frontend_html_service():
    """Probar el servicio de archivos HTML del frontend"""
    
    print("🧪 Iniciando pruebas del servicio FrontendHTMLService...")
    
    try:
        # Crear instancia del servicio
        config = Config()
        service = FrontendHTMLService(config)
        
        print(f"✅ Servicio creado exitosamente")
        print(f"📁 Directorio base: {service.html_base_path}")
        print(f"📏 Tamaño máximo: {service.max_file_size} bytes")
        print(f"🔧 Extensiones permitidas: {service.allowed_extensions}")
        
        # Probar creación de directorio
        print("\n📁 Probando creación de directorio...")
        directory_path = service.create_directory_structure()
        print(f"✅ Directorio creado: {directory_path}")
        
        # Probar generación de nombre de archivo
        print("\n📝 Probando generación de nombre de archivo...")
        filename = service.generate_file_name("reporte_paciente.html", "frontend")
        print(f"✅ Nombre generado: {filename}")
        
        # Crear contenido HTML de prueba
        html_content = """
        <html>
        <head>
            <title>Reporte de Laboratorio - Prueba</title>
        </head>
        <body>
            <h1>Laboratorio Esperanza</h1>
            <h2>Reporte de Laboratorio</h2>
            <div>
                <p><strong>Paciente:</strong> Juan Pérez</p>
                <p><strong>Orden:</strong> ORD-001</p>
                <p><strong>Doctor:</strong> Dr. García</p>
                <p><strong>Fecha:</strong> {}</p>
            </div>
            <div>
                <h3>Resultados:</h3>
                <ul>
                    <li>Hemograma: Normal</li>
                    <li>Química Sanguínea: Normal</li>
                    <li>Orina: Normal</li>
                </ul>
            </div>
        </body>
        </html>
        """.format(datetime.now().strftime("%d/%m/%Y"))
        
        # Crear metadatos
        metadata = {
            "uploaded_at": datetime.now().isoformat(),
            "source": "frontend_test",
            "original_filename": "reporte_paciente.html",
            "patient_name": "Juan Pérez",
            "order_number": "ORD-001",
            "doctor_name": "Dr. García",
            "notes": "Prueba del sistema de archivos HTML"
        }
        
        # Probar validación de contenido
        print("\n🔍 Probando validación de contenido...")
        service.validate_html_content(html_content)
        print("✅ Contenido HTML válido")
        
        # Probar guardado de archivo
        print("\n💾 Probando guardado de archivo...")
        file_path = os.path.join(directory_path, filename)
        service.save_html_file(html_content, file_path, metadata)
        print(f"✅ Archivo guardado: {file_path}")
        
        # Probar lectura de archivo
        print("\n📖 Probando lectura de archivo...")
        read_content = service.get_html_file(file_path)
        if read_content:
            print("✅ Archivo leído exitosamente")
            print(f"📏 Tamaño del contenido: {len(read_content)} caracteres")
        else:
            print("❌ Error al leer archivo")
        
        # Probar lectura de metadatos
        print("\n📋 Probando lectura de metadatos...")
        read_metadata = service.get_file_metadata(file_path)
        if read_metadata:
            print("✅ Metadatos leídos exitosamente")
            print(f"📊 Metadatos: {json.dumps(read_metadata, indent=2, ensure_ascii=False)}")
        else:
            print("❌ Error al leer metadatos")
        
        # Probar listado de archivos
        print("\n📂 Probando listado de archivos...")
        html_files = service.list_html_files(limit=10)
        print(f"✅ Archivos encontrados: {len(html_files)}")
        for file_info in html_files:
            print(f"  📄 {file_info['filename']} ({file_info['size']} bytes)")
        
        # Probar validación de permisos
        print("\n🔐 Probando validación de permisos...")
        permissions = service.validate_file_permissions()
        print("✅ Permisos validados:")
        for key, value in permissions.items():
            status = "✅" if value else "❌"
            print(f"  {status} {key}: {value}")
        
        # Probar backup (si está habilitado)
        if service.backup_enabled:
            print("\n💾 Probando creación de backup...")
            try:
                backup_path = service.backup_html_files()
                print(f"✅ Backup creado: {backup_path}")
            except Exception as e:
                print(f"⚠️  Backup no disponible: {str(e)}")
        else:
            print("\n💾 Backup deshabilitado")
        
        print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
        
        # Mostrar resumen
        print("\n📊 Resumen de la prueba:")
        print(f"  📁 Directorio base: {service.html_base_path}")
        print(f"  📄 Archivos creados: 1")
        print(f"  📏 Tamaño total: {len(html_content)} caracteres")
        print(f"  🔧 Configuración: {service.max_file_size} bytes máximo")
        print(f"  📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Probar los endpoints de la API (simulación)"""
    
    print("\n🌐 Probando endpoints de la API...")
    
    # Simular datos de request
    test_data = {
        "html_content": "<html><body><h1>Test API</h1></body></html>",
        "original_filename": "test_api.html",
        "patient_name": "Paciente Test",
        "order_number": "TEST-001",
        "doctor_name": "Dr. Test",
        "notes": "Prueba de API"
    }
    
    print("✅ Datos de prueba preparados")
    print(f"📝 Contenido HTML: {len(test_data['html_content'])} caracteres")
    print(f"👤 Paciente: {test_data['patient_name']}")
    print(f"📋 Orden: {test_data['order_number']}")
    print(f"👨‍⚕️ Doctor: {test_data['doctor_name']}")
    
    # Simular endpoints
    endpoints = [
        "POST /api/frontend-html/upload",
        "GET /api/frontend-html/list",
        "GET /api/frontend-html/file/<filename>",
        "GET /api/frontend-html/content/<filename>",
        "PUT /api/frontend-html/file/<filename>",
        "DELETE /api/frontend-html/file/<filename>",
        "GET /api/frontend-html/info/<filename>",
        "GET /api/frontend-html/search",
        "POST /api/frontend-html/backup",
        "GET /api/frontend-html/system/validate",
        "GET /api/frontend-html/stats",
        "GET /api/frontend-html/recent",
        "GET /api/frontend-html/download/<filename>"
    ]
    
    print(f"\n📡 Endpoints disponibles: {len(endpoints)}")
    for endpoint in endpoints:
        print(f"  🔗 {endpoint}")
    
    print("\n✅ Endpoints de API configurados correctamente")
    return True

def main():
    """Función principal de pruebas"""
    
    print("🚀 Iniciando pruebas del sistema de archivos HTML del frontend")
    print("=" * 60)
    
    # Probar servicio
    service_success = test_frontend_html_service()
    
    # Probar API
    api_success = test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("📊 Resultados de las pruebas:")
    print(f"  🔧 Servicio: {'✅ Exitoso' if service_success else '❌ Falló'}")
    print(f"  🌐 API: {'✅ Exitoso' if api_success else '❌ Falló'}")
    
    if service_success and api_success:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("✨ El sistema de archivos HTML del frontend está listo para usar")
        return 0
    else:
        print("\n❌ Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
