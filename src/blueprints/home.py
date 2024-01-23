from flask import Blueprint, jsonify, Response
from typing import Tuple

from src.constants.http_status_codes import (
    HTTP_200_OK,
)

home = Blueprint("home", __name__, url_prefix="/")


@home.route("/")
def hello() -> Tuple[Response, int]:
    return jsonify({"message": "Hello World"}), HTTP_200_OK
