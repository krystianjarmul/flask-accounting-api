import pytest

from app import db, app


@pytest.fixture
def client():
    if app.config['ENV'] != 'testing':
        raise EnvironmentError(
            "It's not testing environment! Set correct environment variable."
        )
    db.create_all()
    yield app.test_client()
    db.drop_all()
