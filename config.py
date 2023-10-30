import os
from dotenv import load_dotenv

load_dotenv()


def get_db_dev_uri() -> str:
    username = os.environ.get("DATABASE_USERNAME")
    password = os.environ.get("DATABASE_PASSWORD")
    host = os.environ.get("DATABASE_HOST")
    port = os.environ.get("PORT")
    return f"mysql+mysqlconnector://{str(username)}:{str(password)}@{str(host)}:{str(port)}/onisep?charset=utf8mb4&collation=utf8mb4_general_ci"


def get_db_prod_uri() -> str:
    username = os.environ.get("DATABASE_USERNAME")
    password = os.environ.get("DATABASE_PASSWORD")
    host = os.environ.get("DATABASE_HOST")
    return f"mysql+mysqlconnector://{str(username)}:{str(password)}@{str(host)}/onisep?charset=utf8mb4&collation=utf8mb4_general_ci"


class Config(object):
    DEBUG = False

    SECRET_KEY = os.environ.get("SECRET_KEY")
    CSRF_ENABLED = os.environ.get("CSRF_ENABLED", True)
    CORS_HEADERS = os.environ.get("CORS_HEADERS")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = SECRET_KEY

    SWAGGER = {"title": "Onisep_User API", "uiversion": "3", "version": "1.0.4"}


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_db_dev_uri()


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = get_db_prod_uri()
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 10,
        "max_overflow": 20,
    }
