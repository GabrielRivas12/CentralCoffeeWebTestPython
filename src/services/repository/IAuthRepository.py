from abc import ABC, abstractmethod
from typing import Dict, Optional

class IAuthRepository(ABC):
    
    @abstractmethod
    def create_user(self, email: str, password: str) -> dict:
        """ Metodo para crear un usuario con Firebase Auth """
        pass
    
    @abstractmethod
    def authenticate_user(self, id_token: str) -> dict:
        """ Metodo para autenticar un usuario con Firebase Auth """
        
        pass
    
    @abstractmethod
    def get_user(self, uid: str) -> dict:
        """ Metodo para obtener un usuario por su UID """
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """ Metodo para obtener un usuario por su correo electronico """
        pass
    
    @abstractmethod
    def delete_user(self, uid: str) -> dict:
        """ Metodo para eliminar un usuario por su UID al quererse eliminar su cuenta """
        pass