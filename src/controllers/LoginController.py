from flask import Blueprint, flash, render_template, redirect, request, url_for, session
from dotenv import get_key
import requests
from functools import wraps
from ..services.AuthRepositoryImpl import AuthRepositoryImpl
from ..services.UserRepository import UserRepositoryImpl

repository = AuthRepositoryImpl()
userRepository = UserRepositoryImpl()

login_bp = Blueprint("login", __name__)

baseDir = 'screens/login/'

# Decorador para verificación de roles
def roles_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session:
                flash('Debes iniciar sesión para acceder a esta página.', 'error')
                return redirect(url_for('login.login'))
            
            if session['user_role'] not in allowed_roles:
                flash('No tienes permisos para acceder a esta página.', 'error')
                return redirect(url_for('ofertas.listar_ofertas'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@login_bp.before_request
def load_user():
    if 'user_uid' in session:
        user_info = userRepository.get_user_by_uid(session['user_uid'])
        if user_info:
            # VERIFICAR SI EL ROL SIGUE SIENDO VÁLIDO
            user_role = user_info.get('rol', '')
            allowed_roles = ['Administrador', 'Comprador']
            
            if user_role not in allowed_roles:
                # SI EL ROL YA NO ES VÁLIDO, CERRAR SESIÓN
                session.clear()
                flash('Tu rol ya no tiene acceso al sistema.', 'error')
                return redirect(url_for('login.login'))
            
            session['user'] = user_info
            session['user_role'] = user_role

FIREBASE_API_KEY = get_key('.env', 'FIREBASE_API_KEY')

@login_bp.route('/', methods=['GET', 'POST'])
def login():
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
                }
            )

            data = response.json()
            if 'idToken' in data:
                decoded_token = repository.authenticate_user(data['idToken'])

                if decoded_token:
                    # OBTENER INFORMACIÓN DEL USUARIO DESDE FIRESTORE
                    user_data = userRepository.get_user_by_uid(decoded_token['uid']) 
                    
                    # VERIFICAR SI EL USUARIO EXISTE EN FIRESTORE
                    if not user_data:
                        flash('Usuario no encontrado en el sistema.', 'error')
                        return redirect(url_for('login.login'))
                    
                    user_role = user_data.get('rol', '')
                    
                    # SOLO PERMITIR ACCESO A ADMINISTRADOR Y COMPRADOR
                    allowed_roles = ['Administrador', 'Comprador']
                    if user_role not in allowed_roles:
                        flash('Acceso denegado. Tu rol no tiene permisos para acceder al sistema.', 'error')
                        return redirect(url_for('login.login'))
                    
                    # CREAR SESIÓN SI EL ROL ES VÁLIDO
                    session['user_uid'] = decoded_token['uid']
                    session['email'] = decoded_token['email']
                    session['user_token'] = data['idToken']
                    session['user_role'] = user_role
                    session['user_name'] = user_data.get('nombre', '')
                    
                    flash('¡Inicio de sesión exitoso!', 'success')
                    return redirect(url_for('ofertas.listar_ofertas'))
            
            flash('Credenciales inválidas. Por favor intenta nuevamente.', 'error')
            return redirect(url_for('login.login'))
            
        except Exception as e:
            flash(f'Error en el inicio de sesión: {str(e)}', 'error')
            return redirect(url_for('login.login'))
    
    return render_template(baseDir + 'login.html', full_screen=True)
    
@login_bp.route('/registro', methods=['GET','POST'])
def registro():
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
                # EL ROL SIEMPRE SERÁ "Comprador"
                userRepository.create_user(
                    uid=result['user']['uid'],
                    name=name,
                    email=email,
                    location='Managua, nicaragua',
                    rol='Comprador'  # Rol fijo
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