import os
from flask import Flask
from flask_jwt_extended import JWTManager

from src.routes.alive import alive_route
from src.api.usuario.usuarioRoute import usuario_route
from src.database import db_session

app = Flask(__name__)
app.register_blueprint(alive_route, url_prefix="/alive")
app.register_blueprint(usuario_route, url_prefix="/usuario")

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()