import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from src.database import create_db
from src.api.usuario.usuario_route import usuario_route
from src.api.to_do_card.to_do_card_route import to_do_card_route
from src.api.math.math_route import math_route

def create_app():
    create_db()

    app = Flask(__name__)
    app.register_blueprint(usuario_route, url_prefix="/usuario")
    app.register_blueprint(to_do_card_route, url_prefix="/to-do-card")
    app.register_blueprint(math_route, url_prefix="/math")

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    CORS(app)
    jwt = JWTManager(app)

    return app

if __name__ == '__main__':
    app = create_app()
