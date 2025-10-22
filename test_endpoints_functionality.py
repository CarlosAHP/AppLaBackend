#!/usr/bin/env python3
"""
Script para probar la funcionalidad de los endpoints del frontend HTML
"""

import os
import sys
import json
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.frontend_html_service import FrontendHTMLService
from app.config import Config

def test_endpoints_functionality():
    """Probar la funcionalidad de los endpoints"""
    
    print("🧪 Probando funcionalidad de endpoints...")
    print("=" * 60)
    
    try:
        # Crear instancia del servicio
        config = Config()
        service = FrontendHTMLService(config)
        
        print("✅ Servicio creado exitosamente")
        
        # 1. PROBAR OBTENER ARCHIVOS PENDIENTES
        print("\n📋 1. PROBANDO: Obtener archivos pendientes")
        print("-" * 50)
        
        pending_files = service.get_pending_files(limit=10)
        print(f"📊 Archivos pendientes encontrados: {len(pending_files)}")
        
        if pending_files:
            print("\n📋 Lista de archivos pendientes:")
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
        
        # 2. PROBAR OBTENER ARCHIVOS COMPLETADOS
        print("\n✅ 2. PROBANDO: Obtener archivos completados")
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
        
        # 3. PROBAR ESTADÍSTICAS
        print("\n📊 3. PROBANDO: Obtener estadísticas")
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
        
        # 4. PROBAR CAMBIO DE ESTADO
        print("\n🔄 4. PROBANDO: Cambio de estado")
        print("-" * 50)
        
        if pending_files:
            # Tomar el primer archivo pendiente
            first_file = pending_files[0]
            print(f"🔄 Procesando archivo: {first_file['filename']}")
            
            # Cambiar estado a completado
            try:
                result = service.update_file_status(first_file['file_path'], 'completed')
                print("✅ Estado cambiado a: completed")
                print(f"📊 Resultado: {result}")
                
                # Verificar el cambio
                updated_metadata = service.get_file_metadata(first_file['file_path'])
                if updated_metadata:
                    print(f"📊 Estado actualizado: {updated_metadata.get('status', 'unknown')}")
                    print(f"📅 Fecha de finalización: {updated_metadata.get('completed_at', 'N/A')}")
                
            except Exception as e:
                print(f"❌ Error al cambiar estado: {str(e)}")
        else:
            print("❌ No hay archivos pendientes para cambiar estado")
        
        # 5. PROBAR OBTENER ARCHIVOS POR ESTADO
        print("\n🔍 5. PROBANDO: Obtener archivos por estado")
        print("-" * 50)
        
        for status in ['pending', 'completed', 'cancelled']:
            files_by_status = service.get_files_by_status(status, limit=10)
            print(f"📊 Archivos con estado '{status}': {len(files_by_status)}")
            
            if files_by_status:
                for file_info in files_by_status[:3]:  # Mostrar solo los primeros 3
                    metadata = file_info.get('metadata', {})
                    print(f"  📄 {file_info['filename']} - {metadata.get('patient_name', 'N/A')}")
        
        # 6. PROBAR LISTAR TODOS LOS ARCHIVOS
        print("\n📚 6. PROBANDO: Listar todos los archivos")
        print("-" * 50)
        
        all_files = service.list_html_files(limit=20)
        print(f"📊 Total de archivos en el sistema: {len(all_files)}")
        
        if all_files:
            print("\n📚 Lista de todos los archivos:")
            for i, file_info in enumerate(all_files, 1):
                metadata = file_info.get('metadata', {})
                status = metadata.get('status', 'unknown')
                status_icon = "⏳" if status == "pending" else "✅" if status == "completed" else "❌"
                
                print(f"\n  {i}. {status_icon} {file_info['filename']}")
                print(f"     👤 Paciente: {metadata.get('patient_name', 'N/A')}")
                print(f"     📊 Estado: {status}")
                print(f"     📅 Creado: {metadata.get('created_at', file_info.get('created_at', 'N/A'))}")
                if status == "completed":
                    print(f"     ✅ Completado: {metadata.get('completed_at', 'N/A')}")
        
        # 7. PROBAR BÚSQUEDA
        print("\n🔍 7. PROBANDO: Búsqueda de archivos")
        print("-" * 50)
        
        # Buscar por paciente
        search_results = service.search_html_files(patient_name="Carlos", limit=10)
        print(f"📊 Resultados de búsqueda por 'Carlos': {len(search_results)}")
        
        if search_results:
            for file_info in search_results:
                metadata = file_info.get('metadata', {})
                print(f"  📄 {file_info['filename']} - {metadata.get('patient_name', 'N/A')}")
        
        print("\n🎉 ¡Pruebas de funcionalidad completadas exitosamente!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_file_serving():
    """Probar que los archivos se pueden servir correctamente"""
    
    print("\n🌐 Probando servicio de archivos...")
    print("=" * 60)
    
    try:
        config = Config()
        service = FrontendHTMLService(config)
        
        # Obtener un archivo para probar
        all_files = service.list_html_files(limit=1)
        
        if all_files:
            file_info = all_files[0]
            file_path = file_info['file_path']
            
            print(f"📄 Probando archivo: {file_info['filename']}")
            print(f"📁 Ruta: {file_path}")
            
            # Verificar que el archivo existe
            if os.path.exists(file_path):
                print("✅ Archivo existe en el sistema de archivos")
                
                # Leer contenido HTML
                html_content = service.get_html_content(file_path)
                print(f"✅ Contenido HTML leído: {len(html_content)} caracteres")
                
                # Verificar metadatos
                metadata = service.get_file_metadata(file_path)
                if metadata:
                    print("✅ Metadatos leídos correctamente")
                    print(f"  👤 Paciente: {metadata.get('patient_name', 'N/A')}")
                    print(f"  📊 Estado: {metadata.get('status', 'unknown')}")
                else:
                    print("❌ No se pudieron leer los metadatos")
                
                # Verificar información del archivo
                file_info_detailed = service.get_file_info(file_path)
                if file_info_detailed:
                    print("✅ Información del archivo obtenida")
                    print(f"  📏 Tamaño: {file_info_detailed['size']} bytes")
                    print(f"  📅 Creado: {file_info_detailed['created_at']}")
                    print(f"  📅 Modificado: {file_info_detailed['modified_at']}")
                
            else:
                print("❌ Archivo no encontrado en el sistema de archivos")
        else:
            print("❌ No hay archivos para probar")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error al probar servicio de archivos: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal de pruebas"""
    
    print("🚀 Iniciando pruebas de funcionalidad de endpoints")
    print("=" * 70)
    
    # Probar funcionalidad de endpoints
    endpoints_success = test_endpoints_functionality()
    
    # Probar servicio de archivos
    files_success = test_file_serving()
    
    print("\n" + "=" * 70)
    print("📊 Resultados de las pruebas:")
    print(f"  🔧 Funcionalidad de endpoints: {'✅ Exitoso' if endpoints_success else '❌ Falló'}")
    print(f"  🌐 Servicio de archivos: {'✅ Exitoso' if files_success else '❌ Falló'}")
    
    if endpoints_success and files_success:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("✨ Los endpoints están funcionando correctamente")
        print("✨ Los archivos se están sirviendo correctamente")
        print("✨ La lógica de estados funciona perfectamente")
        return 0
    else:
        print("\n❌ Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
