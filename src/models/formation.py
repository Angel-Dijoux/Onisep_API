import uuid

from sqlalchemy import Column, Integer, String, Text
import strawberry
from src.models.base_model import BaseModel
from src.models.helpers.UUIDType import UUIDType

from src import db


def default_uuid5():
    namespace = uuid.uuid4()
    name = "com.onisep.app"
    return uuid.uuid5(namespace, name)


@strawberry.type
class Formation(BaseModel):
    __tablename__ = "formation"

    id: uuid.UUID = db.Column(
        UUIDType,
        default=default_uuid5,
        primary_key=True,
    )
    code_nsf: int = db.Column(db.Integer, nullable=False)
    type: str = db.Column(db.String(255), nullable=False)
    libelle: str = db.Column(db.String(255), nullable=False)
    tutelle: str = db.Column(db.String(255), nullable=False)
    url: str = db.Column(db.String(255), nullable=False, unique=True)
    domain: str = db.Column(db.Text, nullable=False)
    niveau_de_sortie: str = db.Column(db.String(255), nullable=False)
    duree: str = db.Column(db.String(255), nullable=False)
