import uuid

from sqlalchemy import Column, Integer, String, Text
from src.models.base_model import BaseModel
from src.models.helpers.UUIDType import UUIDType


def default_uuid5():
    namespace = uuid.uuid4()
    name = "com.onisep.app"
    return uuid.uuid5(namespace, name)


class Formation(BaseModel):
    __tablename__ = "formation"

    id = Column(
        UUIDType,
        default=default_uuid5,
        primary_key=True,
    )
    code_nsf = Column(Integer, nullable=False)
    type = Column(String(255), nullable=False)
    libelle = Column(String(255), nullable=False)
    tutelle = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False, unique=True)
    domain = Column(Text, nullable=False)
    niveau_de_sortie = Column(String(255), nullable=False)
    duree = Column(String(255), nullable=False)
