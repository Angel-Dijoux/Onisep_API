from dataclasses import dataclass
from src import db
from src.models.base_model import BaseModel


@dataclass
class Favori(BaseModel):
    __tablename__ = "favori"

    formation_id: str
    user_id: int

    formation_id = db.Column(
        db.String(36),
        db.ForeignKey("formation.id", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    )
