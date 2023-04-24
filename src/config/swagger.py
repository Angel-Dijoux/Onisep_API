from src.constants.env import is_dev

from config import ProductionConfig

template = {
    "swagger": "2.0",
    "info": {
        "title": ProductionConfig.SWAGGER["title"],
        "description": "API for user want register onisep formation",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "angel.dijoux@yahoo.com",
            "url": "https://twitter.com/Elki_YT",
        },
        "termsOfService": "https://twitter.com/Elki_YT",
        "version": ProductionConfig.SWAGGER["version"],
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": ["http" if is_dev else "https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"',
        }
    },
}

swagger_config = {
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
