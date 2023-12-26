# Idéo-Formations initiales en France
# https://opendata.onisep.fr/data/5fa591127f501/2-ideo-formations-initiales-en-france.htm
import requests
from src.business_logic.formation import HEADERS, ONISEP_URL
from src.business_logic.formation.exceptions import NoOnisepAPIException


DATASET = "5fa591127f501"


def get_onisep_data(params: str) -> dict:
    url = ONISEP_URL + DATASET + params
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise NoOnisepAPIException(
        f"status: {response.status_code} \n message : Onisep API is down.  \n dataset : {DATASET} \n headers : {HEADERS} "
    )
