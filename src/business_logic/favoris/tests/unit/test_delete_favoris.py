import pytest

from src.business_logic.favoris.delete_favoris_for_one_user import (
    delete_favoris_for_one_user,
)
from src.models.formation import Formation
from src.models.user import User
from src.models.user_favori import UserFavori
from src.tests.factories.factories import (
    FormationFactory,
    UserFactory,
    UserFavorisFactory,
)


@pytest.fixture
def user_favori_in_db(db_session) -> User:
    user: User = UserFactory()
    db_session.add(user)

    formation: Formation = FormationFactory()
    db_session.add(formation)

    user_favori: UserFavori = UserFavorisFactory(
        formation_id=formation.id, user_id=user.id
    )
    db_session.add(user_favori)

    db_session.commit()
    return user


def test_delete_user_favoris_should_remove_favoris(db_session, user_favori_in_db):
    # Arrange
    user = user_favori_in_db

    # Act
    delete_favoris_for_one_user(user.id)

    # Assert
    favoris = db_session.query(UserFavori).filter(UserFavori.user_id == user.id).all()

    assert len(favoris) == 0
