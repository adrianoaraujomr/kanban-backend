import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from src.api.usuario.usuarioRoute import usuario_route
from src.api.to_do_card.to_do_card_route import to_do_card_route
from src.database import db_session

app = Flask(__name__)
app.register_blueprint(usuario_route, url_prefix="/usuario")
app.register_blueprint(to_do_card_route, url_prefix="/to-do-card")

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_TOKEN_LOCATION'] = ['headers']

CORS(app)
jwt = JWTManager(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()