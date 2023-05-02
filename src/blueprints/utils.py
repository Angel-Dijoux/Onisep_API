from flask import Blueprint, jsonify, Response
from typing import Tuple

from src.constants.http_status_codes import (
    HTTP_200_OK,
)

utils = Blueprint("utils", __name__, url_prefix="/api/v1")


@utils.route("/")
def ping() -> Tuple[Response, int]:
    return jsonify({"status": "up"}), HTTP_200_OK
