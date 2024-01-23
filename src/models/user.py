from typing import Optional

import strawberry

from src import db
from src.models.base_model import BaseModel
from src.models.user_favori import UserFavori

# Create User row


@strawberry.type
class User(BaseModel):
    __tablename__ = "user"

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    email: str = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    profile_pic_url: Optional[str] = db.Column(db.Text)

    favoris: list[UserFavori] = db.relationship(
        "UserFavori",
        secondary=UserFavori.__tablename__,
        primaryjoin="User.id == UserFavori.user_id",
        secondaryjoin="UserFavori.formation_id == Formation.id",
        back_populates="users",
        viewonly=True,
    )
