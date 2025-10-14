class Coordinates:
    def __init__(self, lat: float, lng: float):
        self.lat = lat
        self.lng = lng

    def to_dict(self):
        return {"lat": self.lat, "lng": self.lng}

class Location:
    # añadir type luego
    
    def __init__(self, name: str, coords: Coordinates, description: str, population: str):
        self.name = name
        self.coords = coords
        #self.type = type
        self.description = description
        self.population = population

    def to_dict(self):
        return {
            "name": self.name,
            "coords": self.coords.to_dict(),
            "description": self.description,
            "population": self.population,
        }

    @classmethod
    def from_dict(cls, dict: dict):
        return cls(
                name=dict.get('nombre'),
                coords=Coordinates(lat=dict.get('latitud'),lng=dict.get('longitud')),
                description=dict.get('descripcion'),
                population='100,000'
            )
