from flask import Blueprint, Response

alive_route = Blueprint("alive", __name__)

@alive_route.route("/")
def alive():
    return Response("hello world", status=200, mimetype="text/plain")