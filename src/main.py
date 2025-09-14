import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from src.database import create_db
from src.api.usuario.usuario_route import usuario_route
from src.api.to_do_card.to_do_card_route import to_do_card_route
from src.api.math.math_route import math_route
from src.global_error_handling import handle_exception_http_exception, handle_exception_sqlalchemy_error

from logging.config import dictConfig

def create_app():
    create_db()

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default',
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi'],
        }
    })

    app = Flask(__name__)
    app.register_blueprint(usuario_route, url_prefix="/usuario")
    app.register_blueprint(to_do_card_route, url_prefix="/to-do-card")
    app.register_blueprint(math_route, url_prefix="/math")

    app.register_error_handler(HTTPException, handle_exception_http_exception)
    app.register_error_handler(SQLAlchemyError, handle_exception_sqlalchemy_error)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    CORS(app)
    jwt = JWTManager(app)

    return app

if __name__ == '__main__':
    app = create_app()
