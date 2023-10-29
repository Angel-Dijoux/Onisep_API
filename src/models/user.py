from dataclasses import dataclass
from src import db
from src.models.base_model import BaseModel


# Create User row


@dataclass
class User(BaseModel):
    __tablename__ = "user"

    id: int
    username: str
    email: str
    profile_pic_url: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    profile_pic_url = db.Column(db.Text)
    favoris = db.relationship("UserFavori", backref="user", lazy="dynamic")
