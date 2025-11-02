import json
import src.api.to_do_card.to_do_card_service as to_do_card_service

from src.api.to_do_card.dto.create_issue_dto import CreateIssueDto, UpdateIssueDto

from flask import Blueprint, Response, request, abort
from flask_jwt_extended import jwt_required

to_do_card_route = Blueprint("to-do-card", __name__)
create_issue_schema = CreateIssueDto()
update_issue_schema = UpdateIssueDto()

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
    return Response(json.dumps(result), status=201, mimetype="application/json")

@to_do_card_route.route("/issues/<owner>/<repository>/<issue_number>", methods=["GET"], strict_slashes=False)
def get_issue(owner, repository, issue_number) -> Response:
    result = to_do_card_service.get_issue(owner, repository,issue_number)
    return Response(json.dumps(result), status=200, mimetype="application/json")
    

@to_do_card_route.route("/issues/<owner>/<repository>/<issue_number>", methods=["PUT"], strict_slashes=False)
def update_issue(owner, repository, issue_number) -> Response:
    content = request.json
    errors = update_issue_schema.validate(content)
    if errors:
        abort(400, str(errors))
    result = to_do_card_service.update_issue(owner, repository, issue_number, content)
    return Response(json.dumps(result), status=200, mimetype="application/json")


@to_do_card_route.route("/issues/<owner>/<repository>/<issue_number>", methods=["DELETE"], strict_slashes=False)
def delete_issue(owner, repository, issue_number) -> Response:
    result = to_do_card_service.delete_issue(owner, repository, issue_number)
    if not result:
        return Response(json.dumps({'msg': 'Failed to delete Issue'}), status=500)
    return Response(json.dumps({'msg': 'Issue deleted'}), status=200)
