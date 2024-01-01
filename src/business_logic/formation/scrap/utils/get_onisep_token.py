import os
from typing import Literal
import requests
from urllib3 import Retry

from src.business_logic.formation.exceptions import NoOnisepAPIException
from src.constants.http_status_codes import HTTP_200_OK
from requests.adapters import HTTPAdapter

URL = "https://api.opendata.onisep.fr/api/1.0/login"
RETRY = 3
ERROR_STATUS = [500, 502, 503, 504]


def _get_form_data() -> dict[str, str]:
    return {
        "email": os.environ.get("ONISEP_EMAIL"),
        "password": os.environ.get("ONISEP_PASSWORD"),
    }


def _send_request(session: requests.Session) -> requests.Response:
    response = session.post(URL, data=_get_form_data())
    return response


BearerToken = Literal["Bearer"]


def get_token() -> BearerToken:
    session = create_retry_session()
    for _ in range(RETRY):
        response = _send_request(session)
        if response.status_code == HTTP_200_OK:
            data = response.json()
            return f"Bearer {data.get('token')}"
        elif response.status_code in ERROR_STATUS:
            pass
        else:
            raise NoOnisepAPIException(
                f"Failed to get onisep token. Status code: {response.status_code}"
            )
    raise NoOnisepAPIException("Maximum number of retry attempts reached.")


def create_retry_session() -> requests.Session:
    session = requests.Session()
    retry_strategy = Retry(
        total=RETRY,
        backoff_factor=1,
        status_forcelist=ERROR_STATUS,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    return session
