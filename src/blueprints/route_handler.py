from http.client import HTTPException
from typing import Callable
from flask import Blueprint, jsonify
from flasgger import swag_from
from enum import Enum
import jwt
from loguru import logger

from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


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
        @swag_from(swag_yaml if swag_yaml else lambda: None)
        def inner_wrapper(*args, **kwargs):
            try:
                return jsonify(func(*args, **kwargs)), HTTP_200_OK
            except jwt.ExpiredSignatureError as e:
                # Handle JWT token expiration: return 401 Unauthorized
                logger.warning(f"Expired JWT token in {func.__name__}: {str(e)}")
                return "", HTTP_401_UNAUTHORIZED
            except HTTPException as e:
                # Handle other HTTP exceptions
                logger.warning(f"HTTPException in {func.__name__}: {str(e)}")
                return "", e.code
            except Exception as e:
                # Handle generic exceptions
                logger.warning(f"Error in {func.__name__}: {str(e)}")
                return "", HTTP_500_INTERNAL_SERVER_ERROR

        # Define a unique endpoint function name based on the route and method
        endpoint_name = f"{func.__name__}_{method.value}_{route.replace('/', '_')}"
        blueprint.add_url_rule(
            route, endpoint_name, inner_wrapper, methods=[method.value]
        )

        return inner_wrapper

    return decorator
