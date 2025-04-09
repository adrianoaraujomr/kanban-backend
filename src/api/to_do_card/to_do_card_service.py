import json
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import select

from src.database import get_session
from src.models.to_do_card import ToDoCard

def list_to_do_card():
    Session = get_session()
    with Session() as session:
        query = select(ToDoCard)
        cards = session.execute(query).all()
        return [{
            "id": card[0].id,
            "title": card[0].title,
            "status": card[0].status,
            "description": card[0].description,
            "image": card[0].image
        } for card in cards]

def create_to_do_card(content):
    user_identity = json.loads(get_jwt_identity())
    user_creator_id = user_identity["id"]
    new_card = ToDoCard(
        title=content["title"], 
        status=content["status"], 
        description=content["description"], 
        image=content["image"], 
        user_creator_id=user_creator_id, 
        user_responsible_id=user_creator_id,
        deadline=datetime.now()
    )
    Session = get_session()    
    with Session() as db_session:
        db_session.add(new_card)    
        db_session.commit()
    return content
