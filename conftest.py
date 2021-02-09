import pytest

from app import db, app


@pytest.fixture
def client():
    db.create_all()
    yield app.test_client()
    db.drop_all()
