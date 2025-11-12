from flask import Blueprint, flash, render_template, redirect, request, url_for, session
from dotenv import get_key
import requests
from ..services.AuthRepositoryImpl import AuthRepositoryImpl
from ..services.UserRepository import UserRepositoryImpl

repository = AuthRepositoryImpl()
userRepository = UserRepositoryImpl()

login_bp = Blueprint("login", __name__)

baseDir = 'screens/login/'

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