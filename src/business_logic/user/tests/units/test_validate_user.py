import pytest

from src.business_logic.user.exceptions import AuthenticationException
from src.business_logic.user.validate_user import validate_user
from src.models.user import User
from src.tests.factories.factories import UserFactory
from werkzeug.security import generate_password_hash


def test_validate_user_should_return_user(db_session):
    # Given
    user: User = UserFactory(
        email="test1@example.com", password=generate_password_hash("password123")
    )
    db_session.add(user)
    db_session.commit()

    # Act
    result = validate_user("test1@example.com", "password123")

    # Assert
    assert result == user


def test_validate_user_should_create_email_exception(db_session):
    # Given
    user: User = UserFactory(
        email="test2@example.com", password=generate_password_hash("password123")
    )
    db_session.add(user)
    db_session.commit()

    # Act & Assert
    with pytest.raises(AuthenticationException) as exc_info:
        validate_user("bad.email2@gmail.com", "password123")
    assert str(exc_info.value) == "User not found"


def test_validate_user_should_create_password_exception(db_session):
    # Given
    user: User = UserFactory(
        email="test3@example.com", password=generate_password_hash("password123")
    )
    db_session.add(user)
    db_session.commit()

    with pytest.raises(AuthenticationException) as exc_info:
        validate_user("test3@example.com", "badPassword")
    assert str(exc_info.value) == "Incorrect password"


def test_validate_user_should_create_missing_email_or_password_exception():
    # Act & Assert
    with pytest.raises(AuthenticationException) as exc_info:
        validate_user("", "password")
    assert str(exc_info.value) == "Email and password are required fields"
