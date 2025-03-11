import json
from flask import Blueprint, Response
from src.api.math.math_service import my_pow

math_route = Blueprint("math", __name__)

@math_route.route("/<number>", methods=["GET"], strict_slashes=False)
def pow(number):
    result = {}
    result["result"] = my_pow(2, int(number))
    return Response(json.dumps(result), status=200, mimetype="application/json")