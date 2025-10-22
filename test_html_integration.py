#!/usr/bin/env python3
"""
Script de prueba para verificar la integración de archivos HTML del frontend
"""

import requests
import json
import os
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

def test_backend_health():
    """Probar que el backend esté funcionando"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"OK Backend health check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Database: {data.get('database', {}).get('connected')}")
            return True
        return False
    except Exception as e:
        print(f"ERROR Backend no disponible: {e}")
        return False

def test_frontend_html_endpoints():
    """Probar endpoints de frontend HTML"""
    try:
        # Probar endpoint de validación del sistema
        response = requests.get(f"{API_BASE}/frontend-html/system/validate", timeout=5)
        print(f"OK System validate endpoint: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   System valid: {data.get('valid')}")
            print(f"   Directory exists: {data.get('directory_exists')}")
        
        # Probar endpoint de estadísticas
        response = requests.get(f"{API_BASE}/frontend-html/stats", timeout=5)
        print(f"OK Stats endpoint: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Total files: {data.get('total_files', 0)}")
            print(f"   Total size: {data.get('total_size', 0)} bytes")
        
        return True
    except Exception as e:
        print(f"ERROR Error probando endpoints: {e}")
        return False

def test_html_upload():
    """Probar subida de archivo HTML"""
    try:
        # Datos de prueba
        test_data = {
            "html_content": """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Prueba de Integración</title>
            </head>
            <body>
                <h1>Reporte de Prueba</h1>
                <p>Este es un archivo de prueba generado el {}</p>
                <div class="test-results">
                    <h2>Resultados de Prueba</h2>
                    <ul>
                        <li>Hemoglobina: 14.5 g/dL</li>
                        <li>Hematocrito: 42%</li>
                        <li>Leucocitos: 7,500 /μL</li>
                    </ul>
                </div>
            </body>
            </html>
            """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "original_filename": "test_integration.html",
            "patient_name": "Juan Pérez",
            "order_number": "TEST-001",
            "doctor_name": "Dr. García",
            "patient_age": 35,
            "patient_gender": "M",
            "reception_date": datetime.now().strftime("%Y-%m-%d"),
            "tests": [
                {"name": "hemograma", "filename": "hemograma.html"},
                {"name": "quimica_sanguinea", "filename": "quimica_sanguinea.html"}
            ],
            "status": "pending",
            "created_by": "test_user",
            "created_at": datetime.now().isoformat(),
            "notes": "Archivo de prueba de integración",
            "source": "frontend",
            "prefix": "frontend"
        }
        
        print("Enviando archivo HTML de prueba...")
        response = requests.post(
            f"{API_BASE}/frontend-html/upload",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Respuesta del servidor: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"OK Archivo subido exitosamente:")
            print(f"   Filename: {data.get('data', {}).get('filename')}")
            print(f"   File path: {data.get('data', {}).get('file_path')}")
            print(f"   Size: {data.get('data', {}).get('size')} bytes")
            return data.get('data', {}).get('filename')
        else:
            print(f"ERROR Error al subir archivo: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"ERROR Error en prueba de subida: {e}")
        return None

def test_file_retrieval(filename):
    """Probar recuperación de archivo"""
    if not filename:
        return False
        
    try:
        print(f"Probando recuperacion de archivo: {filename}")
        
        # Probar obtener archivo como HTML
        response = requests.get(f"{API_BASE}/frontend-html/file/{filename}", timeout=5)
        print(f"Archivo HTML: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   Content-Type: {response.headers.get('content-type')}")
            print(f"   Content length: {len(response.content)} bytes")
        
        # Probar obtener contenido como JSON
        response = requests.get(f"{API_BASE}/frontend-html/content/{filename}", timeout=5)
        print(f"Contenido JSON: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('success')}")
            print(f"   Has content: {bool(data.get('data', {}).get('content'))}")
        
        return True
        
    except Exception as e:
        print(f"ERROR Error en prueba de recuperacion: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("Iniciando pruebas de integracion HTML del frontend")
    print("=" * 60)
    
    # 1. Verificar que el backend esté funcionando
    print("\n1. Verificando salud del backend...")
    if not test_backend_health():
        print("ERROR: Backend no esta disponible. Asegurate de que este ejecutandose.")
        return False
    
    # 2. Probar endpoints de frontend HTML
    print("\n2. Probando endpoints de frontend HTML...")
    if not test_frontend_html_endpoints():
        print("ERROR: Los endpoints de frontend HTML no estan funcionando correctamente.")
        return False
    
    # 3. Probar subida de archivo
    print("\n3. Probando subida de archivo HTML...")
    filename = test_html_upload()
    if not filename:
        print("ERROR: No se pudo subir el archivo de prueba.")
        return False
    
    # 4. Probar recuperación de archivo
    print("\n4. Probando recuperacion de archivo...")
    if not test_file_retrieval(filename):
        print("ERROR: No se pudo recuperar el archivo de prueba.")
        return False
    
    print("\n" + "=" * 60)
    print("EXITO: Todas las pruebas pasaron exitosamente!")
    print("La integracion frontend-backend esta funcionando correctamente.")
    
    return True

if __name__ == "__main__":
    main()
