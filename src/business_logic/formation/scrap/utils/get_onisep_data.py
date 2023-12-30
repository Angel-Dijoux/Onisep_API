# Idéo-Formations initiales en France
# https://opendata.onisep.fr/data/5fa591127f501/2-ideo-formations-initiales-en-france.htm
import requests
from src.business_logic.formation import HEADERS, ONISEP_URL, HeaderKey
from src.business_logic.formation.exceptions import NoOnisepAPIException
from src.business_logic.formation.scrap.utils.get_onisep_token import get_token
from src.constants.http_status_codes import HTTP_200_OK, HTTP_401_UNAUTHORIZED


DATASET = "5fa591127f501"


def get_onisep_data(params: str) -> dict:
    url = ONISEP_URL + DATASET + params
    response = requests.get(url, headers=HEADERS)
    if response.status_code == HTTP_200_OK:
        return response.json()
    if response.status_code == HTTP_401_UNAUTHORIZED:
        HEADERS[HeaderKey.AUTHORIZATION.value] = get_token()
        response = requests.get(url, headers=HEADERS)
        if response.status_code == HTTP_200_OK:
            return response.json()
    raise NoOnisepAPIException(
        f"\n status: {response.status_code} \n message : Onisep API is down.  \n dataset : {DATASET} \n headers : {HEADERS} "
    )
