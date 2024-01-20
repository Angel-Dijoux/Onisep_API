from pydoc import resolve
import typing
from src.business_logic.formation.get_formation_details import (
    Formation,
    get_formation_by_id,
)
from src.models import User
import strawberry

from src import db


@strawberry.type
class Book:
    title: str
    author: str


def get_users():
    return db.session.query(User).all()


@strawberry.type
class Query:
    users: typing.List[User] = strawberry.field(resolver=get_users)
    formation: Formation = strawberry.field(resolver=get_formation_by_id)


schema = strawberry.Schema(Query)
