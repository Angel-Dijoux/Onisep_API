from sqlalchemy import Column, ForeignKey, Integer
from src.models.base_model import BaseModel
from src.models import Formation
from src.models.helpers.UUIDType import UUIDType
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship


class UserFavori(BaseModel, SerializerMixin):
    __tablename__ = "user_favori"

    serialize_only = "formation_id"

    formation_id = Column(
        UUIDType,
        ForeignKey("formation.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )

    users = relationship("User", back_populates="favoris")
    formation: list[Formation] = relationship("Formation")
