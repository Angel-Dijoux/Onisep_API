from typing import Callable
from flask import Blueprint, jsonify
from flasgger import swag_from
from enum import Enum
from loguru import logger

from src.constants.http_status_codes import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"


def route_handler(
    blueprint: Blueprint, route: str, method: HttpMethod, swag_yaml: str = None
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @ swag_from(swag_yaml) if swag_yaml else lambda: None
        def inner_wrapper(*args, **kwargs):
            try:
                return jsonify(func(*args, **kwargs)), HTTP_200_OK
            except Exception as e:
                logger.warning(f"Error in {func.__name__}: {str(e)}")
                return "", HTTP_500_INTERNAL_SERVER_ERROR

        # Define a unique endpoint function name based on the route and method
        endpoint_name = f"{func.__name__}_{method.value}_{route.replace('/', '_')}"
        blueprint.add_url_rule(
            route, endpoint_name, inner_wrapper, methods=[method.value]
        )

        return inner_wrapper

    return decorator
