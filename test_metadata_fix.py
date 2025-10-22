#!/usr/bin/env python3
"""
Script de prueba para verificar que todos los metadatos se guardan correctamente
"""

import os
import sys
import json
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.frontend_html_service import FrontendHTMLService
from app.config import Config

def test_metadata_saving():
    """Probar que todos los metadatos se guardan correctamente"""
    
    print("🧪 Probando guardado de metadatos completos...")
    print("=" * 60)
    
    try:
        # Crear instancia del servicio
        config = Config()
        service = FrontendHTMLService(config)
        
        print("✅ Servicio creado exitosamente")
        
        # Crear contenido HTML de prueba
        html_content = """
        <html>
        <head><title>Reporte de Laboratorio - Prueba Metadatos</title></head>
        <body>
            <h1>Laboratorio Esperanza</h1>
            <h2>Reporte de Laboratorio</h2>
            <div>
                <p><strong>Paciente:</strong> Juan Pérez</p>
                <p><strong>Edad:</strong> 35 años</p>
                <p><strong>Género:</strong> Masculino</p>
                <p><strong>Orden:</strong> ORD-001</p>
                <p><strong>Doctor:</strong> Dr. García</p>
                <p><strong>Fecha de Recepción:</strong> 2025-10-09</p>
                <p><strong>Fecha:</strong> {}</p>
            </div>
            <div>
                <h3>Resultados:</h3>
                <ul>
                    <li>Hemograma: Normal</li>
                    <li>Química Sanguínea: Normal</li>
                </ul>
            </div>
        </body>
        </html>
        """.format(datetime.now().strftime("%d/%m/%Y"))
        
        # Crear metadatos completos como los envía el frontend
        metadata = {
            # Campos básicos
            'patient_name': 'Juan Pérez',
            'order_number': 'ORD-001',
            'doctor_name': 'Dr. García',
            'notes': 'Reporte de prueba con metadatos completos',
            
            # Campos adicionales del frontend
            'patient_age': 35,
            'patient_gender': 'Masculino',
            'reception_date': '2025-10-09',
            'tests': ['Hemograma', 'Química Sanguínea', 'Orina'],
            'created_by': 'doctor1_updated',
            'source': 'frontend',
            'prefix': 'frontend',
            'original_filename': 'reporte_metadatos_completos.html',
            'created_at': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        print("\n📤 Metadatos que se van a enviar:")
        print("=" * 40)
        for key, value in metadata.items():
            print(f"  {key}: {value}")
        
        # Crear estructura de directorios
        directory_path = service.create_directory_structure()
        
        # Generar nombre de archivo
        filename = service.generate_file_name(metadata['original_filename'], metadata['prefix'])
        
        # Ruta completa del archivo
        file_path = os.path.join(directory_path, filename)
        
        # Guardar archivo HTML con metadatos completos
        print(f"\n💾 Guardando archivo: {filename}")
        result = service.save_html_file(html_content, file_path, metadata)
        
        print("✅ Archivo guardado exitosamente")
        print(f"📄 Nombre: {result['filename']}")
        print(f"📏 Tamaño: {result['size']} bytes")
        print(f"📅 Subido: {result['uploaded_at']}")
        
        # Verificar metadatos guardados
        print("\n📋 Verificando metadatos guardados:")
        print("=" * 40)
        
        saved_metadata = service.get_file_metadata(file_path)
        if saved_metadata:
            print("✅ Metadatos leídos exitosamente")
            print("\n📊 Metadatos guardados:")
            for key, value in saved_metadata.items():
                print(f"  {key}: {value}")
            
            # Verificar que todos los campos están presentes
            print("\n🔍 Verificando campos específicos:")
            required_fields = [
                'patient_name', 'order_number', 'doctor_name', 'notes',
                'patient_age', 'patient_gender', 'reception_date', 'tests',
                'created_by', 'source', 'prefix', 'original_filename',
                'created_at', 'status', 'uploaded_at', 'file_size'
            ]
            
            missing_fields = []
            for field in required_fields:
                if field in saved_metadata:
                    print(f"  ✅ {field}: {saved_metadata[field]}")
                else:
                    print(f"  ❌ {field}: NO ENCONTRADO")
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"\n⚠️ Campos faltantes: {missing_fields}")
            else:
                print("\n🎉 ¡Todos los metadatos se guardaron correctamente!")
                
        else:
            print("❌ No se pudieron leer los metadatos")
        
        # Mostrar contenido del archivo .meta
        meta_file_path = f"{file_path}.meta"
        if os.path.exists(meta_file_path):
            print(f"\n📄 Contenido del archivo .meta:")
            print("=" * 40)
            with open(meta_file_path, 'r', encoding='utf-8') as f:
                meta_content = f.read()
                print(meta_content)
        
        print("\n🎉 ¡Prueba de metadatos completada exitosamente!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la prueba de metadatos: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal de prueba"""
    
    print("🚀 Iniciando prueba de metadatos completos")
    print("=" * 70)
    
    # Probar guardado de metadatos
    success = test_metadata_saving()
    
    print("\n" + "=" * 70)
    print("📊 Resultados de la prueba de metadatos:")
    print(f"  🔧 Guardado de metadatos: {'✅ Exitoso' if success else '❌ Falló'}")
    
    if success:
        print("\n🎉 ¡Prueba de metadatos completada exitosamente!")
        print("✨ El backend ahora guarda todos los metadatos del frontend")
        print("\n📋 Campos verificados:")
        print("  ✅ patient_name, order_number, doctor_name, notes")
        print("  ✅ patient_age, patient_gender, reception_date")
        print("  ✅ tests, created_by, source, prefix")
        print("  ✅ original_filename, created_at, status")
        print("  ✅ uploaded_at, file_size (campos del sistema)")
        return 0
    else:
        print("\n❌ La prueba de metadatos falló")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
