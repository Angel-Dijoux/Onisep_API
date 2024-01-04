from src.models.formation import Formation
from src import db


def get_formation_by_url(url: str) -> Formation | None:
    return db.session.query(Formation).filter(Formation.url == url).first()
