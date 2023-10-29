import json
from typing import Any, Tuple

from flask import Blueprint, Response, request
from werkzeug.exceptions import HTTPException

from src.blueprints.route_handler import HttpMethod, route_handler
from src.business_logic.formation.scrap.get_formation import (
    get_libelle_type_formation,
    search_formations,
)
from src.constants.http_status_codes import (
    HTTP_200_OK,
)
from src.models.user_favori import UserFavori
from src.models.user import User

from src import db

formations = Blueprint("formations", __name__, url_prefix="/api/v1/formations")


def _filter_by_link(formations: list[dict[str, Any]], for_id: str) -> dict[str, Any]:
    filtered_list = list(filter(lambda f: f["identifiant"] == for_id, formations))
    return filtered_list[0] if filtered_list else {}


@route_handler(
    formations,
    "/<string:id>",
    HttpMethod.GET,
    "../docs/formations/formation.yaml",
)
def get_formation_by_id(id: str) -> Tuple[Response, int] | HTTPException:
    new_user = User(
        username="john_tt",
        password="password",
        email="john@hey.com",
        profile_pic_url="profile.jpg",
    )

    db.session.add(new_user)
    db.session.flush()

    # Create a UserFavori object
    new_favori = UserFavori(
        code_nsf="123",
        sigle_type_formation="ABC",
        libelle_type_formation="Type ABC",
        libelle_formation_principal="Main Formation",
        sigle_formation="Formation ABC",
        duree="12 months",
        niveau_de_sortie_indicatif="Intermediate",
        code_rncp="456",
        niveau_de_certification="Certified",
        libelle_niveau_de_certification="Certification ABC",
        tutelle="Example Tutelle",
        url_et_id_onisep="https://example.com/2",
        request_user_id=new_user.id,  # Assign the user object to the UserFavori
    )
    db.session.add(new_favori)
    db.session.commit()

    with open("assets/formation/data.json", "r") as json_file:
        result = _filter_by_link(json.load(json_file)["formations"]["formation"], id)
    return result, HTTP_200_OK if len(result) > 0 else HTTP_200_OK


@route_handler(
    formations,
    "/search",
    HttpMethod.POST,
    "../docs/formations/searchFormation.yaml",
)
def get_search_formation() -> Tuple[Response, int] | HTTPException:
    post = request.get_json()
    query = post.get("query")
    limit = post.get("limit")
    offset = post.get("offset")

    return search_formations(query, limit, offset)


@route_handler(
    formations,
    "/formation_by_libelle",
    HttpMethod.POST,
    "../docs/formations/formationByLibelle.yaml",
)
def get_formation_by_libelle() -> Tuple[Response, int] | HTTPException:
    post = request.get_json()
    query = post.get("query")

    return get_libelle_type_formation(query)
