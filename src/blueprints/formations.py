import json
from typing import Any, Tuple

from flask import Blueprint, Response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import HTTPException

from src.blueprints.route_handler import HttpMethod, route_handler
from src.business_logic.formation.scrap.get_main_formation import (
    auth_get_main_formations,
    get_main_formations,
)
from src.business_logic.formation.scrap.get_repartition_formations import (
    get_libelle_type_formation,
)
from src.business_logic.formation.scrap.search_formation import (
    auth_search_formations,
    search_formations,
)
from src.constants.http_status_codes import (
    HTTP_200_OK,
)

formations = Blueprint("formations", __name__, url_prefix="/api/v1/formations")


def _filter_by_link(formations: list[dict[str, Any]], for_id: str) -> dict[str, Any]:
    filtered_list = list(filter(lambda f: f["identifiant"] == for_id, formations))
    return filtered_list[0] if filtered_list else {}


@route_handler(formations, "/", HttpMethod.POST)
@jwt_required(optional=True)
def resolve_get_main_formations() -> Tuple[Response, int] | HTTPException:
    data = request.get_json()
    offset = data.get("offset")
    limit = data.get("limit")
    user_id = get_jwt_identity()
    if user_id:
        return auth_get_main_formations(user_id, limit, offset)
    return get_main_formations(limit, offset)


@route_handler(
    formations,
    "/<string:id>",
    HttpMethod.GET,
    "../docs/formations/formation.yaml",
)
def resolve_get_formation_by_id(id: str) -> Tuple[Response, int] | HTTPException:
    with open("assets/formation/data.json", "r") as json_file:
        result = _filter_by_link(json.load(json_file)["formations"]["formation"], id)
    return result, HTTP_200_OK if len(result) > 0 else HTTP_200_OK


@route_handler(
    formations,
    "/search",
    HttpMethod.POST,
    "../docs/formations/searchFormation.yaml",
)
@jwt_required(optional=True)
def resolve_get_search_formation() -> Tuple[Response, int] | HTTPException:
    post = request.get_json()
    query = post.get("query")
    limit = post.get("limit")
    offset = post.get("offset")

    user_id = get_jwt_identity()
    if user_id:
        return auth_search_formations(user_id, query, limit, offset)
    return search_formations(query, limit, offset)


@route_handler(
    formations,
    "/formation_by_libelle",
    HttpMethod.POST,
    "../docs/formations/formationByLibelle.yaml",
)
def resolve_get_formation_by_libelle() -> Tuple[Response, int] | HTTPException:
    data = request.get_json()
    query = data.get("query")

    return get_libelle_type_formation(query)
