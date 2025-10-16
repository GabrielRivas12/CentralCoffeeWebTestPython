from abc import ABC, abstractmethod

class IUserRepository(ABC):
    
    @abstractmethod
    def create_user(self, uid: str, name: str, email: str, location: str, rol: str) -> None:
        pass