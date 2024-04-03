from src.business_logic.user.exceptions import AuthenticationException
from src.models.user import User
from werkzeug.security import check_password_hash
from src import db


def validate_user(email: str, password: str) -> User:
    if not email or not password:
        raise AuthenticationException("Email and password are required fields")
    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        raise AuthenticationException("User not found")
    if not check_password_hash(user.password, password):
        raise AuthenticationException("Incorrect password")
    return user
