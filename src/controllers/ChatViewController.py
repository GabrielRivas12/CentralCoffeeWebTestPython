from flask import Blueprint, render_template, session, abort, request, jsonify
from ..services.ChatRepositotyImpl import ChatRepositoryImpl, obtener_participantes
from ..services.UserRepository import UserRepositoryImpl

chat_view_bp = Blueprint('chat_view', __name__)
repository = ChatRepositoryImpl()
user_repo = UserRepositoryImpl()

@chat_view_bp.route('/chat/<string:chat_id>')
def chat_view(chat_id):
    """
    Renderiza la vista de una conversación de chat específica.
    """
    user_id = session.get('user_uid')
    if not user_id:
        abort(401) # No autorizado

    # 1. Verificar que el usuario actual es participante del chat
    # `obtener_participantes` devuelve una lista (array de Firestore)
    participantes = obtener_participantes(chat_id)
    if not participantes or user_id not in participantes:
        abort(403) # Prohibido

    # 2. Obtener los mensajes del chat
    mensajes = repository.obtener_mensajes(chat_id)

    # 3. Identificar al otro usuario
    otro_usuario_id_list = [p for p in participantes if p != user_id]
    otro_usuario_id = otro_usuario_id_list[0] if otro_usuario_id_list else None
    
    otro_usuario_info = user_repo.get_user_by_uid(otro_usuario_id) if otro_usuario_id else {}

    return render_template(
        'screens/ChatView/ChatView.html',
        chat_id=chat_id,
        mensajes=mensajes,
        current_user_id=user_id,
        otro_usuario=otro_usuario_info
    )

@chat_view_bp.route('/api/chat/<string:chat_id>/messages', methods=['GET', 'POST'])
def api_messages(chat_id):
    """
    API para obtener y enviar mensajes.
    """
    user_id = session.get('user_uid')
    if not user_id:
        abort(401)

    # `obtener_participantes` devuelve una lista
    participantes = obtener_participantes(chat_id)
    if not participantes or user_id not in participantes:
        abort(403)

    if request.method == 'GET':
        mensajes = repository.obtener_mensajes(chat_id)
        return jsonify(mensajes)

    if request.method == 'POST':
        data = request.get_json()
        texto = data.get('texto')

        if not texto:
            return jsonify({'status': 'error', 'message': 'El texto no puede estar vacío'}), 400

        mensaje_id = repository.añadir_mensaje(chat_id, user_id, texto)

        if mensaje_id:
            return jsonify({'status': 'ok', 'message_id': mensaje_id})
        else:
            return jsonify({'status': 'error', 'message': 'No se pudo enviar el mensaje'}), 500