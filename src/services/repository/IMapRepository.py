from abc import ABC, abstractmethod

class IMapRepository(ABC):
    
    @abstractmethod
    def getLocations(self):
        """Metodo para obtener todos los lugares a mostrar en el mapa"""
        pass