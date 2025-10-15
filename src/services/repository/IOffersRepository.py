from abc import ABC, abstractmethod

class IOffersRepository(ABC):

    @abstractmethod
    def crear(self, data: dict):
        """Crea un nuevo registro."""
        pass

    @abstractmethod
    def obtener_uno(self, id: str):
        """Obtiene un registro por su ID."""
        pass

    @abstractmethod
    def obtener_todos(self):
        """Obtiene todos los registros."""
        pass

    @abstractmethod
    def actualizar(self, id: str, data: dict):
        """Actualiza un registro existente."""
        pass

    @abstractmethod
    def eliminar(self, id: str):
        """Elimina un registro por su ID."""
        pass

    @abstractmethod
    def guardar_imagen(self, bucket_name: str, file_obj, file_key: str = None) -> str:
        """Guarda un archivo de imagen y retorna su URL o identificador."""
        pass

    