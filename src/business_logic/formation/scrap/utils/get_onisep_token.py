import os
from typing import Literal
import requests

from src.business_logic.formation.exceptions import NoOnisepAPIException


URL = "https://api.opendata.onisep.fr/api/1.0/login"


def _get_form_data() -> dict[str, str]:
    return {
        "email": os.environ.get("ONISEP_EMAIL"),
        "password": os.environ.get("ONISEP_PASSWORD"),
    }


BearerToken = Literal["Bearer"]


def get_token() -> BearerToken:
    response = requests.post(URL, data=_get_form_data())
    if response.status_code == 200:
        data = response.json()
        return f"Bearer {data.get('token')}"
    raise NoOnisepAPIException(
        f"Failed to get onisep token. Status code: {response.status_code}"
    )
