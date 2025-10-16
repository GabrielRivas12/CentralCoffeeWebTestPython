from abc import ABC, abstractmethod

class IUserRepository(ABC):
    
    @abstractmethod
    def create_user(self, uid: str, name: str, email: str, location: str, rol: str) -> None:
        pass

    @abstractmethod
    def get_user_by_uid(self, uid: str):
        pass

    @abstractmethod
    def update_user(self, uid: str, data: dict) -> None:
        pass