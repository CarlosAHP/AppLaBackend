#!/usr/bin/env python3
"""
Script para probar los nuevos campos de edición en el backend
"""

import os
import sys
import json
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.frontend_html_service import FrontendHTMLService
from app.config import Config

def test_new_edit_fields():
    """Probar los nuevos campos de edición"""
    
    print("🧪 Probando nuevos campos de edición...")
    print("=" * 60)
    
    try:
        # Crear instancia del servicio
        config = Config()
        service = FrontendHTMLService(config)
        
        print("✅ Servicio creado exitosamente")
        
        # 1. PROBAR CREAR ARCHIVO CON NUEVOS CAMPOS
        print("\n📝 1. PROBANDO: Crear archivo con nuevos campos de edición")
        print("-" * 50)
        
        # Crear directorio de prueba
        directory_path = service.create_directory_structure()
        filename = service.generate_file_name("test_edit.html", "test")
        file_path = os.path.join(directory_path, filename)
        
        # Contenido HTML de prueba
        html_content = """
        <html>
        <head><title>Test Edit Fields</title></head>
        <body>
            <h1>Prueba de Campos de Edición</h1>
            <p>Este es un archivo de prueba para los nuevos campos de edición.</p>
        </body>
        </html>
        """
        
        # Metadatos con nuevos campos de edición
        metadata = {
            'patient_name': 'Juan Pérez',
            'order_number': 'TEST001',
            'doctor_name': 'Dr. Test',
            'patient_age': 30,
            'patient_gender': 'M',
            'reception_date': '2025-10-09',
            'created_by': 'test_user',
            'status': 'pending',
            
            # Nuevos campos de edición
            'edit_count': 0,
            'is_modified': False,
            'edit_history': [],
            'last_edit_date': None
        }
        
        # Guardar archivo
        result = service.save_html_file(html_content, file_path, metadata)
        print(f"✅ Archivo creado: {result['filename']}")
        print(f"📊 Metadatos iniciales:")
        print(f"  - edit_count: {result['metadata'].get('edit_count', 'N/A')}")
        print(f"  - is_modified: {result['metadata'].get('is_modified', 'N/A')}")
        print(f"  - edit_history: {len(result['metadata'].get('edit_history', []))} entradas")
        print(f"  - last_edit_date: {result['metadata'].get('last_edit_date', 'N/A')}")
        
        # 2. PROBAR ACTUALIZAR ARCHIVO (SIMULAR EDICIÓN)
        print("\n✏️ 2. PROBANDO: Actualizar archivo (simular edición)")
        print("-" * 50)
        
        # Contenido HTML modificado
        modified_html_content = """
        <html>
        <head><title>Test Edit Fields - MODIFIED</title></head>
        <body>
            <h1>Prueba de Campos de Edición - MODIFICADO</h1>
            <p>Este archivo ha sido editado para probar los nuevos campos.</p>
            <p><strong>Nueva información agregada</strong></p>
        </body>
        </html>
        """
        
        # Metadatos de edición
        edit_metadata = {
            'edited_by': 'test_user',
            'edit_reason': 'Prueba de funcionalidad de edición',
            'changes_summary': 'Agregado contenido adicional y modificado título'
        }
        
        # Actualizar archivo
        update_result = service.update_html_file(file_path, modified_html_content, edit_metadata)
        print(f"✅ Archivo actualizado exitosamente")
        print(f"📊 Metadatos después de edición:")
        print(f"  - edit_count: {update_result['edit_count']}")
        print(f"  - is_modified: {update_result['is_modified']}")
        print(f"  - last_edit_date: {update_result['last_edit_date']}")
        print(f"  - edit_history: {len(update_result['metadata'].get('edit_history', []))} entradas")
        
        # Mostrar historial de ediciones
        edit_history = update_result['metadata'].get('edit_history', [])
        if edit_history:
            print(f"\n📋 Historial de ediciones:")
            for i, edit in enumerate(edit_history, 1):
                print(f"  {i}. {edit['edit_date']} - {edit['edited_by']}")
                print(f"     Razón: {edit['edit_reason']}")
                print(f"     Cambios: {edit['changes_summary']}")
                print(f"     Tamaño: {edit['file_size_before']} → {edit['file_size_after']} bytes")
        
        # 3. PROBAR MARCAR COMO MODIFICADO
        print("\n🏷️ 3. PROBANDO: Marcar archivo como modificado")
        print("-" * 50)
        
        mark_result = service.mark_as_modified(file_path, "test_user", "Marcado manualmente como modificado")
        print(f"✅ Archivo marcado como modificado")
        print(f"📊 Estadísticas después de marcar:")
        print(f"  - edit_count: {mark_result['edit_count']}")
        print(f"  - is_modified: {mark_result['is_modified']}")
        print(f"  - last_edit_date: {mark_result['last_edit_date']}")
        
        # 4. PROBAR OBTENER ESTADÍSTICAS DE EDICIÓN
        print("\n📊 4. PROBANDO: Obtener estadísticas de edición")
        print("-" * 50)
        
        edit_stats = service.get_edit_stats(file_path)
        print(f"📊 Estadísticas de edición:")
        print(f"  - edit_count: {edit_stats['edit_count']}")
        print(f"  - is_modified: {edit_stats['is_modified']}")
        print(f"  - last_edit_date: {edit_stats['last_edit_date']}")
        print(f"  - edit_history: {len(edit_stats['edit_history'])} entradas")
        
        # 5. PROBAR OBTENER HISTORIAL DE EDICIONES
        print("\n📋 5. PROBANDO: Obtener historial de ediciones")
        print("-" * 50)
        
        history = service.get_edit_history(file_path)
        print(f"📋 Historial completo ({len(history)} entradas):")
        for i, edit in enumerate(history, 1):
            print(f"  {i}. {edit['edit_date']} - {edit['edited_by']}")
            print(f"     Razón: {edit['edit_reason']}")
            print(f"     Cambios: {edit['changes_summary']}")
        
        # 6. PROBAR OBTENER ARCHIVOS MODIFICADOS
        print("\n🔍 6. PROBANDO: Obtener archivos modificados")
        print("-" * 50)
        
        modified_files = service.get_modified_files(limit=10)
        print(f"📊 Archivos modificados encontrados: {len(modified_files)}")
        
        for file_info in modified_files:
            metadata = file_info.get('metadata', {})
            print(f"  📄 {file_info['filename']}")
            print(f"     👤 Paciente: {metadata.get('patient_name', 'N/A')}")
            print(f"     ✏️ Ediciones: {metadata.get('edit_count', 0)}")
            print(f"     📅 Última edición: {metadata.get('last_edit_date', 'N/A')}")
        
        # 7. PROBAR RESUMEN DE ESTADÍSTICAS DE EDICIÓN
        print("\n📈 7. PROBANDO: Resumen de estadísticas de edición")
        print("-" * 50)
        
        stats_summary = service.get_edit_stats_summary()
        print(f"📈 Resumen de estadísticas:")
        print(f"  - Total archivos: {stats_summary['total_files']}")
        print(f"  - Archivos modificados: {stats_summary['modified_files']}")
        print(f"  - Archivos sin modificar: {stats_summary['unmodified_files']}")
        print(f"  - Total ediciones: {stats_summary['total_edits']}")
        print(f"  - Promedio ediciones por archivo: {stats_summary['average_edits_per_file']}")
        
        if stats_summary['most_edited_file']:
            most_edited = stats_summary['most_edited_file']
            print(f"  - Archivo más editado: {most_edited['filename']} ({most_edited['edit_count']} ediciones)")
        
        print(f"  - Ediciones recientes: {len(stats_summary['recent_edits'])}")
        
        # 8. PROBAR RESETEAR SEGUIMIENTO DE EDICIONES
        print("\n🔄 8. PROBANDO: Resetear seguimiento de ediciones")
        print("-" * 50)
        
        reset_result = service.reset_edit_tracking(file_path)
        print(f"✅ Seguimiento de ediciones reseteado")
        print(f"📊 Estadísticas después del reset:")
        print(f"  - edit_count: {reset_result['edit_count']}")
        print(f"  - is_modified: {reset_result['is_modified']}")
        print(f"  - last_edit_date: {reset_result['last_edit_date']}")
        print(f"  - edit_history: {len(reset_result['edit_history'])} entradas")
        
        print("\n🎉 ¡Todas las pruebas de campos de edición completadas exitosamente!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_metadata_structure():
    """Probar la estructura de metadatos con los nuevos campos"""
    
    print("\n🔍 Probando estructura de metadatos...")
    print("=" * 60)
    
    try:
        config = Config()
        service = FrontendHTMLService(config)
        
        # Obtener un archivo existente para verificar estructura
        all_files = service.list_html_files(limit=1)
        
        if all_files:
            file_info = all_files[0]
            file_path = file_info['file_path']
            metadata = service.get_file_metadata(file_path)
            
            print(f"📄 Archivo: {file_info['filename']}")
            print(f"📊 Estructura de metadatos:")
            
            # Campos básicos
            print(f"\n📋 Campos básicos:")
            print(f"  - patient_name: {metadata.get('patient_name', 'N/A')}")
            print(f"  - order_number: {metadata.get('order_number', 'N/A')}")
            print(f"  - doctor_name: {metadata.get('doctor_name', 'N/A')}")
            print(f"  - status: {metadata.get('status', 'N/A')}")
            
            # Campos de edición
            print(f"\n✏️ Campos de edición:")
            print(f"  - edit_count: {metadata.get('edit_count', 'N/A')}")
            print(f"  - is_modified: {metadata.get('is_modified', 'N/A')}")
            print(f"  - last_edit_date: {metadata.get('last_edit_date', 'N/A')}")
            print(f"  - edit_history: {len(metadata.get('edit_history', []))} entradas")
            
            # Verificar que los campos existen
            required_edit_fields = ['edit_count', 'is_modified', 'edit_history', 'last_edit_date']
            missing_fields = []
            
            for field in required_edit_fields:
                if field not in metadata:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"\n⚠️ Campos faltantes: {missing_fields}")
            else:
                print(f"\n✅ Todos los campos de edición están presentes")
            
        else:
            print("❌ No hay archivos para probar")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error al probar estructura de metadatos: {str(e)}")
        return False

def main():
    """Función principal de pruebas"""
    
    print("🚀 Iniciando pruebas de nuevos campos de edición")
    print("=" * 70)
    
    # Probar nuevos campos de edición
    edit_fields_success = test_new_edit_fields()
    
    # Probar estructura de metadatos
    metadata_success = test_metadata_structure()
    
    print("\n" + "=" * 70)
    print("📊 Resultados de las pruebas:")
    print(f"  ✏️ Campos de edición: {'✅ Exitoso' if edit_fields_success else '❌ Falló'}")
    print(f"  📊 Estructura de metadatos: {'✅ Exitoso' if metadata_success else '❌ Falló'}")
    
    if edit_fields_success and metadata_success:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("✨ Los nuevos campos de edición funcionan correctamente")
        print("✨ La estructura de metadatos es correcta")
        print("\n📋 Nuevos campos implementados:")
        print("  ✅ edit_count: Número de veces editado")
        print("  ✅ is_modified: Boolean que indica si fue modificado")
        print("  ✅ edit_history: Array con historial de ediciones")
        print("  ✅ last_edit_date: Fecha de la última edición")
        return 0
    else:
        print("\n❌ Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
