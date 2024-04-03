import pytest

from src.business_logic.user.exceptions import AuthenticationException
from src.business_logic.user.validate_user import validate_user
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


def test_validate_user_should_return_user(user_in_db):
    # Act
    result = validate_user("test@example.com", "password123")

    # Assert
    assert result == user_in_db


def test_validate_user_should_create_email_exception(user_in_db):
    # Act & Assert
    with pytest.raises(AuthenticationException) as exc_info:
        validate_user("bad.email@gmail.com", "password123")
    assert str(exc_info.value) == "User not found"


def test_validate_user_should_create_password_exception(user_in_db):
    with pytest.raises(AuthenticationException) as exc_info:
        validate_user("test@example.com", "badPassword")
    assert str(exc_info.value) == "Incorrect password"


def test_validate_user_should_create_missing_email_or_password_exception(user_in_db):
    # Act & Assert
    with pytest.raises(AuthenticationException) as exc_info:
        validate_user("", "password")
    assert str(exc_info.value) == "Email and password are required fields"
