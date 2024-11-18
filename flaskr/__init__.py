from flask import Flask
from flask_jwt_extended import JWTManager

def create_app(config_name):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tu_clave_secreta'
    app.config['JWT_SECRET_KEY'] = 'tu_jwt_clave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial_canciones.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_RUN_PORT'] = 5001
    return app