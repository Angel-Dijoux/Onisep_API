from sqlalchemy import and_, exists
from src.business_logic.formation import get_formation_by_url
from src.models.user_favori import UserFavori

from src import db


def is_favorite(user_id: str, url: str) -> bool:
    formation = get_formation_by_url(url)

    if formation is None:
        return False

    favori_exist = db.session.query(
        exists().where(
            and_(
                UserFavori.user_id == user_id,
                UserFavori.formation_id == formation.id,
            )
        )
    ).scalar()

    return favori_exist
