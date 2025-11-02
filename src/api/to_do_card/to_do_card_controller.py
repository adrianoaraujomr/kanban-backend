import json
import src.api.to_do_card.to_do_card_service as to_do_card_service

from src.api.to_do_card.dto.create_issue_dto import CreateIssueDto

from flask import Blueprint, Response, request, abort
from flask_jwt_extended import jwt_required

to_do_card_route = Blueprint("to-do-card", __name__)
create_issue_schema = CreateIssueDto()

@to_do_card_route.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
def list_cards_route() -> Response:
    result = to_do_card_service.list_to_do_card()
    return Response(json.dumps(result), status=200, mimetype="application/json")

@to_do_card_route.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_card_route() -> Response:
    content = request.json
    result = to_do_card_service.create_to_do_card(content)
    return Response(json.dumps(result), status=201, mimetype="application/json")

@to_do_card_route.route("/issues/<owner>/<repository>", methods=["GET"], strict_slashes=False)
@jwt_required()
def list_issues(owner, repository) -> Response:
    result = to_do_card_service.list_issues(owner, repository)
    return Response(json.dumps(result), status=200, mimetype="application/json")

@to_do_card_route.route("/issues/<owner>/<repository>", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_issue(owner, repository) -> Response:
    content = request.json
    errors = create_issue_schema.validate(content)
    if errors:
        abort(400, str(errors))
    result = to_do_card_service.create_issue(owner, repository, content)
    return Response(json.dumps(result), stauts=201, mimetype="application/json")
    
