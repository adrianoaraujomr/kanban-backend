import json
import logging

from datetime import datetime
from typing import List
from flask import abort
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import select

from src.database import get_session
from src.models.to_do_card import ToDoCard
from src.integrations.github import github_adapter
from src.integrations.github.enum.lock_enum import LockReason

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
    logging.info(f"Creating to-do card: {new_card.title}")
    with Session() as db_session:
        db_session.add(new_card)    
        db_session.commit()
    return content

def list_issues(owner, repository) -> List[dict]:
    return [issue.__dict__ for issue in github_adapter.get_issues_from_repo(owner, repository)]

def create_issue(owner, repository, issue) -> dict:
    issue = github_adapter.create_issue(owner, repository, issue)
    if issue is None:
        abort(500, "Something went wrong")
    return issue.__dict__

def get_issue(owner, repository, issue_number) -> dict:
    issue = github_adapter.get_issue_from_repo(owner, repository, issue_number)
    return issue.__dict__

def update_issue(owner, repository, issue_number, issue) -> dict:
    issue = github_adapter.update_issue(owner, repository, issue_number, issue)
    if issue is None:
        abort(500, "Something went wrong")
    return issue.__dict__

def delete_issue(owner, repository, issue_number) -> bool:
    result = github_adapter.lock_issue(owner, repository, issue_number, LockReason.SPAM)
    return result