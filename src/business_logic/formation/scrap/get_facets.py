import requests

from src.business_logic.formation.scrap.types import Facet
from .. import ONISEP_URL

# Idéo-Actions de formation initiale-Univers enseignement supérieur
# https://opendata.onisep.fr/data/605344579a7d7/2-ideo-actions-de-formation-initiale-univers-enseignement-superieur.htm
DATASET = "605344579a7d7"


def _get_data() -> dict:
    url = ONISEP_URL + DATASET + "/search?size=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()


def _find_data_by_key(key: str) -> list[Facet]:
    data = _get_data()
    return data["facets"][key]


def get_for_type() -> list[Facet]:
    return _find_data_by_key("for_type")


def get_nature_du_certificat() -> list[Facet]:
    return _find_data_by_key("for_nature_du_certificat")


def get_niveau_de_sortie() -> list[Facet]:
    return _find_data_by_key("for_niveau_de_sortie")


def get_ens_status() -> list[Facet]:
    return _find_data_by_key("ens_statut")


def get_ens_departement() -> list[Facet]:
    return _find_data_by_key("ens_departement")


def get_ens_academie() -> list[Facet]:
    return _find_data_by_key("ens_academie")


def get_ens_region() -> list[Facet]:
    return _find_data_by_key("ens_region")


def get_duree_cycle() -> list[Facet]:
    return _find_data_by_key("af_duree_cycle_standard")
