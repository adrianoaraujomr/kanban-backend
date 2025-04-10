from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .base import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("id_user", Integer, ForeignKey("users.id"), primary_key=True),
    Column("id_role", String(50), ForeignKey("roles.id"), primary_key=True),
)

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
        return f"<User name={self.name!r}, email={self.email!r}, password={self.password!r}>"
    
from src.models.role import Role
User.roles = relationship("Role", secondary="user_roles")
