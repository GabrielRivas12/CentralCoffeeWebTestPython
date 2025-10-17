from .repository.IChatRepository import IChatRepository
from ..config.FirebaseConfig import db, query
import datetime
from ..config.CryptoHelper import EncryptionManager

crypto = EncryptionManager()

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

    def obtener_mensajes(self, id_chat):

        try: 
            doc_ref = db.collection('chats').document(id_chat).collection('mensajes')
            mensajes = doc_ref.stream()

            resultados = []

            for doc in mensajes:
                data = doc.to_dict()
                data['texto'] = crypto.decrypt_message(data['texto'])
                print(data['texto'])
                data['id'] = doc.id
                resultados.append(data)

            return resultados
        except Exception as e:
            print(f"Error al obtener subcolección: {e}")
            return []
        
        return super().obtener_mensajes(id_chat)

    def añadir_mensaje(self, id_chat):
        return super().añadir_mensaje(id_chat)