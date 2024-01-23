import os
import sys

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

from config import load_config

from .errors import register_error_handlers
from .middlewares import after_request

db: SQLAlchemy = SQLAlchemy()
plugins = [
    FlaskPlugin(),
    MarshmallowPlugin(),
]


def create_app(environment=None):
    _setup_logging()
    env = environment or os.environ.get("ENV")
    config = load_config(env)
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config)
    CORS(app)
    db.init_app(app)
    Migrate().init_app(app, db)
    JWTManager(app)

    with app.app_context():
        register_blueprints(app)

    app.after_request(after_request)
    register_error_handlers(app)

    return app


def register_blueprints(app: Flask):
    from src.blueprints.home import home
    from src.blueprints.auth import auth
    from src.blueprints.favoris import favoris
    from src.blueprints.formations import formations
    from src.blueprints.graphql import graphql
    from src.blueprints.legal.views import legal
    from src.blueprints.utils import utils

    app.register_blueprint(home)
    app.register_blueprint(utils)
    app.register_blueprint(auth)
    app.register_blueprint(legal)
    app.register_blueprint(favoris)
    app.register_blueprint(formations)
    app.register_blueprint(graphql)


def _set_log_levels():
    log_levels = {
        "INFO": "<green>",
        "DEBUG": "<blue>",
        "WARNING": "<yellow>",
        "ERROR": "<red>",
        "CRITICAL": "<red>",
    }
    [logger.level(level, color=color) for level, color in log_levels.items()]


def _add_stderr_logger():
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


def _setup_logging():
    logger.remove()
    _set_log_levels()
    _add_stderr_logger()
