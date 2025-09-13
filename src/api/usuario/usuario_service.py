import hashlib
import json
from flask_jwt_extended import create_access_token
from sqlalchemy import select

from src.database import get_session
from src.models.user import User
from src.global_error_handling import WrongUsernameOrPassword, EntityNotFound

def login(content):
    Session = get_session()
    with Session() as session:
        query = select(User).where(User.email == content["username"])
        user = session.execute(query).first()
        if user is not None:
            user = user[0]
        else:
            raise WrongUsernameOrPassword()
        hash_sent = hashlib.sha512(content["password"].encode()).hexdigest()
        if hash_sent == user.password:
            user_identity = json.dumps({"id": user.id, "roles": [role.id for role in user.roles]})
            access_token = create_access_token(identity=user_identity)
            return {
                "email": user.email,
                "token": access_token,
            }
        else:
            raise WrongUsernameOrPassword()

def list_users():
    Session = get_session()
    with Session() as session:
        query = select(User)
        users = session.execute(query).all()
        return [{"id": user[0].id, "name": user[0].name, "email": user[0].email, "avatar": user[0].avatar, "password": user[0].password} for user in users]


def get_user_by_id(id):
    Session = get_session()
    with Session() as session:
        query = select(User).where(User.id == int(id))
        user = session.execute(query).first()
        if user:
            return user[0]
        else:
            raise EntityNotFound()


def create_user(content):
    avatar = content["avatar"] if "avatar" in content.keys() else None
    hashed_password = hashlib.sha512(content["password"].encode()).hexdigest()
    new_user = User(content["name"], content["email"], hashed_password, avatar)
    Session = get_session()
    with Session() as db_session:
        db_session.add(new_user)
        db_session.commit()
    return content