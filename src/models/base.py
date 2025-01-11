from sqlalchemy.ext.declarative import declarative_base
from src.database import db_session

Base = declarative_base()
Base.query = db_session.query_property()
metadata = Base.metadata