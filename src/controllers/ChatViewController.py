from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for, flash
from ..services.ChatRepositotyImpl import ChatRepositoryImpl, obtener_participantes
from ..services.UserRepository import UserRepositoryImpl

chat_view_bp = Blueprint('chat_view', __name__)
repository = ChatRepositoryImpl()
user_repo = UserRepositoryImpl()

@chat_view_bp.route('/chat/<string:chat_id>')
def chat_view(chat_id):
    user_id = session.get('user_uid')

    participantes = obtener_participantes(chat_id)
    if not participantes or user_id not in participantes:
        flash('No tienes permisos para acceder a este chat', 'error')
        return redirect(url_for('chat.obtener_chats'))

    mensajes = repository.obtener_mensajes(chat_id)

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
    user_id = session.get('user_uid')
    if not user_id:
        return jsonify({'status': 'error', 'message': 'No autorizado'}), 401

    participantes = obtener_participantes(chat_id)
    if not participantes or user_id not in participantes:
        return jsonify({'status': 'error', 'message': 'No tienes permisos para acceder a este chat'}), 403

    if request.method == 'GET':
        try:
            mensajes = repository.obtener_mensajes(chat_id)
            return jsonify(mensajes)
        except Exception:
            return jsonify({'status': 'error', 'message': 'Error al obtener mensajes'}), 500

    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'status': 'error', 'message': 'Datos no proporcionados'}), 400
                
            texto = data.get('texto')

            if not texto or texto.strip() == '':
                return jsonify({'status': 'error', 'message': 'El texto no puede estar vacío'}), 400

            mensaje_id = repository.añadir_mensaje(chat_id, user_id, texto.strip())

            if mensaje_id:
                return jsonify({'status': 'ok', 'message_id': mensaje_id})
            else:
                return jsonify({'status': 'error', 'message': 'No se pudo enviar el mensaje'}), 500
                
        except Exception:
            return jsonify({'status': 'error', 'message': 'Error al enviar mensaje'}), 500