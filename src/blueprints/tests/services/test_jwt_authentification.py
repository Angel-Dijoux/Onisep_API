import pytest
from src.models.user import User
from src.tests.factories.factories import UserFactory
from werkzeug.security import generate_password_hash


@pytest.fixture
def user_in_db(db_session) -> User:
    user: User = UserFactory(
        email="test@example.com", password=generate_password_hash("password123")
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_jwt_authentification_should_return_user_payload_with_tokens(
    client, user_in_db
):
    # When
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )

    result = response.json

    # Then
    assert result["user"]["id"] == user_in_db.id
    assert result["user"]["email"] == user_in_db.email
    assert result["user"]["username"] == user_in_db.username
    assert result["user"]["access"] != ""
    assert result["user"]["refresh"] != ""


def test_jwt_authentification_should_return_401_unauthorized(client, user_in_db):
    # When
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "bad.email@example.com", "password": "password123"},
    )

    result = response.json
    status = response.status

    assert status == "401 UNAUTHORIZED"
    assert result["error"] == "User not found"
