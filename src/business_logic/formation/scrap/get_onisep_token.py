import os
from loguru import logger
import requests


URL = "https://api.opendata.onisep.fr/api/1.0/login"


def _get_form_data() -> dict[str, str]:
    return {
        "email": os.environ.get("ONISEP_EMAIL"),
        "password": os.environ.get("ONISEP_PASSWORD"),
    }


def get_token() -> str | None:
    response = requests.post(URL, data=_get_form_data())
    if response.status_code == 200:
        data = response.json()
        return data.get("token")
    else:
        logger.warning(
            f"Failed to get onisep token. Status code: {response.status_code}"
        )
        return None
