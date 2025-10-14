from .repository.IMapRepository import IMapRepository
from ..models.location_model import Location
from ..config.FirebaseConfig import db

class MapRepositoryImpl(IMapRepository):
    
    def getLocations(self):
        try:
            data = db.collection('lugares').get()
            return [Location.from_dict(map) for map in data]
            
        except Exception as e:
            print("Error al obtener todos los lugares: " + e)
        return []
