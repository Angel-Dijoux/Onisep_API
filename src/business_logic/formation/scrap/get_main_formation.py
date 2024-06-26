from src.business_logic.formation.scrap.utils.format_formations import (
    format_formation_with_is_favorite,
    format_formations,
)
from src.business_logic.formation.scrap.types import FormationsWithTotal
from src.business_logic.formation.scrap.utils.get_onisep_data import (
    get_raw_data,
)


def get_main_formations(limit: int = 10, offset: int = None) -> FormationsWithTotal:
    data = get_raw_data(limit=limit, offset=offset)

    formated_formations = format_formations(data["results"])

    return FormationsWithTotal(data["total"], formated_formations)


def auth_get_main_formations(
    user_id: int, limit: int = 10, offset: int = None
) -> FormationsWithTotal:
    data = get_raw_data(limit=limit, offset=offset)

    formated_formations = format_formation_with_is_favorite(user_id, data["results"])

    return FormationsWithTotal(data["total"], formated_formations)
