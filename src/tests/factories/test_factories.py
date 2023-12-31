import uuid
from sqlalchemy import func
from src.models.formation import Formation
from src.tests.factories.factories import FormationFactory


def test_check_if_formation_table_is_empty_should_return_0(db_session):
    formation_count = db_session.query(func.count(Formation.id)).scalar()
    assert formation_count == 0


def test_create_one_formation_should_return_1(db_session):
    formation: Formation = FormationFactory()
    db_session.add(formation)
    db_session.commit()

    assert formation.id is not None
    assert isinstance(formation.id, uuid.UUID)
    formation_count = db_session.query(func.count(Formation.id)).scalar()
    assert formation_count == 1
