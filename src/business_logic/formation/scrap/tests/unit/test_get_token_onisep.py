import pytest
from unittest.mock import patch
from src.business_logic.formation.exceptions import NoOnisepAPIException

from src.business_logic.formation.scrap.utils.get_onisep_token import (
    get_token,
)
from src.constants.http_status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND


@pytest.fixture
def mock_onisep_token():
    with patch(
        "src.business_logic.formation.scrap.utils.get_onisep_token._send_request"
    ) as mock_requests_get:
        yield mock_requests_get


def test_get_token_success(mock_onisep_token):
    mock_onisep_token.return_value.status_code = HTTP_200_OK
    mock_onisep_token.return_value.json.return_value = {"token": "fake_token"}

    token = get_token()

    assert token == "Bearer fake_token"


def test_get_token_failure(mock_onisep_token):
    mock_onisep_token.return_value.status_code = HTTP_404_NOT_FOUND

    with pytest.raises(NoOnisepAPIException):
        get_token()
