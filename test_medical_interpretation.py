"""
Script de prueba para la funcionalidad de interpretación médica
"""
import requests
import json
import os
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"
MEDICAL_API_URL = f"{BASE_URL}/api/medical-interpret"

def test_health_check():
    """Probar endpoint de salud"""
    print("🔍 Probando health check...")
    try:
        response = requests.get(f"{MEDICAL_API_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return False

def test_interpret_html():
    """Probar interpretación desde HTML"""
    print("\n🧪 Probando interpretación desde HTML...")
    
    # HTML de ejemplo con resultados de laboratorio
    html_content = """
    <html>
    <head><title>Resultados de Laboratorio</title></head>
    <body>
        <h1>Laboratorio Esperanza - Resultados</h1>
        <h2>Paciente: Juan Pérez</h2>
        <h3>Hematología</h3>
        <ul>
            <li>Hemoglobina: 12.5 g/dl (Normal: 12-16)</li>
            <li>Hematocrito: 38% (Normal: 36-46)</li>
            <li>Leucocitos: 8,500 /μL (Normal: 4,000-11,000)</li>
        </ul>
        <h3>Química Clínica</h3>
        <ul>
            <li>Glucosa: 95 mg/dl (Normal: 70-100)</li>
            <li>Colesterol Total: 180 mg/dl (Normal: <200)</li>
            <li>Triglicéridos: 120 mg/dl (Normal: <150)</li>
        </ul>
    </body>
    </html>
    """
    
    data = {
        "html_content": html_content,
        "patient_info": {
            "age": 35,
            "gender": "M"
        }
    }
    
    try:
        response = requests.post(
            MEDICAL_API_URL,
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        if response.status_code == 200:
            print("✅ Interpretación exitosa!")
            print(f"Interpretación: {result.get('interpretation', 'No disponible')[:200]}...")
        else:
            print(f"❌ Error en interpretación: {result}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error en interpretación HTML: {e}")
        return False

def test_interpret_from_report():
    """Probar interpretación desde reporte existente"""
    print("\n📋 Probando interpretación desde reporte...")
    
    # Usar un ID de reporte existente (ajustar según tu base de datos)
    lab_report_id = 1
    
    data = {
        "patient_info": {
            "age": 28,
            "gender": "F"
        }
    }
    
    try:
        response = requests.post(
            f"{MEDICAL_API_URL}/report/{lab_report_id}",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        if response.status_code == 200:
            print("✅ Interpretación desde reporte exitosa!")
            print(f"Interpretación: {result.get('interpretation', 'No disponible')[:200]}...")
        else:
            print(f"❌ Error en interpretación desde reporte: {result}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error en interpretación desde reporte: {e}")
        return False

def test_invalid_requests():
    """Probar requests inválidos"""
    print("\n🚫 Probando requests inválidos...")
    
    # Test 1: Sin contenido HTML
    try:
        response = requests.post(
            MEDICAL_API_URL,
            json={"patient_info": {"age": 30, "gender": "M"}},
            headers={"Content-Type": "application/json"}
        )
        print(f"Test sin HTML - Status: {response.status_code}")
    except Exception as e:
        print(f"Error en test sin HTML: {e}")
    
    # Test 2: Sin datos
    try:
        response = requests.post(
            MEDICAL_API_URL,
            json={},
            headers={"Content-Type": "application/json"}
        )
        print(f"Test sin datos - Status: {response.status_code}")
    except Exception as e:
        print(f"Error en test sin datos: {e}")

def main():
    """Función principal de pruebas"""
    print("🏥 Pruebas de API de Interpretación Médica")
    print("=" * 50)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ El servidor no está corriendo. Ejecuta: python run.py")
            return
    except Exception as e:
        print(f"❌ No se puede conectar al servidor: {e}")
        print("Asegúrate de que el servidor esté corriendo: python run.py")
        return
    
    print("✅ Servidor conectado correctamente")
    
    # Ejecutar pruebas
    tests = [
        ("Health Check", test_health_check),
        ("Interpretación HTML", test_interpret_html),
        ("Interpretación desde Reporte", test_interpret_from_report),
        ("Requests Inválidos", test_invalid_requests)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen de resultados
    print("\n" + "="*50)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("🎉 ¡Todas las pruebas pasaron! La API está funcionando correctamente.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa la configuración y logs.")

if __name__ == "__main__":
    main()





