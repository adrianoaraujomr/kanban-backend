from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from .user import User


class ToDoCard(Base):
    __tablename__ = "to_do_cards"
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False, default="BACKLOG")
    sector = Column(String(250))
    user_creator_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user_responsible_id = Column(Integer, ForeignKey(User.id), nullable=False)
    priority = Column(String(250))
    deadline = Column(DateTime(timezone=True), nullable=False)

    description = Column(String(1000))
    image = Column(String(1000))

    user_creator = relationship('User', foreign_keys='ToDoCard.user_creator_id')
    user_responsible = relationship('User', foreign_keys='ToDoCard.user_responsible_id')

    def __init__(self, title=None, sector=None, user_creator_id=None, user_responsible_id=None, status=None, priority=None, deadline=None, description=None, image=None):
        self.title = title
        self.sector = sector
        self.user_creator_id = user_creator_id
        self.user_responsible_id = user_responsible_id
        self.status = status
        self.priority = priority
        self.deadline = deadline
        
        self.description = description
        self.image = image

    def __repr__(self):
        return f"<To Do Card {self.name!r}>"