from unittest.mock import MagicMock, patch

import pytest
from src.business_logic.formation.exceptions import NoOnisepAPIException
from src.business_logic.formation.scrap.utils.get_onisep_data import get_raw_data

from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


@pytest.fixture
def mock_onisep_request():
    with patch(
        "src.business_logic.formation.scrap.utils.get_onisep_data.requests.get"
    ) as mock_requests_get:
        yield mock_requests_get


def test_get_onisep_data_successful(mock_onisep_request):
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = HTTP_200_OK
    mock_response.json.return_value = {"total": "5173"}
    mock_onisep_request.return_value = mock_response
    # Act
    result = get_raw_data("SHR")
    # Assert
    assert result == {"total": "5173"}


def test_get_onisep_data_retry_after_unauthorized(mock_onisep_request):
    # Arrange
    unauthorized_response = MagicMock()
    unauthorized_response.status_code = HTTP_401_UNAUTHORIZED
    authorized_response = MagicMock()
    authorized_response.status_code = HTTP_200_OK
    authorized_response.json.return_value = {"total": "5173"}

    # Set up the responses for the two requests
    mock_onisep_request.side_effect = [unauthorized_response, authorized_response]

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
