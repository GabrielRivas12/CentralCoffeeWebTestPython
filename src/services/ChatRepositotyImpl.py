from .repository.IChatRepository import IChatRepository
from ..config.FirebaseConfig import db
from google.cloud.firestore_v1 import FieldFilter, Or
import datetime
from ..config.CryptoHelper import EncryptionManager
from ..services.UserRepository import UserRepositoryImpl

crypto = EncryptionManager()
user_repo = UserRepositoryImpl()

def obtener_participantes(id_chat: str):
    """Obtiene los participantes de un chat"""
    try:
        doc = db.collection('chats').document(id_chat).get()
        if doc.exists:
            data = doc.to_dict()
            # Retorna el diccionario de participantes
            return data.get('participantes', {}) if 'participantes' in data else data
        return {}
    except Exception as e:
        print(f"Error obteniendo participantes: {e}")
        return {}

class ChatRepositoryImpl(IChatRepository):

    def crear_chat(self, id_emisor, id_receptor):
        doc_ref = db.collection('chats')
        
        # Estructura corregida: guardar participantes como un array
        datos = {
            'participantes': [id_emisor, id_receptor],
            'creadoEn': datetime.datetime.now(datetime.timezone.utc),
            'ultimoMensaje': None,
            'ultimaActualizacion': datetime.datetime.now(datetime.timezone.utc)
        }

        doc = doc_ref.add(datos)
        id_chat = doc[1].id
        print(f"Chat creado con ID: {id_chat}")
        return id_chat

    def borrar_chat(self, id_chat):
        try:
            # Primero borrar mensajes de la subcolección
            mensajes_ref = db.collection('chats').document(id_chat).collection('mensajes')
            mensajes = mensajes_ref.stream()
            
            for mensaje in mensajes:
                mensaje.reference.delete()
            
            # Luego borrar el chat
            db.collection('chats').document(id_chat).delete()
            return True
        except Exception as e:
            print(f"Error borrando chat: {e}")
            return False

    def obtener_chats_usuario(self, id_usuario):
        try:
            # Consulta para encontrar chats donde el usuario es participante usando 'array-contains'
            query = db.collection('chats').where(
                filter=FieldFilter("participantes", "array_contains", id_usuario)
            )
            
            chats_stream = query.stream()
            chats_encontrados = []

            for chat in chats_stream:
                chat_data = chat.to_dict()

                print(chat_data)
                
                participantes = chat_data.get('participantes', [])
                
                # Identificar al otro usuario en el array
                otro_usuario_id_list = [p for p in participantes if p != id_usuario]
                
                if not otro_usuario_id_list:
                    continue # No se encontró otro usuario, pasar al siguiente chat

                otro_usuario_id = otro_usuario_id_list[0]

                # Obtener información del otro usuario y el último mensaje
                info_otro_usuario = self._obtener_info_usuario(otro_usuario_id)
                ultimo_mensaje_data = self._obtener_ultimo_mensaje(chat.id)
                
                # Formatear los datos para la respuesta
                ultimo_mensaje_texto = ultimo_mensaje_data.get('texto', 'No hay mensajes') if ultimo_mensaje_data else 'No hay mensajes'
                timestamp = ultimo_mensaje_data.get('timestamp', chat_data.get('ultimaActualizacion')) if ultimo_mensaje_data else chat_data.get('ultimaActualizacion')
                
                fecha_formateada = self._formatear_fecha(timestamp)

                chats_encontrados.append({
                    'chat_id': chat.id,
                    'otro_usuario': {
                        'id': otro_usuario_id,
                        'nombre': info_otro_usuario.get('nombre', 'Usuario'),
                        'foto_perfil': info_otro_usuario.get('fotoPerfil', 'default_avatar.png')
                    },
                    'ultimo_mensaje': ultimo_mensaje_texto,
                    'fecha_ultimo_mensaje': fecha_formateada,
                    'timestamp': timestamp # Para ordenación
                })

            # Ordenar chats por el timestamp del último mensaje/actualización
            chats_encontrados.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return chats_encontrados

        except Exception as e:
            print(f"Error al obtener chats de usuario {id_usuario}: {e}")
            return []
    
    def _obtener_info_usuario(self, usuario_id):
        """Obtiene información de un usuario"""
        try:
            if hasattr(user_repo, 'get_user_by_uid'):
                return user_repo.get_user_by_uid(usuario_id) or {}
            elif hasattr(user_repo, 'obtener_usuario_por_id'):
                return user_repo.obtener_usuario_por_id(usuario_id) or {}
            else:
                # Fallback: obtener directamente de Firestore
                doc = db.collection('usuarios').document(usuario_id).get()
                return doc.to_dict() if doc.exists else {}
        except Exception as e:
            print(f"Error obteniendo info usuario {usuario_id}: {e}")
            return {'nombre': 'Usuario'}

    def _obtener_ultimo_mensaje(self, chat_id):
        """Obtiene el último mensaje de un chat"""
        try:
            mensajes_ref = db.collection('chats').document(chat_id).collection('mensajes')
            mensajes = mensajes_ref.order_by('timestamp', direction='DESCENDING').limit(1).stream()
            
            for mensaje in mensajes:
                data = mensaje.to_dict()
                # Intentar desencriptar si está encriptado
                if data.get('encriptado'):
                    try:
                        data['texto'] = crypto.decrypt_message(data['texto'])
                    except:
                        data['texto'] = '[Mensaje encriptado]'
                return data
            return None
        except Exception as e:
            print(f"Error obteniendo último mensaje: {e}")
            return None

    def _formatear_fecha(self, timestamp):
        """Formatea la fecha para mostrar"""
        if not timestamp:
            return ''
        
        ahora = datetime.datetime.now()
        
        # Convertir a datetime si es necesario
        if isinstance(timestamp, str):
            try:
                if 'T' in timestamp:
                    timestamp = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            except:
                return ''
        
        if timestamp.date() == ahora.date():
            return timestamp.strftime('%H:%M')
        elif timestamp.year == ahora.year:
            return timestamp.strftime('%d/%m')
        else:
            return timestamp.strftime('%d/%m/%Y')

    def obtener_mensajes(self, id_chat):
        try: 
            doc_ref = db.collection('chats').document(id_chat).collection('mensajes')
            mensajes = doc_ref.order_by('timestamp').stream()

            resultados = []

            for doc in mensajes:
                data = doc.to_dict()
                
                # Desencriptar si es necesario
                if data.get('encriptado'):
                    try:
                        data['texto'] = crypto.decrypt_message(data['texto'])
                        print(data['texto'])
                    except Exception as crypto_error:
                        print(f"Error desencriptando mensaje {doc.id}: {crypto_error}")
                        data['texto'] = '[Error desencriptación]'
                
                data['id'] = doc.id
                resultados.append(data)

            return resultados
        except Exception as e:
            print(f"Error al obtener mensajes: {e}")
            return []

    def añadir_mensaje(self, id_chat, id_emisor, texto, tipo="texto", encriptar=True):
        try:
            chat_ref = db.collection('chats').document(id_chat)
            chat_doc = chat_ref.get()
            
            if not chat_doc.exists:
                print(f"El chat {id_chat} no existe")
                return None
            
            # Encriptar el mensaje si es necesario
            texto_guardar = crypto.encrypt_message(texto) if encriptar else texto
            
            mensaje_data = {
                'de': id_emisor, # Corregido de 'emisor' a 'de'
                'texto': texto_guardar,
                'tipo': tipo,
                'timestamp': datetime.datetime.now(datetime.timezone.utc),
                'encriptado': encriptar
            }
            
            # Agregar mensaje
            mensaje_ref = chat_ref.collection('mensajes').add(mensaje_data)
            mensaje_id = mensaje_ref[1].id
            
            # Actualizar chat principal
            texto_visual = texto[:50] + "..." if len(texto) > 50 else texto
            chat_ref.update({
                'ultimoMensaje': texto_visual,
                'ultimaActualizacion': datetime.datetime.now()
            })
            
            print(f"Mensaje agregado al chat {id_chat}")
            return mensaje_id
            
        except Exception as e:
            print(f"Error añadiendo mensaje: {e}")
            return None

    def obtener_chat_entre_usuarios(self, id_usuario1, id_usuario2):
        """Encuentra un chat existente entre dos usuarios"""
        try:
            chat_ref = db.collection('chats')
            
            from google.cloud.firestore_v1 import And
            
            # Esta consulta requiere un índice compuesto en Firestore.
            # Si no existe, Firestore devolverá un error con un enlace para crearlo.
            query = chat_ref.where(filter=And([
                FieldFilter('participantes', 'array_contains', id_usuario1),
                FieldFilter('participantes', 'array_contains', id_usuario2)
            ]))
            
            chats = query.stream()
            
            for chat in chats:
                # Devuelve el primer chat que coincida
                return chat.id
            
            return None
            
        except Exception as e:
            print(f"Error buscando chat entre usuarios: {e}")
            return None