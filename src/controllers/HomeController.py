import json
from dotenv import get_key
from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, flash
from functools import wraps
from ..services.MapRepositoryImpl import MapRepositoryImpl

mapRepository = MapRepositoryImpl()

home_bp = Blueprint('home', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'Administrador':
            flash('No tienes permisos para acceder a esta página.', 'error')
            return redirect(url_for('home.mapa'))
        return f(*args, **kwargs)
    return decorated_function

@home_bp.route('/mapa')
def mapa():
    api_key = get_key(".env", "MAPS_API_KEY")
    data = mapRepository.getLocations()
    
    user_role = session.get('user_role', 'Comprador')
    
    print(f"DEBUG - Rol en sesión: {user_role}")
    print(f"DEBUG - Sesión completa: {dict(session)}")
    
    data_json = json.dumps(data)
    return render_template('screens/Mapa/Mapa.html', 
                         locations=data_json, 
                         google_maps_api_key=api_key,
                         user_role=user_role)

@home_bp.route('/bandeja_entrada')
def bandeja_entrada():
    return render_template('screens/Bandeja_entrada/Bandeja_entrada.html')

@home_bp.route('/api/marcadores', methods=['POST'])
@admin_required
def crear_marcador():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Datos no proporcionados'}), 400
            
        marcador_data = {
            'nombre': data.get('nombre'),
            'descripcion': data.get('descripcion'),
            'horario': data.get('horario'),
            'latitud': data.get('latitud'),
            'longitud': data.get('longitud'),
            'userId': session.get('user_uid', 'admin')
        }
        
        required_fields = ['nombre', 'latitud', 'longitud']
        for field in required_fields:
            if not marcador_data.get(field):
                return jsonify({'success': False, 'error': f'Campo {field} es requerido'}), 400
        
        success = mapRepository.createLocation(marcador_data)
        if success:
            return jsonify({'success': True, 'message': 'Marcador creado correctamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al crear marcador'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@home_bp.route('/api/marcadores/<doc_id>', methods=['PUT'])
@admin_required
def actualizar_marcador(doc_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Datos no proporcionados'}), 400
            
        update_data = {
            'nombre': data.get('nombre'),
            'descripcion': data.get('descripcion'),
            'horario': data.get('horario')
        }
        
        if not any(update_data.values()):
            return jsonify({'success': False, 'error': 'Al menos un campo debe ser proporcionado'}), 400
        
        success = mapRepository.updateLocation(doc_id, update_data)
        if success:
            return jsonify({'success': True, 'message': 'Marcador actualizado correctamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al actualizar marcador'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@home_bp.route('/api/marcadores/<doc_id>', methods=['DELETE'])
@admin_required
def eliminar_marcador(doc_id):
    try:
        success = mapRepository.deleteLocation(doc_id)
        if success:
            return jsonify({'success': True, 'message': 'Marcador eliminado correctamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al eliminar marcador'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500