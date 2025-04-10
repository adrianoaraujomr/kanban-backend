from sqlalchemy import Column, String
from .base import Base

class Role(Base):
    __tablename__ = "roles"
    id = Column(String(50), primary_key=True)

    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return self.id