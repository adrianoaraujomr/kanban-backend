import hashlib
import json
from flask_jwt_extended import create_access_token
from sqlalchemy import select

from src.database import get_session
from src.models.user import User

def login(content):
    try: 
        Session = get_session()
        with Session() as session:
            query = select(User).where(User.email == content["username"])
            user = session.execute(query).first()
            if user is not None:
                user = user[0]
            else:
                raise Exception("Wrong username or password")
            hash_sent = hashlib.sha512(content["password"].encode()).hexdigest()
            if hash_sent == user.password:
                user_identity = json.dumps({"id": user.id})
                access_token = create_access_token(identity=user_identity) ## Tem de ser uma string
                return {
                    "email": user.email,
                    "token": access_token,
                }
            else:
                raise Exception("Wrong username or password")
    except:
        raise Exception("Something went wrong")

def list_users():
    Session = get_session()
    with Session() as session:
        query = select(User)
        users = session.execute(query).all()
        return [{"id": user[0].id, "name": user[0].name, "email": user[0].email, "avatar": user[0].avatar, "password": user[0].password} for user in users]


def get_user_by_id(id):
    try:
        Session = get_session()
        with Session() as session:
            query = select(User).where(User.id == int(id))
            user = session.execute(query).first()
            if user:
                return user[0]
            return None
    except:
        raise Exception("User don't exist")


def create_user(content):
    avatar = content["avatar"] if "avatar" in content.keys() else None
    hashed_password = hashlib.sha512(content["password"].encode()).hexdigest()
    new_user = User(content["name"], content["email"], hashed_password, avatar)
    Session = get_session()
    with Session() as db_session:
        db_session.add(new_user)
        db_session.commit()
    return content