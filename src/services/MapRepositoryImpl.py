from .repository.IMapRepository import IMapRepository
from ..config.FirebaseConfig import db

class MapRepositoryImpl(IMapRepository):
    
    def getLocations(self):
        try:
            data = db.collection('lugares').get()
            locations = []
            for doc in data:
                location_data = doc.to_dict()
                location = {
                    'nombre': location_data.get('nombre', 'Sin nombre'),
                    'descripcion': location_data.get('descripcion', 'Sin descripción'),
                    'horario': location_data.get('horario', 'Horario no disponible'),
                    'latitud': location_data.get('latitud', 0),
                    'longitud': location_data.get('longitud', 0),
                    'userId': location_data.get('userId', ''),
                    'doc_id': doc.id 
                }
                locations.append(location)
            
            print(f"Se obtuvieron {len(locations)} ubicaciones de Firebase")
            return locations
            
        except Exception as e:
            print(f"Error al obtener todos los lugares: {e}")
            return []
    
    def updateLocation(self, doc_id, update_data):
        try:
            doc_ref = db.collection('lugares').document(doc_id)
            doc_ref.update(update_data)
            print(f"Marcador {doc_id} actualizado correctamente")
            return True
        except Exception as e:
            print(f"Error al actualizar ubicación: {e}")
            return False
    
    def deleteLocation(self, doc_id):
        try:
            db.collection('lugares').document(doc_id).delete()
            print(f"Marcador {doc_id} eliminado correctamente")
            return True
        except Exception as e:
            print(f"Error al eliminar ubicación: {e}")
            return False
    
    def createLocation(self, location_data):
        try:
            doc_ref = db.collection('lugares').document()
            location_data['doc_id'] = doc_ref.id 
            doc_ref.set(location_data)
            print(f"Nuevo marcador creado con ID: {doc_ref.id}")
            return True
        except Exception as e:
            print(f"Error al crear ubicación: {e}")
            return False