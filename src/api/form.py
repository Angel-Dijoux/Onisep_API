import typing
from src.models.formation import Formation
import strawberry
from src import db


@strawberry.type
class Book:
    title: str
    author: str


def get_formations():
    return db.session.query(Formation).all()
