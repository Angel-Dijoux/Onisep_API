from config import TestingConfig


def test_testing_config(db_session):
    from flask import current_app as app

    assert app.config["DEBUG"]
    assert app.config["TESTING"]
    assert (
        app.config["SQLALCHEMY_DATABASE_URI"] == TestingConfig.SQLALCHEMY_DATABASE_URI
    )
