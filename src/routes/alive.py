from flask import Blueprint, Response
from flask_jwt_extended import jwt_required

alive_route = Blueprint("alive", __name__)

@alive_route.route("/")
@jwt_required()
def alive():
    return Response("hello world", status=200, mimetype="text/plain")