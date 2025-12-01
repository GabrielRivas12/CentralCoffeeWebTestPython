from flask import Blueprint, flash, render_template, redirect, request, url_for, session, jsonify
from dotenv import get_key
import requests
from functools import wraps
import time
import logging
import json  # Añade esta importación
from ..services.AuthRepositoryImpl import AuthRepositoryImpl
from ..services.UserRepository import UserRepositoryImpl

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

repository = AuthRepositoryImpl()
userRepository = UserRepositoryImpl()


login_bp = Blueprint("login", __name__, url_prefix='/login')

baseDir = 'screens/login/'

FIREBASE_API_KEY = get_key('.env', 'API_KEY')

if not FIREBASE_API_KEY:
    logger.error("❌ CRÍTICO: NO SE ENCONTRÓ API_KEY EN .env")
    logger.error("Revisa que tu archivo .env tenga: API_KEY = 'tu_api_key_aqui'")
    # Si sigue fallando, usa la API key directamente
    FIREBASE_API_KEY = "AIzaSyCJhLkIM4YqrI1tT9neYLSofwe9katbWWo"
    logger.info(f"✅ API_KEY establecida manualmente: {FIREBASE_API_KEY[:10]}...")
else:
    logger.info(f"✅ API_KEY cargada correctamente desde .env: {FIREBASE_API_KEY[:10]}...")
# Diccionario para almacenar tiempos de última solicitud por email (en memoria)
reset_attempts = {}

# Decorador para verificar autenticación
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_token' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'error')
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para verificar roles
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_token' not in session:
                flash('Debes iniciar sesión para acceder a esta página.', 'error')
                return redirect(url_for('login.login'))
            
            user_role = session.get('user_role')
            if user_role not in allowed_roles:
                flash('No tienes permisos para acceder a esta página.', 'error')
                return redirect(url_for('ofertas.listar_ofertas'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def clean_old_attempts():
    """Limpiar intentos de recuperación con más de 1 hora"""
    current_time = time.time()
    one_hour_ago = current_time - 3600
    
    # Crear lista de emails a eliminar
    to_delete = []
    for email, attempt_time in reset_attempts.items():
        if attempt_time < one_hour_ago:
            to_delete.append(email)
    
    # Eliminar entradas antiguas
    for email in to_delete:
        del reset_attempts[email]

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    # Si ya está autenticado, redirigir a ofertas
    if 'user_token' in session:
        flash('Ya tienes una sesión activa.', 'info')
        return redirect(url_for('ofertas.listar_ofertas'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Error en el inicio de sesión: Rellene el formulario de login', 'error')
            return redirect(url_for('login.login'))

        try:
            response = requests.post(
                f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}',
                json={
                    'email': email,
                    'password': password,
                    'returnSecureToken': True
                },
                timeout=30
            )

            data = response.json()
            if 'idToken' in data:
                decoded_token = repository.authenticate_user(data['idToken'])

                if decoded_token:
                    user_data = userRepository.get_user_by_uid(decoded_token['uid']) 
                    
                    if not user_data:
                        flash('Usuario no encontrado en el sistema.', 'error')
                        return redirect(url_for('login.login'))
                    
                    user_role = user_data.get('rol', '')
                    
                    allowed_roles = ['Administrador', 'Comprador']
                    if user_role not in allowed_roles:
                        flash('Acceso denegado. Tu rol no tiene permisos para acceder al sistema.', 'error')
                        return redirect(url_for('login.login'))
                    
                    session['user_uid'] = decoded_token['uid']
                    session['email'] = decoded_token['email']
                    session['user_token'] = data['idToken']
                    session['user_role'] = user_role
                    session['user_name'] = user_data.get('nombre', '')
                    
                    # Hacer la sesión permanente
                    session.permanent = True
                    
                    flash('¡Inicio de sesión exitoso!', 'success')
                    return redirect(url_for('ofertas.listar_ofertas'))
            
            flash('Credenciales inválidas. Por favor intenta nuevamente.', 'error')
            return redirect(url_for('login.login'))
            
        except Exception as e:
            logger.error(f"Error en login: {str(e)}")
            flash(f'Error en el inicio de sesión: {str(e)}', 'error')
            return redirect(url_for('login.login'))
    
    return render_template(baseDir + 'login.html', full_screen=True)

@login_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Endpoint para enviar correo de recuperación de contraseña"""
    logger.info("=== INICIO reset_password ===")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request headers: {dict(request.headers)}")
    logger.info(f"Request content type: {request.content_type}")
    logger.info(f"Request is_json: {request.is_json}")
    
    try:
        # Verificar si es JSON
        if not request.is_json:
            logger.error("❌ Request no es JSON")
            logger.error(f"Content-Type recibido: {request.content_type}")
            logger.error(f"Datos recibidos: {request.data}")
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400
        
        data = request.get_json()
        logger.info(f"Datos JSON recibidos: {data}")
        email = data.get('email')
        # ... el resto del código igual ...
        
        # Verificar si ya se envió un correo recientemente (15 segundos)
        current_time = time.time()
        if email in reset_attempts:
            last_attempt = reset_attempts[email]
            time_since_last_attempt = current_time - last_attempt
            
            if time_since_last_attempt < 15:  # 15 segundos de espera
                wait_time = 15 - int(time_since_last_attempt)
                logger.warning(f"Intento demasiado pronto para {email}, esperar {wait_time}s")
                return jsonify({
                    'success': False,
                    'error': f'Debes esperar {wait_time} segundos antes de enviar otro correo.'
                }), 429
        
        # Verificar que la API KEY esté configurada
        if not FIREBASE_API_KEY:
            logger.error("FIREBASE_API_KEY no configurada")
            return jsonify({
                'success': False,
                'error': 'Error de configuración del servidor: FIREBASE_API_KEY no encontrada.'
            }), 500
        
        logger.info(f"FIREBASE_API_KEY: {FIREBASE_API_KEY[:10]}...")
        logger.info(f"Enviando solicitud a Firebase para {email}")
        
        # URL de Firebase para reset de contraseña
        firebase_url = f'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_API_KEY}'
        logger.info(f"URL Firebase: {firebase_url}")
        
        payload = {
            'requestType': 'PASSWORD_RESET',
            'email': email
        }
        
        logger.info(f"Payload: {payload}")
        
        response = requests.post(
            firebase_url,
            json=payload,
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        logger.info(f"Respuesta de Firebase - Status: {response.status_code}")
        logger.info(f"Respuesta de Firebase - Text: {response.text}")
        
        try:
            firebase_data = response.json()
        except json.JSONDecodeError:
            logger.error(f"Firebase devolvió respuesta no JSON: {response.text[:200]}")
            return jsonify({
                'success': False,
                'error': 'Respuesta inválida del servicio de autenticación.'
            }), 500
        
        if response.status_code == 200:
            # Registrar el tiempo de esta solicitud
            reset_attempts[email] = current_time
            
            # Limpiar entradas antiguas (más de 1 hora)
            clean_old_attempts()
            
            logger.info(f"Correo de recuperación enviado exitosamente a {email}")
            return jsonify({
                'success': True,
                'message': 'Se ha enviado un correo con las instrucciones para restablecer tu contraseña.'
            })
        else:
            error_message = firebase_data.get('error', {}).get('message', 'Error desconocido de Firebase')
            logger.error(f"Error de Firebase: {error_message}")
            logger.error(f"Respuesta completa: {firebase_data}")
            
            if 'EMAIL_NOT_FOUND' in error_message:
                user_message = 'No existe una cuenta con este correo electrónico.'
            elif 'TOO_MANY_ATTEMPTS_TRY_LATER' in error_message:
                user_message = 'Demasiados intentos. Por favor intenta más tarde.'
            elif 'INVALID_EMAIL' in error_message:
                user_message = 'El correo electrónico no es válido.'
            elif 'USER_DISABLED' in error_message:
                user_message = 'Esta cuenta ha sido deshabilitada.'
            elif 'MISSING_EMAIL' in error_message:
                user_message = 'El correo electrónico es requerido.'
            else:
                user_message = f'Error: {error_message}'
            
            return jsonify({
                'success': False,
                'error': user_message
            }), response.status_code
            
    except requests.exceptions.Timeout:
        logger.error("Timeout al conectar con Firebase")
        return jsonify({
            'success': False,
            'error': 'Tiempo de espera agotado. Por favor intenta nuevamente.'
        }), 504
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Error de conexión con Firebase: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error de conexión con el servicio de autenticación. Verifica tu conexión a internet.'
        }), 503
    except Exception as e:
        logger.error(f"Error en reset_password: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor. Por favor intenta más tarde.'
        }), 500
    finally:
        logger.info("=== FIN reset_password ===")

@login_bp.route('/test-connection', methods=['GET'])
def test_connection():
    """Endpoint de prueba para verificar que el servidor responde"""
    logger.info("Test connection endpoint called")
    return jsonify({
        'success': True,
        'message': 'Servidor funcionando correctamente',
        'timestamp': time.time()
    })


@login_bp.route('/registro', methods=['GET','POST'])
def registro():
    # Si ya está autenticado, redirigir a ofertas
    if 'user_token' in session:
        flash('Ya tienes una sesión activa.', 'info')
        return redirect(url_for('ofertas.listar_ofertas'))
    
    if request.method == 'GET':
        return render_template(baseDir + 'registro.html', full_screen=True)
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        confirmar = request.form.get('confirmar')
        name = request.form.get('name')

        if password != confirmar:
            flash("Las contraseñas no coinciden", 'error')
            return redirect(url_for('login.registro'))

        try:
            result = repository.create_user(email, password)

            if result['success']:
                userRepository.create_user(
                    uid=result['user']['uid'],
                    name=name,
                    email=email,
                    location='Managua, nicaragua',
                    rol='Comprador'
                )
            
                flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
                return redirect(url_for('login.login'))
            else:
                flash(f"Error en el registro: {result.get('error', 'Error desconocido')}", 'error')
                return redirect(url_for('login.registro'))
                
        except Exception as e:
            flash(f"Error al registrar usuario: {str(e)}", 'error')
            return redirect(url_for('login.registro'))

@login_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('login.login'))

@login_bp.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado'
    }), 404

@login_bp.errorhandler(500)
def internal_error(error):
    logger.error(f"Error interno del servidor: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500