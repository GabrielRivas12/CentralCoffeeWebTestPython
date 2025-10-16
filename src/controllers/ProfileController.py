from flask import request, session, render_template, Blueprint, redirect, url_for, flash
from ..services.UserRepository import UserRepositoryImpl
from ..services.OffersRepositoryImpl import OffersRepositoryImpl
from ..services.OffersRepositoryImpl import OffersRepositoryImpl

profile_bp = Blueprint('profile', __name__)
userRepository = UserRepositoryImpl()
offersRepository = OffersRepositoryImpl()

@profile_bp.before_request
def load_user():
    if 'user_uid' in session:
        user_info = userRepository.get_user_by_uid(session['user_uid'])
        if user_info:
            session['user'] = user_info
    else:
        flash('Por favor inicia sesión para ver tu perfil.', 'error')
        return redirect(url_for('login.login'))

@profile_bp.route('/profile')
def profile():
    if 'user_uid' not in session:
        flash('Por favor inicia sesión para ver tu perfil.', 'error')
        return redirect(url_for('login.login'))
    user_info = userRepository.get_user_by_uid(session['user_uid'])
    productos = offersRepository.obtener_uno(session['user_uid'])
    return render_template('screens/profile/AdminProfile.html', user=user_info, productos=productos)

@profile_bp.route('/update-profile', methods=['POST'])
def update_profile():
    try:
        data = dict(request.form)

        if 'profilePhoto' in request.files and request.files['profilePhoto'].filename != "":
            profile = request.files.get('profilePhoto')
            data['fotoPerfil'] = offersRepository.guardar_imagen(bucket_name='file', file_obj=profile)
        if 'coverPhoto' in request.files and request.files['coverPhoto'].filename != "": 
            cover=request.files.get('coverPhoto')
            data['fotoPortada'] = offersRepository.guardar_imagen(bucket_name='file', file_obj=cover)
        data['uid'] = session.get('user_uid')
        data['nombre'] = userRepository.get_user_by_uid(data['uid']).get('nombre')
        data['email'] = session.get('correo')

        userRepository.update_user(uid=data['uid'], data=data)
        flash('Perfil actualizado exitosamente.', 'success')    
        return redirect(url_for('profile.profile'))
        
    except Exception as e:
        flash(f'Error actualizando el perfil: {str(e)}', 'error')
        return redirect(url_for('profile.profile'))
