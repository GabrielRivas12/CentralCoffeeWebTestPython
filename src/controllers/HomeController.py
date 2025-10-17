import json
from dotenv import get_key
from flask import Blueprint, render_template
from ..services.MapRepositoryImpl import MapRepositoryImpl

mapRepository = MapRepositoryImpl()

home_bp = Blueprint('home', __name__)


@home_bp.route('/mapa')
def mapa():
    api_key = get_key(".env","MAPS_API_KEY")
    data = mapRepository.getLocations()

    location_dict = [map.to_dict() for map in data]
    data_json = json.dumps(location_dict)
    return render_template('screens/Mapa/mapa.html', locations=data_json, google_maps_api_key=api_key)

# ---------------- Mapa ----------------

@home_bp.route('/rci')
def rci():
    return render_template('screens/RCI/rci.html')

@home_bp.route('/bandeja_entrada')
def bandeja_entrada():
    return render_template('screens/Bandeja_entrada/Bandeja_entrada.html')
