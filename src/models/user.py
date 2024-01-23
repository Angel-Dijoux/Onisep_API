from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Text
from src.models.base_model import BaseModel
from src.models.user_favori import UserFavori
from sqlalchemy.orm import relationship


# Create User row


@dataclass
class User(BaseModel):
    __tablename__ = "user"

    id: int
    username: str
    email: str
    profile_pic_url: str

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(Text(), nullable=False)
    profile_pic_url = Column(Text)

    favoris = relationship(
        "UserFavori",
        secondary=UserFavori.__tablename__,
        primaryjoin="User.id == UserFavori.user_id",
        secondaryjoin="UserFavori.formation_id == Formation.id",
        back_populates="users",
        viewonly=True,
    )
