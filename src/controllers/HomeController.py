import json
from dotenv import get_key
from flask import Blueprint, render_template, request, session, jsonify
from ..services.MapRepositoryImpl import MapRepositoryImpl

mapRepository = MapRepositoryImpl()

home_bp = Blueprint('home', __name__)

@home_bp.route('/mapa')
def mapa():
    api_key = get_key(".env", "MAPS_API_KEY")
    data = mapRepository.getLocations()
    
    user_role = session.get('user_role', 'Comprador')  # Por defecto Comprador
    
    # DEBUG
    print(f"DEBUG - Rol en sesión: {user_role}")
    print(f"DEBUG - Sesión completa: {dict(session)}")
    
    data_json = json.dumps(data)
    return render_template('screens/Mapa/mapa.html', 
                         locations=data_json, 
                         google_maps_api_key=api_key,
                         user_role=user_role)

@home_bp.route('/bandeja_entrada')
def bandeja_entrada():
    return render_template('screens/Bandeja_entrada/Bandeja_entrada.html')

@home_bp.route('/api/marcadores', methods=['POST'])
def crear_marcador():
    if session.get('user_role') != 'Administrador':
        return jsonify({'success': False, 'error': 'No autorizado'}), 403
    
    try:
        data = request.get_json()
        marcador_data = {
            'nombre': data.get('nombre'),
            'descripcion': data.get('descripcion'),
            'horario': data.get('horario'),
            'latitud': data.get('latitud'),
            'longitud': data.get('longitud'),
            'userId': session.get('user_uid', 'admin')
        }
        
        success = mapRepository.createLocation(marcador_data)
        if success:
            return jsonify({'success': True, 'message': 'Marcador creado correctamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al crear marcador'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@home_bp.route('/api/marcadores/<doc_id>', methods=['PUT'])
def actualizar_marcador(doc_id):
    if session.get('user_role') != 'Administrador':
        return jsonify({'success': False, 'error': 'No autorizado'}), 403
    
    try:
        data = request.get_json()
        update_data = {
            'nombre': data.get('nombre'),
            'descripcion': data.get('descripcion'),
            'horario': data.get('horario')
        }
        
        success = mapRepository.updateLocation(doc_id, update_data)
        if success:
            return jsonify({'success': True, 'message': 'Marcador actualizado correctamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al actualizar marcador'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@home_bp.route('/api/marcadores/<doc_id>', methods=['DELETE'])
def eliminar_marcador(doc_id):
    if session.get('user_role') != 'Administrador':
        return jsonify({'success': False, 'error': 'No autorizado'}), 403
    
    try:
        success = mapRepository.deleteLocation(doc_id)
        if success:
            return jsonify({'success': True, 'message': 'Marcador eliminado correctamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al eliminar marcador'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500