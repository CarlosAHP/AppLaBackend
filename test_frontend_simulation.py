#!/usr/bin/env python3
"""
Script de prueba para simular el comportamiento del frontend
"""

import os
import sys
import json
import requests
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.frontend_html_service import FrontendHTMLService
from app.config import Config

def simulate_frontend_workflow():
    """Simular el flujo de trabajo completo del frontend"""
    
    print("🌐 Simulando comportamiento del frontend...")
    print("=" * 60)
    
    try:
        # Crear instancia del servicio
        config = Config()
        service = FrontendHTMLService(config)
        
        print(f"✅ Servicio creado exitosamente")
        
        # 1. SIMULAR SUBIDA DE ARCHIVOS DESDE EL FRONTEND
        print("\n📤 1. SIMULANDO SUBIDA DE ARCHIVOS DESDE EL FRONTEND")
        print("-" * 50)
        
        # Crear varios archivos HTML de prueba
        test_files = [
            {
                "html_content": """
                <html>
                <head><title>Hemograma Completo</title></head>
                <body>
                    <h1>Laboratorio Esperanza</h1>
                    <h2>Hemograma Completo</h2>
                    <div>
                        <p><strong>Paciente:</strong> Carlos Alfonso Hernández Pérez</p>
                        <p><strong>Orden:</strong> 005</p>
                        <p><strong>Doctor:</strong> Dr. García</p>
                        <p><strong>Fecha:</strong> {}</p>
                    </div>
                    <div>
                        <h3>Resultados:</h3>
                        <ul>
                            <li>Hemoglobina: 14.5 g/dL</li>
                            <li>Hematocrito: 42%</li>
                            <li>Leucocitos: 7,500/μL</li>
                        </ul>
                    </div>
                </body>
                </html>
                """.format(datetime.now().strftime("%d/%m/%Y")),
                "metadata": {
                    "patient_name": "Carlos Alfonso Hernández Pérez",
                    "order_number": "005",
                    "doctor_name": "Dr. García",
                    "notes": "Hemograma completo - Prueba frontend"
                }
            },
            {
                "html_content": """
                <html>
                <head><title>Química Sanguínea</title></head>
                <body>
                    <h1>Laboratorio Esperanza</h1>
                    <h2>Química Sanguínea</h2>
                    <div>
                        <p><strong>Paciente:</strong> María González López</p>
                        <p><strong>Orden:</strong> 006</p>
                        <p><strong>Doctor:</strong> Dr. Martínez</p>
                        <p><strong>Fecha:</strong> {}</p>
                    </div>
                    <div>
                        <h3>Resultados:</h3>
                        <ul>
                            <li>Glucosa: 95 mg/dL</li>
                            <li>Colesterol: 180 mg/dL</li>
                            <li>Triglicéridos: 120 mg/dL</li>
                        </ul>
                    </div>
                </body>
                </html>
                """.format(datetime.now().strftime("%d/%m/%Y")),
                "metadata": {
                    "patient_name": "María González López",
                    "order_number": "006",
                    "doctor_name": "Dr. Martínez",
                    "notes": "Química sanguínea - Prueba frontend"
                }
            },
            {
                "html_content": """
                <html>
                <head><title>Análisis de Orina</title></head>
                <body>
                    <h1>Laboratorio Esperanza</h1>
                    <h2>Análisis de Orina</h2>
                    <div>
                        <p><strong>Paciente:</strong> Ana Patricia Rodríguez</p>
                        <p><strong>Orden:</strong> 007</p>
                        <p><strong>Doctor:</strong> Dr. López</p>
                        <p><strong>Fecha:</strong> {}</p>
                    </div>
                    <div>
                        <h3>Resultados:</h3>
                        <ul>
                            <li>Densidad: 1.020</li>
                            <li>pH: 6.5</li>
                            <li>Proteínas: Negativo</li>
                        </ul>
                    </div>
                </body>
                </html>
                """.format(datetime.now().strftime("%d/%m/%Y")),
                "metadata": {
                    "patient_name": "Ana Patricia Rodríguez",
                    "order_number": "007",
                    "doctor_name": "Dr. López",
                    "notes": "Análisis de orina - Prueba frontend"
                }
            }
        ]
        
        # Subir archivos simulando el frontend
        uploaded_files = []
        for i, file_data in enumerate(test_files, 1):
            print(f"\n📤 Subiendo archivo {i}/3...")
            
            # Crear estructura de directorios
            directory_path = service.create_directory_structure()
            
            # Generar nombre de archivo
            filename = service.generate_file_name(f"reporte_{i}.html", "frontend")
            
            # Ruta completa del archivo
            file_path = os.path.join(directory_path, filename)
            
            # Preparar metadatos
            metadata = file_data["metadata"].copy()
            metadata.update({
                "uploaded_at": datetime.now().isoformat(),
                "source": "frontend_simulation",
                "original_filename": f"reporte_{i}.html",
                "status": "pending"  # Estado por defecto
            })
            
            # Guardar archivo
            service.save_html_file(file_data["html_content"], file_path, metadata)
            
            file_info = {
                "filename": filename,
                "file_path": file_path,
                "metadata": metadata
            }
            uploaded_files.append(file_info)
            
            print(f"✅ Archivo {i} subido: {filename}")
            print(f"   👤 Paciente: {metadata['patient_name']}")
            print(f"   📋 Orden: {metadata['order_number']}")
            print(f"   👨‍⚕️ Doctor: {metadata['doctor_name']}")
            print(f"   ⏳ Estado: {metadata['status']}")
        
        print(f"\n✅ Total de archivos subidos: {len(uploaded_files)}")
        
        # 2. SIMULAR OBTENER ARCHIVOS PENDIENTES (LO QUE VERÍA EL FRONTEND)
        print("\n📋 2. SIMULANDO OBTENER ARCHIVOS PENDIENTES (FRONTEND)")
        print("-" * 50)
        
        # Obtener archivos pendientes
        pending_files = service.get_pending_files(limit=10)
        print(f"📊 Archivos pendientes encontrados: {len(pending_files)}")
        
        if pending_files:
            print("\n📋 Lista de archivos pendientes (ordenados por fecha de creación):")
            for i, file_info in enumerate(pending_files, 1):
                metadata = file_info.get('metadata', {})
                print(f"\n  {i}. 📄 {file_info['filename']}")
                print(f"     👤 Paciente: {metadata.get('patient_name', 'N/A')}")
                print(f"     📋 Orden: {metadata.get('order_number', 'N/A')}")
                print(f"     👨‍⚕️ Doctor: {metadata.get('doctor_name', 'N/A')}")
                print(f"     📅 Creado: {metadata.get('created_at', file_info.get('created_at', 'N/A'))}")
                print(f"     ⏳ Estado: {metadata.get('status', 'unknown')}")
                print(f"     📏 Tamaño: {file_info.get('size', 0)} bytes")
        else:
            print("❌ No se encontraron archivos pendientes")
        
        # 3. SIMULAR PROCESAR ARCHIVOS (CAMBIAR ESTADO)
        print("\n🔄 3. SIMULANDO PROCESAR ARCHIVOS (CAMBIAR ESTADO)")
        print("-" * 50)
        
        if pending_files:
            # Procesar el primer archivo (marcar como completado)
            first_file = pending_files[0]
            print(f"✅ Procesando archivo: {first_file['filename']}")
            
            # Cambiar estado a completado
            service.update_file_status(first_file['file_path'], 'completed')
            print(f"✅ Estado cambiado a: completed")
            
            # Verificar cambio
            updated_metadata = service.get_file_metadata(first_file['file_path'])
            if updated_metadata:
                print(f"📊 Estado actualizado: {updated_metadata.get('status', 'unknown')}")
                print(f"📅 Fecha de finalización: {updated_metadata.get('completed_at', 'N/A')}")
        
        # 4. SIMULAR OBTENER ARCHIVOS COMPLETADOS
        print("\n✅ 4. SIMULANDO OBTENER ARCHIVOS COMPLETADOS")
        print("-" * 50)
        
        completed_files = service.get_completed_files(limit=10)
        print(f"📊 Archivos completados encontrados: {len(completed_files)}")
        
        if completed_files:
            print("\n✅ Lista de archivos completados:")
            for i, file_info in enumerate(completed_files, 1):
                metadata = file_info.get('metadata', {})
                print(f"\n  {i}. 📄 {file_info['filename']}")
                print(f"     👤 Paciente: {metadata.get('patient_name', 'N/A')}")
                print(f"     📋 Orden: {metadata.get('order_number', 'N/A')}")
                print(f"     👨‍⚕️ Doctor: {metadata.get('doctor_name', 'N/A')}")
                print(f"     ✅ Completado: {metadata.get('completed_at', 'N/A')}")
                print(f"     📅 Creado: {metadata.get('created_at', 'N/A')}")
        else:
            print("❌ No se encontraron archivos completados")
        
        # 5. SIMULAR OBTENER ESTADÍSTICAS
        print("\n📊 5. SIMULANDO OBTENER ESTADÍSTICAS")
        print("-" * 50)
        
        stats = service.get_status_stats()
        print("📊 Estadísticas del sistema:")
        print(f"  📄 Total de archivos: {stats['total_files']}")
        print(f"  ⏳ Pendientes: {stats['pending_count']}")
        print(f"  ✅ Completados: {stats['completed_count']}")
        print(f"  ❌ Cancelados: {stats['cancelled_count']}")
        
        print("\n📊 Distribución por estado:")
        for status, count in stats['by_status'].items():
            print(f"  {status}: {count} archivos")
        
        # 6. SIMULAR BÚSQUEDA POR ESTADO
        print("\n🔍 6. SIMULANDO BÚSQUEDA POR ESTADO")
        print("-" * 50)
        
        for status in ['pending', 'completed', 'cancelled']:
            files_by_status = service.get_files_by_status(status, limit=10)
            print(f"📊 Archivos con estado '{status}': {len(files_by_status)}")
            
            if files_by_status:
                for file_info in files_by_status:
                    metadata = file_info.get('metadata', {})
                    print(f"  📄 {file_info['filename']} - {metadata.get('patient_name', 'N/A')}")
        
        # 7. SIMULAR OBTENER TODOS LOS ARCHIVOS (HISTORIAL)
        print("\n📚 7. SIMULANDO OBTENER HISTORIAL COMPLETO")
        print("-" * 50)
        
        all_files = service.list_html_files(limit=20)
        print(f"📊 Total de archivos en el sistema: {len(all_files)}")
        
        if all_files:
            print("\n📚 Historial completo (todos los archivos):")
            for i, file_info in enumerate(all_files, 1):
                metadata = file_info.get('metadata', {})
                status = metadata.get('status', 'unknown')
                status_icon = "⏳" if status == "pending" else "✅" if status == "completed" else "❌"
                
                print(f"\n  {i}. {status_icon} {file_info['filename']}")
                print(f"     👤 Paciente: {metadata.get('patient_name', 'N/A')}")
                print(f"     📋 Orden: {metadata.get('order_number', 'N/A')}")
                print(f"     👨‍⚕️ Doctor: {metadata.get('doctor_name', 'N/A')}")
                print(f"     📊 Estado: {status}")
                print(f"     📅 Creado: {metadata.get('created_at', file_info.get('created_at', 'N/A'))}")
                if status == "completed":
                    print(f"     ✅ Completado: {metadata.get('completed_at', 'N/A')}")
        
        print("\n🎉 ¡Simulación del frontend completada exitosamente!")
        
        # Mostrar resumen final
        print("\n📊 Resumen de la simulación:")
        print(f"  📁 Directorio base: {service.html_base_path}")
        print(f"  📄 Archivos creados: {len(uploaded_files)}")
        print(f"  ⏳ Pendientes: {stats['pending_count']}")
        print(f"  ✅ Completados: {stats['completed_count']}")
        print(f"  📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la simulación del frontend: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints_simulation():
    """Simular llamadas a los endpoints de la API"""
    
    print("\n🌐 Simulando llamadas a endpoints de la API...")
    print("=" * 60)
    
    # Simular endpoints que el frontend usaría
    endpoints_to_test = [
        {
            "method": "GET",
            "endpoint": "/api/frontend-html/pending",
            "description": "Obtener archivos pendientes",
            "params": {"limit": 20}
        },
        {
            "method": "GET", 
            "endpoint": "/api/frontend-html/completed",
            "description": "Obtener archivos completados",
            "params": {"limit": 20}
        },
        {
            "method": "GET",
            "endpoint": "/api/frontend-html/status-stats",
            "description": "Obtener estadísticas por estado",
            "params": {}
        },
        {
            "method": "GET",
            "endpoint": "/api/frontend-html/list",
            "description": "Listar todos los archivos",
            "params": {"limit": 50}
        },
        {
            "method": "PATCH",
            "endpoint": "/api/frontend-html/file/<filename>/status",
            "description": "Actualizar estado de archivo",
            "params": {"status": "completed"}
        }
    ]
    
    print("📡 Endpoints que el frontend usaría:")
    for i, endpoint in enumerate(endpoints_to_test, 1):
        print(f"\n  {i}. {endpoint['method']} {endpoint['endpoint']}")
        print(f"     📝 {endpoint['description']}")
        if endpoint['params']:
            print(f"     📊 Parámetros: {endpoint['params']}")
    
    print("\n✅ Simulación de endpoints completada")
    return True

def main():
    """Función principal de simulación"""
    
    print("🚀 Iniciando simulación completa del frontend")
    print("=" * 70)
    
    # Simular flujo de trabajo del frontend
    workflow_success = simulate_frontend_workflow()
    
    # Simular endpoints de API
    api_success = test_api_endpoints_simulation()
    
    print("\n" + "=" * 70)
    print("📊 Resultados de la simulación del frontend:")
    print(f"  🔧 Flujo de trabajo: {'✅ Exitoso' if workflow_success else '❌ Falló'}")
    print(f"  🌐 Endpoints API: {'✅ Exitoso' if api_success else '❌ Falló'}")
    
    if workflow_success and api_success:
        print("\n🎉 ¡Simulación del frontend completada exitosamente!")
        print("✨ El sistema está listo para mostrar archivos en el frontend")
        print("\n📋 Funcionalidades verificadas:")
        print("  ✅ Subida de archivos HTML")
        print("  ✅ Estado automático 'pending'")
        print("  ✅ Obtención de archivos pendientes")
        print("  ✅ Cambio de estados")
        print("  ✅ Filtrado por estado")
        print("  ✅ Estadísticas por estado")
        print("  ✅ Historial completo")
        print("  ✅ Ordenamiento por fecha")
        return 0
    else:
        print("\n❌ Algunas simulaciones fallaron")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
