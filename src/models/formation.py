from dataclasses import dataclass
from typing import Optional
import uuid

from sqlalchemy import Text

from src import db
from src.models.base_model import BaseModel
from src.models.helpers.UUIDType import UUIDType


def default_uuid5():
    namespace = uuid.uuid4()
    name = "com.onisep.app"
    return uuid.uuid5(namespace, name)


class Formation(BaseModel):
    __tablename__ = "formation"

    id = db.Column(
        UUIDType,
        default=default_uuid5,
        primary_key=True,
    )
    code_nsf = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    libelle = db.Column(db.String(255), nullable=False)
    tutelle = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False, unique=True)
    domain = db.Column(Text, nullable=False)
    niveau_de_sortie = db.Column(db.String(255), nullable=False)
    duree = db.Column(db.String(255), nullable=False)
