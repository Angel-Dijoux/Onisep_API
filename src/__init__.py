from flask import Flask, jsonify
import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from src.constants.http_status_codes import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from src.config.swagger import template, swagger_config

from config import DevelopmentConfig, ProductionConfig

db = SQLAlchemy()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, instance_relative_config=True)

    if os.environ.get("ENV") == "production":
        config_class = ProductionConfig

    app.config.from_object(config_class)
    CORS(app)
    db.init_app(app)
    Migrate().init_app(app, db)
    JWTManager(app)

    with app.app_context():
        register_blueprints(app)

    @app.after_request
    def after_request(response):
        response.headers.add("X-Content-Type-Options", "nosniff")
        response.headers.add(
            "Strict-Transport-Security", "max-age=86400; includeSubDomains"
        )
        response.headers.add("X-Frame-Options", "deny")
        response.headers.add("Access-Control-Allow-Methods", ["GET", "POST", "DELETE"])
        response.headers.add("X-XSS-Protection", "1; mode=block")
        response.headers.set("Server", "Jojo's")

        return response

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error": "404 not found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return (
            jsonify({"error": "Something went wrong, we are working on it"}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )

    Swagger(app, config=swagger_config, template=template)

    return app


def register_blueprints(app: Flask):
    from src.blueprints.favoris import favoris
    from src.blueprints.formations import formations
    from src.blueprints.auth import auth

    app.register_blueprint(auth)
    app.register_blueprint(favoris)
    app.register_blueprint(formations)
