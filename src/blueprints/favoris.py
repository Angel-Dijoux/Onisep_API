from flask import Blueprint, jsonify, request, Response, abort
from sqlalchemy import and_, exists
from werkzeug.exceptions import HTTPException
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from flasgger import swag_from

from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from src import db
from src.models import UserFavori

from typing import Tuple

from src.models.formation import Formation

favoris = Blueprint("favoris", __name__, url_prefix="/api/v1/favoris")


def _create_new_formation(favori: dict) -> Formation:
    formation = Formation(**favori)
    db.session.add(formation)
    db.session.flush()
    return formation


@favoris.route("/", methods=["POST"])
@jwt_required()
@swag_from("../docs/favoris/postFavoris.yaml")
def post_favori_by_user_id() -> Tuple[Response, int] | HTTPException:
    current_user = get_jwt_identity()

    favori_data = request.get_json()
    url = favori_data.get("url", "")

    if not validators.url(url):
        abort(HTTP_400_BAD_REQUEST, "Enter a valid URL")

    formation = Formation.query.filter(Formation.url == url).first()

    if formation is None:
        formation = _create_new_formation(favori_data)

    favori_exist = db.session.query(
        exists().where(
            and_(
                UserFavori.user_id == current_user,
                UserFavori.formation_id == formation.id,
            )
        )
    ).scalar()

    if favori_exist:
        abort(HTTP_409_CONFLICT, "URL already exists")

    favori = UserFavori(formation_id=formation.id, user_id=current_user)
    db.session.add(favori)
    db.session.commit()

    return jsonify(favori), HTTP_201_CREATED


@favoris.route("/", methods=["GET"])
@jwt_required()
@swag_from("../docs/favoris/getFavoris.yaml")
def get_favoris_by_user_id() -> Tuple[Response, int]:
    current_user = get_jwt_identity()
    favoris = (
        UserFavori.query.filter(UserFavori.request_user_id == current_user)
        .order_by(UserFavori.created_at.asc())
        .all()
    )
    return jsonify({"size": len(favoris), "results": favoris}), HTTP_200_OK


# Remove_favoris function need JWT token and delete favoris for this user


@favoris.route("/favori_ids")
@jwt_required()
def get_favoris_ids() -> Tuple[Response, int]:
    current_user = get_jwt_identity()
    result = (
        UserFavori.query.with_entities(UserFavori.url_et_id_onisep, UserFavori.id)
        .filter(UserFavori.request_user_id == current_user)
        .all()
    )
    favori_data = [{"id": row.id, "url": row.url_et_id_onisep} for row in result]
    return jsonify({"favori_ids": favori_data}), HTTP_200_OK


@favoris.delete("/<int:id>")
@jwt_required()
@swag_from("../docs/favoris/remove.yaml")
def remove_favori(id: int) -> Tuple[Response, int] | HTTPException:
    current_user = get_jwt_identity()

    favori = UserFavori.query.filter_by(request_user_id=current_user, id=id).first()

    if not favori:
        abort(HTTP_404_NOT_FOUND, "Favoris not found")

    db.session.delete(favori)
    db.session.commit()

    return jsonify({}), HTTP_200_OK
