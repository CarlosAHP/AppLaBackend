"""
Rutas para servir las pruebas de laboratorio HTML
"""

from flask import Blueprint, send_file, jsonify, request
from pathlib import Path
import os

# Crear el blueprint para las rutas de pruebas de laboratorio
lab_tests_bp = Blueprint('lab_tests', __name__, url_prefix='/api/lab-tests')

@lab_tests_bp.route('/html/<filename>')
def serve_lab_test_html(filename):
    """
    Servir archivos HTML de pruebas de laboratorio
    
    GET /api/lab-tests/html/<filename>
    """
    try:
        # Ruta a los archivos HTML
        html_dir = Path("bocetos_pruebas/html_output")
        file_path = html_dir / filename
        
        # Verificar que el archivo existe
        if not file_path.exists():
            return jsonify({
                'success': False,
                'message': f'Archivo {filename} no encontrado'
            }), 404
        
        # Verificar que es un archivo HTML
        if not filename.endswith('.html'):
            return jsonify({
                'success': False,
                'message': 'Solo se permiten archivos HTML'
            }), 400
        
        # Servir el archivo HTML
        return send_file(file_path, mimetype='text/html')
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al servir archivo: {str(e)}'
        }), 500

@lab_tests_bp.route('/list')
def list_lab_tests():
    """
    Listar todas las pruebas de laboratorio disponibles
    
    GET /api/lab-tests/list
    """
    try:
        html_dir = Path("bocetos_pruebas/html_output")
        
        if not html_dir.exists():
            return jsonify({
                'success': False,
                'message': 'Directorio de pruebas no encontrado'
            }), 404
        
        # Buscar todos los archivos HTML
        html_files = []
        for file_path in html_dir.glob("*.html"):
            if file_path.name != "index.html":  # Excluir el índice
                html_files.append({
                    'filename': file_path.name,
                    'name': file_path.stem,
                    'url': f'/api/lab-tests/html/{file_path.name}',
                    'size': file_path.stat().st_size,
                    'modified': file_path.stat().st_mtime
                })
        
        # Ordenar por nombre
        html_files.sort(key=lambda x: x['name'])
        
        return jsonify({
            'success': True,
            'data': html_files,
            'total': len(html_files)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al listar archivos: {str(e)}'
        }), 500

@lab_tests_bp.route('/categories')
def get_categories():
    """
    Obtener categorías de pruebas de laboratorio
    
    GET /api/lab-tests/categories
    """
    try:
        categories = {
            'Hematología': [
                '3. HEMATOLOGIA.html',
                '15. FROTE PERIFERICO, CLASIFICACION DE ANEMIA.html',
                '22. HEMATOLOGIA CANINO.html',
                '23. HEMATOLOGIA (FELINO).html',
                'frote_periferico.html',
                'clasificacion_anemia.html',
                'gota_gruesa.html'
            ],
            'Bioquímica': [
                '4. QUIMICA CLINICA.html',
                '5. ENZIMAS.html',
                '6. ELECTROLITOS.html',
                '10. ENDOCRINOLOGIA.html'
            ],
            'Microbiología': [
                '14. CULTIVOS VARIOS.html',
                '16. HELICOBACTER PYLORI.html',
                '17. MICROBIOLOGIA.html',
                'urocultivo_negativo.html',
                'urocultivo_positivo.html',
                'orocultivo.html',
                'secrecion_vaginal.html',
                'coprocultivo.html',
                'helicobacter_antigeno_heces.html',
                'azul_metileno.html',
                'transferrina_heces.html',
                'virus_heces.html',
                'sangre_oculta_heces.html',
                'helicobacter_igm_1.html',
                'helicobacter_igg_1.html',
                'helicobacter_igm_igg_2.html',
                'panel_parasitos.html',
                'clostridium_difficile.html',
                'clinitest_1.html',
                'clinitest_2.html',
                'clinitest_sudan_calprotectina.html',
                'helicobacter_igg_3.html',
                'ziehl_neelsen_esputo.html',
                'bk_esputo_1.html',
                'bk_esputo_2.html',
                'bk_esputo_3.html',
                'koh_lesiones_piel.html',
                'microscopia_azul_metileno.html'
            ],
            'Inmunología': [
                '8. INMUNOLOGIA.html',
                '9. INFECCIOSAS.html',
                '11. MARCADORES TUMORALES.html'
            ],
            'Urianálisis': [
                '2. ORINA.html',
                'orina_completa.html'
            ],
            'Coprología': [
                '1. HECES.html',
                'heces_completa.html',
                'coprologia.html'
            ],
            'Especiales': [
                '7. PRUEBA DE EMBARAZO.html',
                '12. COAGULACION.html',
                '13. TIPO DE SANGRE.html',
                '18. ESPERMOGRAMA.html',
                '19. TARJETA DE SALUD.html',
                '20. DROGAS.html',
                'espermograma.html',
                'inmunologia_infecciosa.html',
                'hepatitis.html',
                'heces_completa.html',
                'orina_completa.html',
                'acido_valproico_1.html',
                'acido_valproico_fenitoina.html'
            ],
            'Paquetes': [
                '20. PAQUETE PRENATAL.html',
                '20. PAQUETE PRENATAL DRA. WENDY MADRID.html',
                '21. PAQUETE COVID-19.html',
                '24. PAQUETE DENGUE.html',
                'hematologia_wendy.html',
                'tipo_sangre_wendy.html',
                'bioquimica_wendy.html',
                'inmunologia_infecciosa_wendy.html',
                'hepatitis_wendy.html',
                'orina_completa_wendy.html',
                'hematologia_prenatal.html',
                'tipo_sangre_prenatal.html',
                'bioquimica_prenatal.html',
                'inmunologia_infecciosa_prenatal.html',
                'hepatitis_prenatal.html',
                'heces_completa_prenatal.html',
                'orina_completa_prenatal.html',
                'hematologia_covid.html',
                'bioquimica_covid.html',
                'inmunologia_covid.html',
                'proteinas_neoplasicas_covid.html',
                'coagulacion_covid.html',
                'enzimas_covid.html',
                'interleucina_covid.html',
                'hematologia_canino.html',
                'bioquimica_canino.html',
                'bioquimica_hepatica_canino.html',
                'hematologia_felino.html',
                'bioquimica_felino.html',
                'bioquimica_hepatica_felino.html',
                'bilirrubinas_felino.html',
                'hematologia_dengue.html',
                'inmunologia_dengue.html',
                'orina_completa_dengue.html'
            ]
        }
        
        return jsonify({
            'success': True,
            'data': categories
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener categorías: {str(e)}'
        }), 500

@lab_tests_bp.route('/search')
def search_lab_tests():
    """
    Buscar pruebas de laboratorio
    
    GET /api/lab-tests/search?q=<search_term>
    """
    try:
        search_term = request.args.get('q', '').strip()
        
        if not search_term:
            return jsonify({
                'success': False,
                'message': 'Término de búsqueda requerido'
            }), 400
        
        html_dir = Path("bocetos_pruebas/html_output")
        
        if not html_dir.exists():
            return jsonify({
                'success': False,
                'message': 'Directorio de pruebas no encontrado'
            }), 404
        
        # Buscar archivos que coincidan con el término
        matching_files = []
        for file_path in html_dir.glob("*.html"):
            if file_path.name != "index.html":
                filename_lower = file_path.name.lower()
                if search_term.lower() in filename_lower:
                    matching_files.append({
                        'filename': file_path.name,
                        'name': file_path.stem,
                        'url': f'/api/lab-tests/html/{file_path.name}'
                    })
        
        return jsonify({
            'success': True,
            'data': matching_files,
            'total': len(matching_files),
            'search_term': search_term
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error en búsqueda: {str(e)}'
        }), 500

