import datetime
from flask import Blueprint, flash, render_template, redirect, url_for, request, session
from ..services.ChatRepositotyImpl import ChatRepositoryImpl

repository = ChatRepositoryImpl()

def formatear_fecha(timestamp):
    """
    Formatea la fecha para mostrarla en el chat
    """
    if not timestamp:
        return ''
    
    ahora = datetime.datetime.now()
    
    # Convertir a datetime si es string
    if isinstance(timestamp, str):
        try:
            # Manejar diferentes formatos de fecha
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
    id_usuario = session.get('user_uid')
    
    if not id_usuario:
        flash('Debes iniciar sesión para ver tus chats', 'error')
        return redirect(url_for('auth.login'))

    chats = []
    try:
        # El repositorio ya nos da los chats procesados, con la información del otro usuario y el último mensaje.
        chats = repository.obtener_chats_usuario(id_usuario)
    
    except Exception as e:
        print(f"Error al obtener y procesar los chats: {e}")
        flash('Error al cargar los chats', 'error')

    return render_template('screens/Bandeja_entrada/Bandeja_entrada.html', chats=chats)

