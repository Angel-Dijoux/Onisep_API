import sys

from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

from config import DevelopmentConfig, ProductionConfig
from src.config.swagger import swagger_config, template
from src.constants.env import is_dev

from .errors import register_error_handlers
from .middlewares import after_request

db = SQLAlchemy()


def create_app(config_class=DevelopmentConfig):
    _setup_logging()
    app = Flask(__name__, instance_relative_config=True)

    if not is_dev():
        config_class = ProductionConfig

    app.config.from_object(config_class)
    CORS(app)
    db.init_app(app)
    Migrate().init_app(app, db)
    JWTManager(app)

    with app.app_context():
        register_blueprints(app)

    app.after_request(after_request)
    register_error_handlers(app)

    Swagger(app, config=swagger_config, template=template)
    return app


def register_blueprints(app: Flask):
    from src.blueprints.auth import auth
    from src.blueprints.favoris import favoris
    from src.blueprints.formations import formations
    from src.blueprints.utils import utils

    app.register_blueprint(utils)
    app.register_blueprint(auth)
    app.register_blueprint(favoris)
    app.register_blueprint(formations)


def _setup_logging():
    logger.remove()
    logger.level("INFO", color="<green>")
    logger.level("DEBUG", color="<blue>")
    logger.level("WARNING", color="<yellow>")
    logger.level("ERROR", color="<red>")
    logger.level("CRITICAL", color="<red>")
    logger.add(
        sys.stderr,
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> | "
            "{extra}"
        ),
    )
