import uuid
from dataclasses import dataclass
from email.policy import default
from enum import unique
from typing import Callable

from cuid2 import Cuid, cuid_wrapper
from sqlalchemy import UUID

from src import db
from src.models.base_model import BaseModel
from src.models.helpers.UUIDType import UUIDType


def default_uuid5():
    namespace = uuid.uuid4()
    name = "com.onisep.app"
    return uuid.uuid5(namespace, name)


@dataclass
class Formation(BaseModel):
    __tablename__ = "formation"

    id: UUIDType
    code_nsf: int
    type: str
    libelle: str
    tutelle: str
    url: str
    domain: str
    niveau_de_sortie: str
    duree: str

    id = db.Column(
        UUIDType,
        default=default_uuid5,
        primary_key=True,
    )
    code_nsf = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(120), nullable=False)
    libelle = db.Column(db.String(120), nullable=False)
    tutelle = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(255), nullable=False, unique=True)
    domain = db.Column(db.String(255), nullable=False)
    niveau_de_sortie = db.Column(db.String(120), nullable=False)
    duree = db.Column(db.String(15), nullable=False)
