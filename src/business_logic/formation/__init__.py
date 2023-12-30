from enum import Enum
import os

from src.business_logic.formation.scrap.utils.get_onisep_token import (
    BearerToken,
    get_token,
)


class HeaderKey(Enum):
    APPLICATION_ID = "Application-ID"
    AUTHORIZATION = "Authorization"


ONISEP_URL = "https://api.opendata.onisep.fr/api/1.0/dataset/"

HEADERS: dict[HeaderKey, BearerToken | str] = {
    HeaderKey.APPLICATION_ID.value: os.environ.get("ONISEP_APP_ID"),
    HeaderKey.AUTHORIZATION.value: get_token(),
}
