from src import db
from src.models.base_model import BaseModel
from src.models.helpers.UUIDType import UUIDType
from sqlalchemy_serializer import SerializerMixin


class UserFavori(BaseModel, SerializerMixin):
    __tablename__ = "user_favori"

    serialize_only = "formation_id"

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
