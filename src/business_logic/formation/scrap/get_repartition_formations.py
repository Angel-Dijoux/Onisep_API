from src.business_logic.formation.scrap.types import Facet
from src.business_logic.formation.scrap.utils.get_onisep_data import get_onisep_data


def _process_data(data: dict) -> list[Facet]:
    return [Facet(**facet) for facet in data]


def get_libelle_type_formation(query: str) -> list[Facet]:
    params = f"/search?q={query}"
    data = get_onisep_data(params)
    return _process_data(data["facets"]["libelle_type_formation"])
