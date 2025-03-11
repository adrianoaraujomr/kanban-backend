import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = None
engine = None

def create_db():
    global Session, engine

    db_name = os.getenv("DB_NAME")
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    engine = create_engine(f"postgresql+pg8000://{db_user}:{db_password}@{db_host}/{db_name}", client_encoding="utf8")
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_engine():
    return engine

def get_session():
    return Session