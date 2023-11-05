from src.business_logic.formation.scrap.types import (
    FormationIsFavorite,
    FormationsWithTotal,
)

from src import db
from src.models.formation import Formation
from src.models.user_favori import UserFavori


def get_favoris_by_user_id(user_id: int) -> FormationsWithTotal:
    favoris = (
        db.session.query(Formation)
        .join(UserFavori, UserFavori.formation_id == Formation.id)
        .filter(UserFavori.user_id == user_id)
        .all()
    )

    formatted_favoris = [
        FormationIsFavorite(
            formation=favori.to_dict(),
            is_favorite=True,
        )
        for favori in favoris
    ]

    return FormationsWithTotal(
        formations=formatted_favoris, total=len(formatted_favoris)
    )
