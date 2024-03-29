from unittest.mock import patch

import pytest
from src.business_logic.formation.scrap.search_formation import (
    auth_search_formations,
    search_formations,
)
from src.business_logic.formation.scrap.types import (
    FormationsWithTotal,
)
from src.business_logic.formation.scrap.utils.format_formations import (
    format_formation_with_is_favorite,
    format_formations,
)
from src.models.user import User
from src.models.user_favori import UserFavori
from src.tests.factories.factories import (
    UserFactory,
    UserFavorisFactory,
)


MOKED_RESEARCH = {
    "total": 5754,
    "size": 1,
    "results": [
        {
            "code_nsf": "334",
            "sigle_type_formation": "",
            "libelle_type_formation": "baccalauréat technologique",
            "libelle_formation_principal": "bac techno STHR Sciences et technologies de l'hôtellerie et de la restauration",
            "sigle_formation": "STHR",
            "duree": "1 an",
            "niveau_de_sortie_indicatif": "Bac ou équivalent",
            "code_rncp": "",
            "niveau_de_certification": "4",
            "libelle_niveau_de_certification": "niveau 4 (bac ou équivalent)",
            "tutelle": "Ministère chargé de l'Éducation nationale et de la Jeunesse",
            "url_et_id_onisep": "http://www.onisep.fr/http/redirection/formation/slug/FOR.494",
            "domainesous-domaine": "hôtellerie-restauration, tourisme/hôtellerie | hôtellerie-restauration, tourisme/restauration",
        }
    ],
}


@pytest.fixture
def mock_search_formations():
    with patch(
        "src.business_logic.formation.scrap.search_formation.get_raw_data"
    ) as mock_get_raw_data:
        yield mock_get_raw_data


def test_search_formations_should_return_formations_without_favorite(
    mock_search_formations,
):
    # Arrange
    mock_search_formations.return_value = MOKED_RESEARCH

    # Act
    formations = search_formations(limit=1, offset=None, query="STHR1")

    # Assert
    moked_formation = MOKED_RESEARCH["results"]
    waited_formations = format_formations(moked_formation)
    waited_result = FormationsWithTotal(
        total=MOKED_RESEARCH["total"], formations=waited_formations
    )

    assert formations == waited_result
    mock_search_formations.assert_called_once_with(limit=1, offset=None, query="STHR1")


def test_authenticated_search_formations_should_return_formations_with_favorite(
    mock_search_formations, db_session
):
    # Arrange
    mock_search_formations.return_value = MOKED_RESEARCH

    # Given
    user: User = UserFactory()
    db_session.add(user)
    db_session.flush()

    user_favori: UserFavori = UserFavorisFactory(user_id=user.id)
    db_session.add(user_favori)
    db_session.commit()

    # Act
    formations = auth_search_formations(
        user_id=user.id, query="STHR2", limit=1, offset=None
    )

    # Assert
    moked_formation = MOKED_RESEARCH["results"]
    waited_formations = format_formation_with_is_favorite(user.id, moked_formation)
    waited_result = FormationsWithTotal(
        total=MOKED_RESEARCH["total"], formations=waited_formations
    )

    assert formations == waited_result
    mock_search_formations.assert_called_once_with(query="STHR2", limit=1, offset=None)
