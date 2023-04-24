import os


def get_dev_db_uri() -> str:
    return "sqlite:///onisepapi.db"


def get_prod_db_uri() -> str:
    username = os.environ.get("DATABASE_USERNAME")
    password = os.environ.get("DATABASE_PASSWORD")
    host = os.environ.get("DATABASE_HOST")

    return f"mysql+mysqlconnector://{username}:{password}@{host}/onisep"


class Config(object):
    DEBUG = False

    SECRET_KEY = os.environ.get("SECRET_KEY")
    CSRF_ENABLED = os.environ.get("CSRF_ENABLED", True)
    CORS_HEADERS = os.environ.get("CORS_HEADERS")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    SWAGGER = {"title": "Onisep_User API", "uiversion": "3", "version": "1.0.4"}


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_dev_db_uri()


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = get_prod_db_uri()
