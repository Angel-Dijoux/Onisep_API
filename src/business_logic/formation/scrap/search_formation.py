from src.business_logic.formation.scrap.utils.format_formations import (
    format_formation_with_is_favorite,
    format_formations,
)
from src.business_logic.formation.scrap.types import FormationsWithTotal
from src.business_logic.formation.scrap.utils.get_onisep_data import (
    get_raw_data,
)


def search_formations(
    query: str, limit: int, offset: int = None
) -> FormationsWithTotal:
    data = get_raw_data(limit=limit, offset=offset, query=query)

    formated_formations = format_formations(data["results"])

    return FormationsWithTotal(total=data["total"], formations=formated_formations)


def auth_search_formations(
    user_id: int, query: str, limit: int, offset: int = None
) -> FormationsWithTotal:
    data = get_raw_data(limit=limit, offset=offset, query=query)
    formated_formations = format_formation_with_is_favorite(user_id, data["results"])

    return FormationsWithTotal(total=data["total"], formations=formated_formations)
