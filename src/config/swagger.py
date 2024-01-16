from src.constants.env import is_dev
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from config import Config


def get_swagger_api_spec(
    config: Config, plugins: list[FlaskPlugin | MarshmallowPlugin]
) -> APISpec:
    info = {
        **config.SWAGGER,
        "description": "API for user registration on Onisep formation",
        "termsOfService": "/privacy_policy",
        "contact": {
            "email": "angel.dijoux@yahoo.com",
            "url": "https://github.com/Angel-Dijoux",
        },
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    }
    spec = APISpec(
        title=config.SWAGGER["title"],
        version=config.SWAGGER["version"],
        openapi_version="2.0",
        plugins=plugins,
        info=info,
    )
    api_key_scheme = {"type": "apiKey", "in": "header", "name": "Authorization"}
    spec.components.security_scheme("Bearer", api_key_scheme)
    return spec


swagger_config = {
    "host": ["localhost:5005" if is_dev() else "api.nc-elki.v6.army"],
    "schemes": ["http" if is_dev() else "https"],
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/",
}
