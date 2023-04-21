from flask import Blueprint, jsonify, Response
from flasgger import swag_from
import json
from typing import Any


from src.constants.http_status_codes import (
    HTTP_200_OK,
)

formations = Blueprint("formations", __name__, url_prefix="/api/v1/formations")


def filter_by_link(formations: list[dict[str, Any]], id: str) -> list[dict[str, Any]]:
    return list(filter(lambda f: f["identifiant"] == id, formations))


@formations.route("/<string:id>")
def get_formation_by_id(id: str) -> "Response":
    with open("assets/formation/data.json", "r") as json_file:
        data = json.load(json_file)
    return jsonify(filter_by_link(data["formations"]["formation"], id)), HTTP_200_OK
