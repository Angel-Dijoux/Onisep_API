from sqlalchemy import ForeignKey
from sqlalchemy_serializer import SerializerMixin

from src import db
from src.models import Formation
from src.models.base_model import BaseModel
from src.models.helpers.UUIDType import UUIDType


class UserFavori(BaseModel, SerializerMixin):
    __tablename__ = "user_favori"

    serialize_only = "formation_id"

    formation_id = db.Column(
        UUIDType,
        ForeignKey("formation.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )

    user_id = db.Column(
        db.Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )

    users = db.relationship("User", back_populates="favoris")
    formation: list[Formation] = db.relationship("Formation")
