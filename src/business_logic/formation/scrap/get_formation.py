import requests

from src.business_logic.formation import HEADERS, ONISEP_URL
from src.business_logic.formation.scrap.types import (
    Facet,
    SearchedFormations,
)
from src.models.formation import Formation

# Idéo-Formations initiales en France
# https://opendata.onisep.fr/data/5fa591127f501/2-ideo-formations-initiales-en-france.htm
DATASET = "5fa591127f501"


def _get_data(params: str) -> dict:
    url = ONISEP_URL + DATASET + params
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise Exception("Onisep API is down.", response.status_code)


def _format_formations(data: list[dict]) -> list[Formation]:
    return [
        Formation(
            code_nsf=int(formation.get("code_nsf") or 0),
            type=formation.get("sigle_type_formation")
            or formation.get("libelle_type_formation"),
            libelle=formation.get("libelle_formation_principal"),
            tutelle=formation.get("tutelle"),
            url=formation.get("url_et_id_onisep"),
            domain=formation.get("domainesous-domaine"),
            niveau_de_sortie=formation.get("niveau_de_sortie_indicatif"),
            duree=formation.get("duree"),
        ).to_dict()
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
