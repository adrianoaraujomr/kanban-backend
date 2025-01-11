from flask import Flask
from src.routes.alive import alive_route
from src.api.usuario.usuarioRoute import usuario_route
from src.database import db_session

app = Flask(__name__)
app.register_blueprint(alive_route, url_prefix="/alive")
app.register_blueprint(usuario_route, url_prefix="/usuario")

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()