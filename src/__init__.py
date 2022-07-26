from flask import Flask, jsonify
import os
from flask_jwt_extended import JWTManager
from flasgger import swag_from, Swagger
from flask_migrate import Migrate

from src.auth import auth
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.favoris import favoris
from src.db import db
from src.config.swagger import template, swagger_config


def create_app(test_config=None):

    app = Flask(
        __name__,
        instance_relative_config=True
    )

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            SWAGGER={
                "title": "Onisep_User API",
                "uiversion": 3,
            }
        )

    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    Migrate().init_app(app, db)

    JWTManager(app)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error": "404 not found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({"error": "Something went wrong, we are working on it"}), HTTP_500_INTERNAL_SERVER_ERROR

    app.register_blueprint(auth)
    app.register_blueprint(favoris)

    Swagger(app, config=swagger_config, template=template)

    return app
