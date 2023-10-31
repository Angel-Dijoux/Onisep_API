import requests
from src.business_logic.formation import ONISEP_URL
from src.business_logic.formation.scrap.types import (
    Facet,
    Formation,
    SearchedFormations,
)

# Idéo-Formations initiales en France
# https://opendata.onisep.fr/data/5fa591127f501/2-ideo-formations-initiales-en-france.htm
DATASET = "5fa591127f501"


def _get_data(params: str) -> dict:
    url = ONISEP_URL + DATASET + params
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()


def _format_formations(data: list[dict]) -> list[Formation]:
    return [
        Formation(
            int(formation["code_nsf"] or 0),
            formation["sigle_type_formation"] or formation["libelle_type_formation"],
            formation["libelle_formation_principal"],
            formation["tutelle"],
            formation["url_et_id_onisep"],
            formation["domainesous-domaine"],
            formation["niveau_de_sortie_indicatif"],
            formation["duree"],
        )
        for formation in data
    ]


def search_formations(query: str, limit: int, offset: int = None) -> SearchedFormations:
    params = f"/search?q={query}&size={limit}"
    if offset:
        params += f"&from={offset}"
    data = _get_data(params)

    formated_formations = _format_formations(data["results"])

    return SearchedFormations(data["total"], formated_formations)


def get_libelle_type_formation(query: str) -> list[Facet]:
    params = f"/search?q={query}"
    data = _get_data(params)
    return data["facets"]["libelle_type_formation"]


def get_main_formations(limit: int = 10, offset: int = None) -> SearchedFormations:
    params = f"/search?&size={limit}"
    if offset:
        params += f"&from={offset}"
    data = _get_data(params)

    formated_formations = _format_formations(data["results"])

    return SearchedFormations(data["total"], formated_formations)
