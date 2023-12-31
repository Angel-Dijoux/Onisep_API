from typing import Generator
import pytest
from flask import Flask
from sqlalchemy.orm import Session
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from src import create_app
from src import db as _db


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
