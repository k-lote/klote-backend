from src import create_app
import pytest

@pytest.fixture(scope="module")
def app():
    flask_app = create_app()
    yield flask_app