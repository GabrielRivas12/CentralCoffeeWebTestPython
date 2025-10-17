from abc import ABC, abstractmethod

class IChatRepository(ABC):

    @abstractmethod
    def crear_chat(self, id_emisor: str, id_receptor: str) -> str:
        pass

    @abstractmethod
    def añadir_mensaje(self, id_chat: str) -> None:
        pass

    @abstractmethod
    def borrar_chat(self, id_chat: str) -> None:
        pass

    @abstractmethod
    def obtener_chats_usuario(self, id_usuario: str) -> list:
        pass

    @abstractmethod
    def obtener_mensajes(self, id_chat: str) -> list:
        pass