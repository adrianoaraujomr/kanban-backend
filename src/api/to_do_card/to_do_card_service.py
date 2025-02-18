from datetime import datetime
from flask_jwt_extended import get_jwt_identity

from src.database import db_session
from src.models.to_do_card import ToDoCard

def list_to_do_card():
    cards = ToDoCard.query.all()
    return [{
        "id": card.id,
        "title": card.title,
        "status": card.status,
        "description": card.description,
        "image": card.image
    } for card in cards]

def create_to_do_card(content):
    user_creator_id = int(get_jwt_identity())
    new_card = ToDoCard(
        title=content["title"], 
        status=content["status"], 
        description=content["description"], 
        image=content["image"], 
        user_creator_id=user_creator_id, 
        user_responsible_id=user_creator_id,
        deadline=datetime.now()
    )
    db_session.add(new_card)
    db_session.commit()
    return content
