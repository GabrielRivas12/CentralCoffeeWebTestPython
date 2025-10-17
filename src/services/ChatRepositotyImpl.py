from .repository.IChatRepository import IChatRepository
from ..config.FirebaseConfig import db, query
import datetime

class ChatRepositoryImpl(IChatRepository):
    
    def crear_chat(self, id_emisor, id_receptor):

        doc_ref = db.collection('chats')

        datos ={
                '0': id_emisor,
                '1': id_receptor,
                'creadoEn': datetime.datetime.now()
                }

        doc = doc_ref.add(datos)

        id_chat = doc[1].id

        print(id_chat)

        return id_chat

    def borrar_chat(self, id_chat):
        return super().borrar_chat(id_chat)

    def obtener_chats_usuario(self, id_usuario):
        doc_ref = db.collection('chats')

        chats = doc_ref.where(filter=query.Or([
            query.FieldFilter('0', '==', id_usuario),
            query.FieldFilter('1', '==', id_usuario)
        ])).stream()

        return [chat.id for chat in chats]

    def añadir_mensaje(self, id_chat):
        return super().añadir_mensaje(id_chat)