#!/usr/bin/env python3
"""
Script que simula exactamente lo que el frontend necesita para mostrar archivos
"""

import os
import sys
import json
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.frontend_html_service import FrontendHTMLService
from app.config import Config

def simulate_frontend_display():
    """Simular exactamente lo que el frontend necesita para mostrar archivos"""
    
    print("🖥️ Simulando lo que el frontend necesita para mostrar archivos...")
    print("=" * 70)
    
    try:
        # Crear instancia del servicio
        config = Config()
        service = FrontendHTMLService(config)
        
        print("✅ Servicio inicializado")
        
        # 1. OBTENER ARCHIVOS PENDIENTES (PARA MOSTRAR EN LA INTERFAZ PRINCIPAL)
        print("\n📋 1. OBTENIENDO ARCHIVOS PENDIENTES PARA LA INTERFAZ PRINCIPAL")
        print("-" * 60)
        
        pending_files = service.get_pending_files(limit=20)
        print(f"📊 Archivos pendientes encontrados: {len(pending_files)}")
        
        if pending_files:
            print("\n🖥️ DATOS QUE EL FRONTEND RECIBIRÍA:")
            print("=" * 50)
            
            # Simular la respuesta JSON que recibiría el frontend
            frontend_response = {
                "success": True,
                "data": pending_files,
                "count": len(pending_files),
                "status": "pending",
                "message": f"Se encontraron {len(pending_files)} archivos pendientes"
            }
            
            print("📄 Respuesta JSON para el frontend:")
            print(json.dumps(frontend_response, indent=2, ensure_ascii=False))
            
            print("\n🖥️ CÓMO EL FRONTEND PROCESARÍA ESTOS DATOS:")
            print("=" * 50)
            
            for i, file_info in enumerate(pending_files, 1):
                metadata = file_info.get('metadata', {})
                
                print(f"\n📋 Archivo {i}:")
                print(f"  📄 Nombre: {file_info['filename']}")
                print(f"  👤 Paciente: {metadata.get('patient_name', 'Sin nombre')}")
                print(f"  📋 Orden: {metadata.get('order_number', 'N/A')}")
                print(f"  👨‍⚕️ Doctor: {metadata.get('doctor_name', 'N/A')}")
                print(f"  📅 Creado: {metadata.get('created_at', file_info.get('created_at', 'N/A'))}")
                print(f"  ⏳ Estado: {metadata.get('status', 'unknown')}")
                print(f"  📏 Tamaño: {file_info.get('size', 0)} bytes")
                
                # Simular cómo el frontend mostraría esto en la interfaz
                print(f"\n  🖥️ ELEMENTO HTML QUE SE GENERARÍA:")
                print(f"     <div class='file-item pending'>")
                print(f"       <h4>{metadata.get('patient_name', 'Sin nombre')}</h4>")
                print(f"       <p>Orden: {metadata.get('order_number', 'N/A')}</p>")
                print(f"       <p>Doctor: {metadata.get('doctor_name', 'N/A')}</p>")
                print(f"       <p>Creado: {metadata.get('created_at', 'N/A')}</p>")
                print(f"       <button onclick='markAsCompleted(\"{file_info['filename']}\")'>✅ Completar</button>")
                print(f"       <button onclick='markAsCancelled(\"{file_info['filename']}\")'>❌ Cancelar</button>")
                print(f"     </div>")
        else:
            print("❌ No hay archivos pendientes para mostrar")
        
        # 2. OBTENER ESTADÍSTICAS (PARA EL DASHBOARD)
        print("\n📊 2. OBTENIENDO ESTADÍSTICAS PARA EL DASHBOARD")
        print("-" * 60)
        
        stats = service.get_status_stats()
        print("📊 Estadísticas del sistema:")
        print(f"  📄 Total de archivos: {stats['total_files']}")
        print(f"  ⏳ Pendientes: {stats['pending_count']}")
        print(f"  ✅ Completados: {stats['completed_count']}")
        print(f"  ❌ Cancelados: {stats['cancelled_count']}")
        
        print("\n🖥️ DATOS PARA EL DASHBOARD DEL FRONTEND:")
        print("=" * 50)
        
        dashboard_data = {
            "total_files": stats['total_files'],
            "pending_count": stats['pending_count'],
            "completed_count": stats['completed_count'],
            "cancelled_count": stats['cancelled_count'],
            "by_status": stats['by_status']
        }
        
        print("📊 Respuesta JSON para el dashboard:")
        print(json.dumps(dashboard_data, indent=2, ensure_ascii=False))
        
        print("\n🖥️ ELEMENTOS HTML PARA EL DASHBOARD:")
        print("=" * 50)
        print(f"<div class='dashboard-stats'>")
        print(f"  <div class='stat-item'>")
        print(f"    <span class='stat-number'>{stats['total_files']}</span>")
        print(f"    <span class='stat-label'>Total de Archivos</span>")
        print(f"  </div>")
        print(f"  <div class='stat-item pending'>")
        print(f"    <span class='stat-number'>{stats['pending_count']}</span>")
        print(f"    <span class='stat-label'>Pendientes</span>")
        print(f"  </div>")
        print(f"  <div class='stat-item completed'>")
        print(f"    <span class='stat-number'>{stats['completed_count']}</span>")
        print(f"    <span class='stat-label'>Completados</span>")
        print(f"  </div>")
        print(f"  <div class='stat-item cancelled'>")
        print(f"    <span class='stat-number'>{stats['cancelled_count']}</span>")
        print(f"    <span class='stat-label'>Cancelados</span>")
        print(f"  </div>")
        print(f"</div>")
        
        # 3. OBTENER ARCHIVOS COMPLETADOS (PARA EL HISTORIAL)
        print("\n✅ 3. OBTENIENDO ARCHIVOS COMPLETADOS PARA EL HISTORIAL")
        print("-" * 60)
        
        completed_files = service.get_completed_files(limit=20)
        print(f"📊 Archivos completados encontrados: {len(completed_files)}")
        
        if completed_files:
            print("\n🖥️ DATOS PARA EL HISTORIAL DEL FRONTEND:")
            print("=" * 50)
            
            for i, file_info in enumerate(completed_files, 1):
                metadata = file_info.get('metadata', {})
                
                print(f"\n✅ Archivo completado {i}:")
                print(f"  📄 Nombre: {file_info['filename']}")
                print(f"  👤 Paciente: {metadata.get('patient_name', 'Sin nombre')}")
                print(f"  📋 Orden: {metadata.get('order_number', 'N/A')}")
                print(f"  👨‍⚕️ Doctor: {metadata.get('doctor_name', 'N/A')}")
                print(f"  ✅ Completado: {metadata.get('completed_at', 'N/A')}")
                print(f"  📅 Creado: {metadata.get('created_at', 'N/A')}")
                
                # Simular cómo el frontend mostraría esto en el historial
                print(f"\n  🖥️ ELEMENTO HTML PARA EL HISTORIAL:")
                print(f"     <div class='history-item completed'>")
                print(f"       <div class='file-info'>")
                print(f"         <h4>{metadata.get('patient_name', 'Sin nombre')}</h4>")
                print(f"         <p>Orden: {metadata.get('order_number', 'N/A')}</p>")
                print(f"         <p>Doctor: {metadata.get('doctor_name', 'N/A')}</p>")
                print(f"         <p>Completado: {metadata.get('completed_at', 'N/A')}</p>")
                print(f"       </div>")
                print(f"       <div class='file-actions'>")
                print(f"         <button onclick='viewFile(\"{file_info['filename']}\")'>👁️ Ver</button>")
                print(f"         <button onclick='downloadFile(\"{file_info['filename']}\")'>📥 Descargar</button>")
                print(f"       </div>")
                print(f"     </div>")
        else:
            print("❌ No hay archivos completados para mostrar en el historial")
        
        # 4. SIMULAR ACTUALIZACIÓN DE ESTADO (DESDE EL FRONTEND)
        print("\n🔄 4. SIMULANDO ACTUALIZACIÓN DE ESTADO DESDE EL FRONTEND")
        print("-" * 60)
        
        if pending_files:
            # Tomar el primer archivo pendiente
            first_file = pending_files[0]
            print(f"🔄 Procesando archivo: {first_file['filename']}")
            
            # Simular cambio de estado a completado
            service.update_file_status(first_file['file_path'], 'completed')
            print("✅ Estado cambiado a: completed")
            
            # Verificar el cambio
            updated_metadata = service.get_file_metadata(first_file['file_path'])
            if updated_metadata:
                print(f"📊 Estado actualizado: {updated_metadata.get('status', 'unknown')}")
                print(f"📅 Fecha de finalización: {updated_metadata.get('completed_at', 'N/A')}")
                
                print("\n🖥️ RESPUESTA JSON PARA EL FRONTEND:")
                print("=" * 50)
                update_response = {
                    "success": True,
                    "message": f"Estado del archivo {first_file['filename']} actualizado a completed",
                    "data": {
                        "filename": first_file['filename'],
                        "status": "completed",
                        "updated_at": updated_metadata.get('updated_at', 'N/A')
                    }
                }
                print(json.dumps(update_response, indent=2, ensure_ascii=False))
        
        # 5. MOSTRAR ESTRUCTURA COMPLETA DE DATOS PARA EL FRONTEND
        print("\n📋 5. ESTRUCTURA COMPLETA DE DATOS PARA EL FRONTEND")
        print("-" * 60)
        
        # Obtener todos los archivos para mostrar la estructura completa
        all_files = service.list_html_files(limit=50)
        
        print("🖥️ ESTRUCTURA COMPLETA DE DATOS:")
        print("=" * 50)
        
        complete_data = {
            "success": True,
            "data": all_files,
            "count": len(all_files),
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
        
        print("📄 Respuesta JSON completa:")
        print(json.dumps(complete_data, indent=2, ensure_ascii=False))
        
        print("\n🎉 ¡Simulación de display del frontend completada exitosamente!")
        
        # Mostrar resumen final
        print("\n📊 Resumen de datos para el frontend:")
        print(f"  📁 Directorio base: {service.html_base_path}")
        print(f"  📄 Total de archivos: {len(all_files)}")
        print(f"  ⏳ Pendientes: {stats['pending_count']}")
        print(f"  ✅ Completados: {stats['completed_count']}")
        print(f"  📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la simulación del display: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal de simulación de display"""
    
    print("🚀 Iniciando simulación de display del frontend")
    print("=" * 70)
    
    # Simular display del frontend
    display_success = simulate_frontend_display()
    
    print("\n" + "=" * 70)
    print("📊 Resultados de la simulación de display:")
    print(f"  🖥️ Display del frontend: {'✅ Exitoso' if display_success else '❌ Falló'}")
    
    if display_success:
        print("\n🎉 ¡Simulación de display completada exitosamente!")
        print("✨ El sistema está listo para mostrar archivos en el frontend")
        print("\n📋 Datos disponibles para el frontend:")
        print("  ✅ Archivos pendientes (ordenados por fecha)")
        print("  ✅ Estadísticas del sistema")
        print("  ✅ Archivos completados (historial)")
        print("  ✅ Actualización de estados")
        print("  ✅ Estructura JSON completa")
        print("  ✅ Elementos HTML de ejemplo")
        return 0
    else:
        print("\n❌ La simulación de display falló")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
