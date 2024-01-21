from typing import Optional

import strawberry
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from src.models.base_model import BaseModel
from src.models.user_favori import UserFavori

# Create User row


@strawberry.type
class User(BaseModel):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(80), unique=True, nullable=False)
    email: str = Column(String(200), unique=True, nullable=False)
    password = Column(Text(), nullable=False)
    profile_pic_url: Optional[str] = Column(Text)

    favoris = relationship(
        "UserFavori",
        secondary=UserFavori.__tablename__,
        primaryjoin="User.id == UserFavori.user_id",
        secondaryjoin="UserFavori.formation_id == Formation.id",
        back_populates="users",
        viewonly=True,
    )
