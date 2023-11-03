import os

from src.business_logic.formation.scrap.utils.get_onisep_token import get_token


ONISEP_URL = "https://api.opendata.onisep.fr/api/1.0/dataset/"

HEADERS = {
    "Application-ID": os.environ.get("ONISEP_APP_ID"),
    "Authorization": "Bearer " + get_token(),
}
