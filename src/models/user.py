from sqlalchemy import Column, Integer, String
from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    avatar = Column(String(250))

    def __init__(self, name=None, email=None, password=None, avatar=None):
        self.name = name
        self.email = email
        self.password = password
        self.avatar = avatar

    def __repr__(self):
        return f"<User {self.name!r}>"