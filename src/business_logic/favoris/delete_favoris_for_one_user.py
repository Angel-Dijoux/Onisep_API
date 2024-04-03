from src.models.user_favori import UserFavori
from src import db


def delete_favoris_for_one_user(user_id: int) -> None:
    favoris = db.session.query(UserFavori).filter(UserFavori.user_id == user_id).all()
    [db.session.delete(f) for f in favoris]
    db.session.commit()
