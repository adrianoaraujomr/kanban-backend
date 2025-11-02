import json
from flask import Response
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from requests.exceptions import HTTPError

def handle_standar_exception(e: Exception):
    response = Response(status=500)
    response.data = json.dumps({
        "code": 500,
        "name": "Python Exception",
        "description": "Deu Ruim",
    })
    response.content_type = "application/json"
    return response

def handle_exception_http_exception(e: HTTPException):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

def handle_expection_requests_http_error(e: HTTPError):
    response = Response(status=e.response.status_code)
    response.data = json.dumps({
        "code": e.response.status_code,
        "name": "External API Error",
        "description": f"External API Error: {e.response.reason}",
    })
    response.content_type = "application/json"
    return response

def handle_exception_sqlalchemy_error(e: SQLAlchemyError):
    response = Response(status=500)
    response.data = json.dumps({
        "code": 500,
        "name": "Database Error",
        "description": f"SQLAlchemy Error: {e.code}",
    })
    response.content_type = "application/json"
    return response
    
class WrongUsernameOrPassword(HTTPException):
    code = 401
    description = "Wrong username or password"

class EntityNotFound(HTTPException):
    code = 404
    description = "Entity not found"
    
    