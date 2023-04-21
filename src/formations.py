from flask import Blueprint, jsonify, Response
from flasgger import swag_from
import json
from typing import Any


from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

formations = Blueprint("formations", __name__, url_prefix="/api/v1/formations")


def filter_by_link(formations: list[dict[str, Any]], id: str) -> dict[str, Any]:
    filtered_list = list(filter(lambda f: f["identifiant"] == id, formations))
    return filtered_list[0] if filtered_list else []


@formations.route("/<string:id>")
@swag_from("./docs/formations/formation.yaml")
def get_formation_by_id(id: str) -> "Response":
    print(id)
    try:
        with open("assets/formation/data.json", "r") as json_file:
            result = filter_by_link(json.load(json_file)["formations"]["formation"], id)
        return jsonify(result), HTTP_200_OK if len(result) > 0 else HTTP_404_NOT_FOUND
    except Exception:
        print("Error in get_formation_by_id : ", Exception)
        return HTTP_500_INTERNAL_SERVER_ERROR
