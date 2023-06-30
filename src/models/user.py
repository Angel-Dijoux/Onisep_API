from dataclasses import dataclass
from src import db

# Create User row


@dataclass
class User(db.Model):
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
    favoris = db.relationship("Favori", backref="user")

    def __repr__(self) -> str:
        return "User>>> {self.username}"
