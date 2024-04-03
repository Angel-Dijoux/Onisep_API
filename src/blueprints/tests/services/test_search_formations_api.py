from unittest.mock import patch
import pytest
from src.business_logic.formation.scrap.tests.unit.test_search_onisep_formations import (
    MOKED_RESEARCH,
)
from src.business_logic.formation.scrap.types import FormationIsFavorite
from src.models.formation import Formation


@pytest.fixture
def mock_search_formations():
    with patch(
        "src.business_logic.formation.scrap.search_formation.get_raw_data"
    ) as mock_get_raw_data:
        yield mock_get_raw_data


def test_no_authenticated_search_formation_api_should_return_formations(
    client, mock_search_formations
):
    # Arrange
    mock_search_formations.return_value = MOKED_RESEARCH

    # When
    response = client.post(
        "/api/v1/formations/search", json={"query": "STH", "limit": 1}
    )

    result = response.json

    # Then
    formation_favorite = result["formations"][0]
    formation_favorite_instance = FormationIsFavorite(**formation_favorite)

    formation = formation_favorite["formation"]
    formation_instance = Formation(**formation)

    assert result["total"] == 5754
    assert isinstance(formation_favorite_instance, FormationIsFavorite)
    assert formation_favorite["is_favorite"] is False
    assert isinstance(formation_instance, Formation)
