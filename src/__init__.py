from flask import Flask, session, redirect, url_for, flash, request
import os
def create_app():
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')

    app.secret_key = os.environ.get('SECRET_KEY')

    from .controllers.OffersController import ofertas_bp
    from .controllers.AssistantController import assistant_bp
    from .controllers.LoginController import login_bp
    from .controllers.HomeController import home_bp
    from .controllers.ProfileController import profile_bp
    from .controllers.ChatController import chat_bp
    from .controllers.ChatViewController import chat_view_bp

    app.register_blueprint(ofertas_bp)
    app.register_blueprint(assistant_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(chat_view_bp)

    @app.before_request
    def check_authentication():

        if request.path == '/rci':
            return
        
        public_routes = [
            'login.login', 
            'login.registro', 
            'login.logout',
            'static',
            'home.home',
            'assistant.rci'
        ]
        
        if request.endpoint in public_routes:
            return
            
        if 'user_uid' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'error')
            return redirect(url_for('login.login'))
            
        allowed_roles = ['Administrador', 'Comprador']
        if session.get('user_role') not in allowed_roles:
            session.clear()
            flash('Tu rol ya no tiene acceso al sistema.', 'error')
            return redirect(url_for('login.login'))

    return app