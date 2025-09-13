import json
from flask import Blueprint, Response, request
from flask_jwt_extended import jwt_required
from src.api.to_do_card.to_do_card_service import list_to_do_card, create_to_do_card

to_do_card_route = Blueprint("to-do-card", __name__)

@to_do_card_route.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
def list_cards_route():
    result = list_to_do_card()
    return Response(json.dumps(result), status=200, mimetype="application/json")

@to_do_card_route.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_card_route():
    content = request.json
    result = create_to_do_card(content)
    return Response(json.dumps(result), status=201, mimetype="application/json")