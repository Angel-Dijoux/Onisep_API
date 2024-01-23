from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import (
    create_access_token,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session

from src import create_app
from src import db as _db
from src.business_logic.formation.scrap.utils.get_onisep_token import BearerToken
from src.models.user import User


@pytest.fixture(autouse=True, scope="session")
def app() -> Flask:
    app = create_app("testing")
    return app


@pytest.fixture(scope="module")
def db(app: Flask) -> SQLAlchemy:
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()


@pytest.fixture(scope="module")
def db_session(db: SQLAlchemy) -> Session:
    yield db.session
    db.session.rollback()
    db.session.close()


@pytest.fixture()
def client(app: Flask, db: SQLAlchemy) -> Generator[FlaskClient, None, None]:
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="module")
def authenticated_user(db_session: Session) -> tuple[User, dict[str, BearerToken]]:
    from src.tests.factories import UserFactory

    user: User = UserFactory()
    db_session.add(user)
    db_session.commit()

    headers = {"Authorization": f"Bearer {create_access_token(identity=user.id)}"}

    yield user, headers
