import hashlib
from flask_jwt_extended import create_access_token

from src.database import db_session
from src.models.user import User

def login(content):
    try: 
        user = User.query.filter_by(email=content["username"]).first()
        hash_sent = hashlib.sha512(content["password"].encode()).hexdigest()
        if user and hash_sent == user.password:
            access_token = create_access_token(identity=str(user.id)) ## Tem de ser uma string
            return {
                "email": user.email,
                "token": access_token,
            }
        else:
            raise Exception("Access denied")
    except:
        raise Exception("Access denied")

def list_users():
    users = User.query.all()
    return [{"id": user.id, "name": user.name, "email": user.email, "avatar": user.avatar, "password": user.password} for user in users]


def get_user_by_id(id):
    try:
        user = User.query.filter_by(id=int(id)).first()
        return {"id": user.id, "name": user.name, "email": user.email}
    except:
        raise Exception("User don't exist")


def create_user(content):
    avatar = content["avatar"] if "avatar" in content.keys() else None
    hashed_password = hashlib.sha512(content["password"].encode()).hexdigest()
    new_user = User(content["name"], content["email"], hashed_password, avatar)
    db_session.add(new_user)
    db_session.commit()
    return content