from flask import Blueprint, flash, render_template, redirect, url_for, request, session
from ..services.ChatRepositotyImpl import ChatRepositoryImpl

repository = ChatRepositoryImpl()

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/crearChat', methods=['POST'])
def crear_chat():
    id_emisor = session.get('user_uid')
    id_receptor = request.form.get('id_receptor')

    if not id_emisor or not id_receptor:
        flash('no puedes crear un chat sin dos ids', 'error')
        return redirect(url_for('ofertas.listar_ofertas'))

    id_chat = repository.crear_chat(id_emisor, id_receptor)
    return redirect(url_for('ofertas.listar_ofertas'))

@chat_bp.route('/obtenerChats')
def obtener_chats():
    id_chat = "o5VKHigAzRO1C1RQuNfDOzIiJLf1_w8Vi1am0s2bpHC5EKsIzOChfR2I3"

    repository.obtener_mensajes(id_chat)

    return redirect(url_for('ofertas.listar_ofertas'))