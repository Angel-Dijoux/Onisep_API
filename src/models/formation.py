import uuid

import strawberry
from sqlalchemy import Column, Integer, String, Text

from src.models.base_model import BaseModel
from src.models.helpers.UUIDType import UUIDType


def default_uuid5():
    namespace = uuid.uuid4()
    name = "com.onisep.app"
    return uuid.uuid5(namespace, name)


@strawberry.type
class Formation(BaseModel):
    __tablename__ = "formation"

    id: uuid.UUID = Column(
        UUIDType,
        default=default_uuid5,
        primary_key=True,
    )
    code_nsf: int = Column(Integer, nullable=False)
    type: str = Column(String(255), nullable=False)
    libelle: str = Column(String(255), nullable=False)
    tutelle: str = Column(String(255), nullable=False)
    url: str = Column(String(255), nullable=False, unique=True)
    domain: str = Column(Text, nullable=False)
    niveau_de_sortie: str = Column(String(255), nullable=False)
    duree: str = Column(String(255), nullable=False)
