import json
from functools import wraps
from flask import abort
from flask_jwt_extended import get_jwt_identity

def get_current_user_roles():
    user_identity = get_jwt_identity()
    user = json.loads(user_identity)
    return user["roles"]

def role_authorization(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
          user_roles = get_current_user_roles()
          for role in roles:
              if role in user_roles:
                  return func(*args, **kwargs)
          return abort(403)
        return decorated_view
    return wrapper
