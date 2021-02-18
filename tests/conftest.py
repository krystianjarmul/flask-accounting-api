import pytest

from src.accountment import app, db


@pytest.fixture
def client():
    if app.config['ENV'] != 'testing':
        raise EnvironmentError(
            "It's not testing environment! Set correct environment variable."
        )
    db.create_all()
    yield app.test_client()
    db.drop_all()


@pytest.fixture
def session():
    db.create_all()
    yield db.session
    db.drop_all()
