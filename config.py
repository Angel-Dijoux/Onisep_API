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

    API_VERSION = "1.0.5"

    SWAGGER = {"title": "Onisep Explorer", "uiversion": "3", "version": API_VERSION}


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_db_dev_uri()

    SWAGGER = {
        "title": "Onisep Explorer DEV",
        "uiversion": "3",
        "version": Config.API_VERSION,
    }


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = get_db_prod_uri()
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 10,
        "max_overflow": 20,
    }


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "test"
    JWT_SECRET_KEY = "test"
    ENABLE_SEMANTIC_SEARCH = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI_TESTING",
        "mysql+mysqlconnector://root:@/onisep_testing?charset=utf8mb4&collation=utf8mb4_general_ci",
    )


def load_config(env: str) -> Config:
    config_switch = {
        "production": ProductionConfig,
        "testing": TestingConfig,
        "development": DevelopmentConfig,
    }

    config = config_switch.get(env, DevelopmentConfig)
    config.ENV = env

    return config
