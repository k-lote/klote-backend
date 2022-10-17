from src import create_app, db
import pytest

@pytest.fixture(scope="session")
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        yield testing_client

@pytest.fixture(scope="session")
def app_with_db():
    db.create_all()
    
    yield test_client

    db.session.commit()
    db.drop_all

@pytest.fixture(scope="session")
def app_with_db():
    db.create_all()
    
    yield test_client

    db.session.commit()
    db.drop_all



