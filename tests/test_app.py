import pytest

from src.app import app


@pytest.fixture
def client():
    app.config.update(
        {
            "TESTING": True,
            "MONGODB_SETTINGS": {
                "db": "test_db",
                "host": "mongomock://localhost",
            },
        }
    )
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "API works!"}
