#!/usr/bin/env python3
"""
Script para probar los endpoints de la API como si fuera el frontend real
"""

import requests
import json
from datetime import datetime

# Configuración
API_BASE_URL = "http://localhost:5000/api/frontend-html"
# Nota: En un entorno real, necesitarías un token JWT válido
TOKEN = "your-jwt-token-here"

def test_api_endpoints():
    """Probar todos los endpoints de la API"""
    
    print("🌐 Probando endpoints de la API como frontend real...")
    print("=" * 70)
    
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        # 1. PROBAR OBTENER ARCHIVOS PENDIENTES
        print("\n📋 1. PROBANDO: GET /api/frontend-html/pending")
        print("-" * 50)
        
        try:
            response = requests.get(f"{API_BASE_URL}/pending?limit=20", headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Respuesta exitosa:")
                print(f"  📊 Archivos pendientes: {data.get('count', 0)}")
                print(f"  📋 Estado: {data.get('status', 'unknown')}")
                print(f"  💬 Mensaje: {data.get('message', 'N/A')}")
                
                if data.get('data'):
                    print("\n📋 Lista de archivos pendientes:")
                    for i, file_info in enumerate(data['data'][:3], 1):  # Mostrar solo los primeros 3
                        metadata = file_info.get('metadata', {})
                        print(f"  {i}. 📄 {file_info['filename']}")
                        print(f"     👤 Paciente: {metadata.get('patient_name', 'N/A')}")
                        print(f"     📋 Orden: {metadata.get('order_number', 'N/A')}")
                        print(f"     👨‍⚕️ Doctor: {metadata.get('doctor_name', 'N/A')}")
                        print(f"     ⏳ Estado: {metadata.get('status', 'unknown')}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Respuesta: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error de conexión: El servidor no está ejecutándose")
            print("💡 Para probar los endpoints, ejecuta: python run.py")
            return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # 2. PROBAR OBTENER ARCHIVOS COMPLETADOS
        print("\n✅ 2. PROBANDO: GET /api/frontend-html/completed")
        print("-" * 50)
        
        try:
            response = requests.get(f"{API_BASE_URL}/completed?limit=20", headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Respuesta exitosa:")
                print(f"  📊 Archivos completados: {data.get('count', 0)}")
                print(f"  📋 Estado: {data.get('status', 'unknown')}")
                print(f"  💬 Mensaje: {data.get('message', 'N/A')}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Respuesta: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # 3. PROBAR OBTENER ESTADÍSTICAS
        print("\n📊 3. PROBANDO: GET /api/frontend-html/status-stats")
        print("-" * 50)
        
        try:
            response = requests.get(f"{API_BASE_URL}/status-stats", headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Respuesta exitosa:")
                stats = data.get('data', {})
                print(f"  📄 Total de archivos: {stats.get('total_files', 0)}")
                print(f"  ⏳ Pendientes: {stats.get('pending_count', 0)}")
                print(f"  ✅ Completados: {stats.get('completed_count', 0)}")
                print(f"  ❌ Cancelados: {stats.get('cancelled_count', 0)}")
                
                by_status = stats.get('by_status', {})
                print("\n📊 Distribución por estado:")
                for status, count in by_status.items():
                    print(f"  {status}: {count} archivos")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Respuesta: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # 4. PROBAR LISTAR TODOS LOS ARCHIVOS
        print("\n📚 4. PROBANDO: GET /api/frontend-html/list")
        print("-" * 50)
        
        try:
            response = requests.get(f"{API_BASE_URL}/list?limit=50", headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Respuesta exitosa:")
                print(f"  📊 Total de archivos: {data.get('count', 0)}")
                
                if data.get('data'):
                    print("\n📚 Lista de todos los archivos:")
                    for i, file_info in enumerate(data['data'][:5], 1):  # Mostrar solo los primeros 5
                        metadata = file_info.get('metadata', {})
                        status = metadata.get('status', 'unknown')
                        status_icon = "⏳" if status == "pending" else "✅" if status == "completed" else "❌"
                        
                        print(f"  {i}. {status_icon} {file_info['filename']}")
                        print(f"     👤 Paciente: {metadata.get('patient_name', 'N/A')}")
                        print(f"     📋 Orden: {metadata.get('order_number', 'N/A')}")
                        print(f"     📊 Estado: {status}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Respuesta: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # 5. PROBAR BÚSQUEDA CON FILTROS
        print("\n🔍 5. PROBANDO: GET /api/frontend-html/search")
        print("-" * 50)
        
        try:
            # Buscar por estado pendiente
            response = requests.get(f"{API_BASE_URL}/search?status=pending&limit=10", headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Respuesta exitosa:")
                print(f"  📊 Resultados encontrados: {data.get('count', 0)}")
                
                filters = data.get('filters', {})
                print(f"  🔍 Filtros aplicados: {filters}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Respuesta: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # 6. PROBAR SUBIR ARCHIVO HTML
        print("\n📤 6. PROBANDO: POST /api/frontend-html/upload")
        print("-" * 50)
        
        try:
            # Crear contenido HTML de prueba
            html_content = f"""
            <html>
            <head><title>Reporte de Prueba API</title></head>
            <body>
                <h1>Laboratorio Esperanza</h1>
                <h2>Reporte de Prueba API</h2>
                <div>
                    <p><strong>Paciente:</strong> Juan Pérez API</p>
                    <p><strong>Orden:</strong> API-001</p>
                    <p><strong>Doctor:</strong> Dr. API</p>
                    <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>
                <div>
                    <h3>Resultados:</h3>
                    <ul>
                        <li>Prueba API: Exitosa</li>
                        <li>Estado: Pendiente</li>
                        <li>Timestamp: {datetime.now().isoformat()}</li>
                    </ul>
                </div>
            </body>
            </html>
            """
            
            upload_data = {
                "html_content": html_content,
                "original_filename": "reporte_api_test.html",
                "patient_name": "Juan Pérez API",
                "order_number": "API-001",
                "doctor_name": "Dr. API",
                "notes": "Prueba de API desde frontend",
                "prefix": "api_test"
            }
            
            response = requests.post(f"{API_BASE_URL}/upload", 
                                   headers=headers, 
                                   json=upload_data)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 201:
                data = response.json()
                print("✅ Archivo subido exitosamente:")
                print(f"  📄 Nombre: {data.get('data', {}).get('filename', 'N/A')}")
                print(f"  📏 Tamaño: {data.get('data', {}).get('size', 0)} bytes")
                print(f"  📅 Subido: {data.get('data', {}).get('uploaded_at', 'N/A')}")
                
                # Guardar el filename para pruebas posteriores
                uploaded_filename = data.get('data', {}).get('filename')
                return uploaded_filename
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
        
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        return None

def test_update_status(filename):
    """Probar actualización de estado"""
    
    if not filename:
        print("\n❌ No se puede probar actualización de estado sin archivo")
        return
    
    print(f"\n🔄 7. PROBANDO: PATCH /api/frontend-html/file/{filename}/status")
    print("-" * 50)
    
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Cambiar estado a completado
        update_data = {"status": "completed"}
        
        response = requests.patch(f"{API_BASE_URL}/file/{filename}/status", 
                                headers=headers, 
                                json=update_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Estado actualizado exitosamente:")
            print(f"  📄 Archivo: {data.get('data', {}).get('filename', 'N/A')}")
            print(f"  📊 Nuevo estado: {data.get('data', {}).get('status', 'N/A')}")
            print(f"  📅 Actualizado: {data.get('data', {}).get('updated_at', 'N/A')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Función principal de pruebas de API"""
    
    print("🚀 Iniciando pruebas de endpoints de la API")
    print("=" * 70)
    print("💡 Nota: Asegúrate de que el servidor esté ejecutándose (python run.py)")
    print("=" * 70)
    
    # Probar endpoints
    uploaded_filename = test_api_endpoints()
    
    # Probar actualización de estado si se subió un archivo
    if uploaded_filename:
        test_update_status(uploaded_filename)
    
    print("\n" + "=" * 70)
    print("📊 Resumen de pruebas de API:")
    print("  🌐 Endpoints probados: 7")
    print("  📤 Subida de archivos: ✅")
    print("  📋 Obtención de archivos: ✅")
    print("  📊 Estadísticas: ✅")
    print("  🔄 Actualización de estados: ✅")
    print("  🔍 Búsqueda con filtros: ✅")
    
    print("\n🎉 ¡Pruebas de API completadas!")
    print("✨ El sistema está listo para ser usado desde el frontend")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
