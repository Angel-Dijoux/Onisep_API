from dataclasses import dataclass
from enum import unique
from typing import Callable

from cuid2 import cuid_wrapper

from src import db
from src.models.base_model import BaseModel


@dataclass
class Formation(BaseModel):
    __tablename__ = "formation"

    id: str
    code_nsf: int
    type: str
    libelle: str
    tutelle: str
    url: str
    domain: str
    niveau_de_sortie: str
    duree: str

    cuid_generator: Callable[[], str] = cuid_wrapper()

    id = db.Column(
        db.String(36),
        default=cuid_generator(),
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
