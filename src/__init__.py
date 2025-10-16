from flask import Flask
from dotenv import get_key

def create_app():
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')

    app.secret_key = get_key('.env', 'SECRET_KEY')

    # importación de controladores
    from .controllers.OffersController import ofertas_bp
    from .controllers.AssistantController import assistant_bp
    from .controllers.LoginController import login_bp
    from .controllers.HomeController import home_bp

    # registro de controladores
    app.register_blueprint(ofertas_bp)
    app.register_blueprint(assistant_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(home_bp)

    # --- Configuración adicional (si es necesaria) ---
    # Por ejemplo, cargar configuración desde un archivo o variables de entorno.
    # app.config.from_object('src.config.settings')

    return app
