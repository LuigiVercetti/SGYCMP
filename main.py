from flask import Flask, render_template
from config import Config
from models import db
from routes import routes

def create_app():
    app = Flask(__name__, template_folder='templates')  # Ahora toma templates de /templates

    # Configuración
    app.config.from_object(Config)

    # Inicializar base de datos
    db.init_app(app)

    # Registrar rutas del Blueprint
    app.register_blueprint(routes)

    # Ruta raíz -> login.html desde /templates
    @app.route('/')
    def home():
        return render_template('login.html')

    return app

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(host= 'host=0.0.0.0', port=5000, debug=True)