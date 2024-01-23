# Idéo-Formations initiales en France
# https://opendata.onisep.fr/data/5fa591127f501/2-ideo-formations-initiales-en-france.htm
from enum import Enum
import os
import requests
from src.business_logic.formation.exceptions import NoOnisepAPIException
from src.business_logic.formation.scrap.utils.get_onisep_token import (
    BearerToken,
    get_token,
)
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
)


class HeaderKey(Enum):
    APPLICATION_ID = "Application-ID"
    AUTHORIZATION = "Authorization"


ONISEP_URL = "https://api.opendata.onisep.fr/api/1.0/dataset/"


def _get_headers() -> dict[HeaderKey, BearerToken | str]:
    return {
        HeaderKey.APPLICATION_ID.value: os.environ.get("ONISEP_APP_ID"),
        HeaderKey.AUTHORIZATION.value: get_token(),
    }


DATASET = "5fa591127f501"


def get_onisep_data(params: str) -> dict:
    url = ONISEP_URL + DATASET + params
    response = requests.get(url, headers=_get_headers())
    if response.status_code == HTTP_200_OK:
        return response.json()
    if response.status_code == HTTP_401_UNAUTHORIZED:
        _get_headers()[HeaderKey.AUTHORIZATION.value] = get_token()
        response = requests.get(url, headers=_get_headers())
        if response.status_code == HTTP_200_OK:
            return response.json()
    raise NoOnisepAPIException(
        f"\n status: {response.status_code} \n message : Onisep API is down.  \n dataset : {DATASET} \n headers : {_get_headers()} "
    )


def get_raw_data(
    limit: int = 10,
    offset: int = None,
    query: str = None,
) -> dict:
    if not query:
        params = f"/search?&size={limit}"
    else:
        params = f"/search?q={query}&size={limit}"
    if offset:
        params += f"&from={offset}"
    return get_onisep_data(params)
