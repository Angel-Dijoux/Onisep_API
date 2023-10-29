from dataclasses import dataclass
from typing import Callable

from cuid2 import cuid_wrapper
from src import db
from src.models.base_model import BaseModel


@dataclass
class UserFavori(BaseModel):
    __tablename__ = "user_favori"

    formation_id = db.Column(
        db.String(36),
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

    formation = db.relationship("Formation", back_populates="favoris")
    user = db.relationship("User", back_populates="users")
