from unittest.mock import MagicMock, patch

import pytest

from src.business_logic.formation.exceptions import NoOnisepAPIException
from src.business_logic.formation.scrap.utils.get_onisep_data import (
    HeaderKey,
    get_raw_data,
)
from src.business_logic.formation.scrap.utils.get_onisep_token import BearerToken
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


HEADERS: dict[HeaderKey, BearerToken | str] = {
    HeaderKey.APPLICATION_ID.value: "ONISEP_APP_ID",
    HeaderKey.AUTHORIZATION.value: "Bearer TEST",
}


@pytest.fixture
def mock_onisep_request():
    with patch(
        "src.business_logic.formation.scrap.utils.get_onisep_data.requests.get"
    ) as mock_requests_get:
        yield mock_requests_get


@pytest.fixture
def mock_onisep_token():
    with patch(
        "src.business_logic.formation.scrap.utils.get_onisep_data._get_headers"
    ) as mock_requests_get:
        yield mock_requests_get


def test_get_onisep_data_successful(mock_onisep_request, mock_onisep_token):
    # Arrange
    mock_onisep_token.status_code = HTTP_200_OK
    mock_onisep_token.json.return_value = HEADERS

    mock_response = MagicMock()
    mock_response.status_code = HTTP_200_OK
    mock_response.json.return_value = {"total": "5173"}
    mock_onisep_request.return_value = mock_response
    # Act
    result = get_raw_data("SHR")
    # Assert
    assert result == {"total": "5173"}


def test_get_onisep_data_retry_after_unauthorized(
    mock_onisep_request, mock_onisep_token
):
    # Arrange
    unauthorized_response = mock_onisep_request.return_value
    unauthorized_response.status_code = 401

    successful_response = mock_onisep_request.return_value
    successful_response.status_code = 200
    successful_response.json.return_value = {"total": "5173"}

    mock_onisep_token.return_value = {"total": "5173"}

    with patch(
        "src.business_logic.formation.scrap.utils.get_onisep_data.get_token"
    ) as mock_get_token:
        mock_get_token.return_value = "Bearer TEST"
        # Act
        result = get_raw_data("SHR")

    # Assert
    assert result == {"total": "5173"}


def test_get_onisep_data_raises_exception(mock_onisep_request):
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
    mock_onisep_request.return_value = mock_response

    # Act and Assert
    with pytest.raises(NoOnisepAPIException):
        get_raw_data("SHR")
