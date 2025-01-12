import json
from flask import Blueprint, Response, request
from flask_jwt_extended import jwt_required
from src.api.usuario.usuarioService import list_users, create_user, login

usuario_route = Blueprint("usuario", __name__)

@usuario_route.route("/login", methods=["POST"])
def login_user_route():
    content = request.json
    result = login(content)
    return Response(json.dumps(result), status=200, mimetype="application/json")

@usuario_route.route("/")
@jwt_required()
def list_users_route():
    result = list_users()
    return Response(json.dumps(result), status=200, mimetype="application/json")


@usuario_route.route("/", methods=["POST"])
@jwt_required()
def create_user_route():
    content = request.json
    result = create_user(content)
    return Response(json.dumps(result), status=201, mimetype="application/json")