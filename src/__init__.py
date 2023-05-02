from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .middlewares import after_request
from .errors import register_error_handlers

from src.config.swagger import template, swagger_config

from config import DevelopmentConfig, ProductionConfig

from src.constants.env import is_dev

db = SQLAlchemy()


def create_app(config_class=DevelopmentConfig):
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
    from src.blueprints.favoris import favoris
    from src.blueprints.formations import formations
    from src.blueprints.auth import auth
    from src.blueprints.utils import utils

    app.register_blueprint(utils)
    app.register_blueprint(auth)
    app.register_blueprint(favoris)
    app.register_blueprint(formations)
