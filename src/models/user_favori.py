from dataclasses import dataclass
from typing import Callable

from cuid2 import cuid_wrapper
from sqlalchemy import UUID
from src import db
from src.models.base_model import BaseModel
from src.models.helpers.UUIDType import UUIDType


@dataclass
class UserFavori(BaseModel):
    __tablename__ = "user_favori"

    formation_id = db.Column(
        UUIDType,
        db.ForeignKey("formation.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )

    users = db.relationship("User", back_populates="favoris")
    formation = db.relationship("Formation")
