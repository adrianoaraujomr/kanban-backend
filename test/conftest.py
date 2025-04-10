import pytest
from src.main import create_app
from src.database import get_engine
from src.models.base import Base
from src.models.role import Role
from src.models.user import User, user_roles
from dotenv import load_dotenv
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker

load_dotenv()

def insert_data(engine):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session() as db_session:
        user = User("root", "root@email.com", "2b64f2e3f9fee1942af9ff60d40aa5a719db33b8ba8dd4864bb4f11e25ca2bee00907de32a59429602336cac832c8f2eeff5177cc14c864dd116c8bf6ca5d9a9", "")
        role = Role("admin")
        user_role = insert(user_roles).values(id_user=1, id_role="admin")
        db_session.add(user)
        db_session.add(role)
        db_session.commit()
        db_session.execute(user_role)
        db_session.commit()

@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.update({"TESTING": True,})
    engine = get_engine()

    with app.app_context():
        Base.metadata.create_all(engine)
        insert_data(engine)
        yield app
        Base.metadata.drop_all(engine)

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
