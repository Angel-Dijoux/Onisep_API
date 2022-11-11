template = {
    "swagger": "2.0",
    "info": {
        "title": "Onisep_User API",
        "description": "API for user want register onisep formation",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "angel.dijoux@yahoo.com",
            "url": "https://twitter.com/Elki_YT",
        },
        "termsOfService": "https://twitter.com/Elki_YT",
        "version": "1.0.3"
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}
