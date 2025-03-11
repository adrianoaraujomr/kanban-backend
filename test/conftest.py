import pytest
from src.main import create_app
from src.database import get_engine
from src.models.base import Base
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.update({"TESTING": True,})
    engine = get_engine()

    with app.app_context():
        Base.metadata.create_all(engine)
        yield app
        Base.metadata.drop_all(engine)

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
