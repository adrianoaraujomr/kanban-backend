import json
from flask import Response
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

def handle_exception_http_exception(e: HTTPException):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

def handle_exception_sqlalchemy_error(e: SQLAlchemyError):
    response = Response()
    response.data = json.dumps({
        "code": 500,
        "name": "Database Error",
        "description": f"SQLAlchemy Error: {e.code}",
    })
    response.content_type = "application/json"
    response.status_code = 500
    return response
    
class WrongUsernameOrPassword(HTTPException):
    code = 401
    description = "Wrong username or password"

class EntityNotFound(HTTPException):
    code = 404
    description = "Entity not found"
    
    