from flask import Blueprint, jsonify, request, Response, Literal
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from flasgger import swag_from

from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from src import db
from src.models import Favori

favoris = Blueprint("favoris", __name__, url_prefix="/api/v1/favoris")


@favoris.route("/", methods=["POST"])
@jwt_required()
@swag_from("../docs/favoris/postFavoris.yaml")
def post_favori_by_user_id() -> Response | Literal:
    current_user = get_jwt_identity()
    # Collect informations
    favori_data = request.get_json()
    if not validators.url(favori_data.get("url_et_id_onisep", "")):
        return jsonify({"error": "Enter valid url"}), HTTP_400_BAD_REQUEST

    if Favori.query.filter_by(
        request_user_id=current_user,
        url_et_id_onisep=favori_data.get("url_et_id_onisep", ""),
    ).first():
        return jsonify({"error": "URL already exists"}), HTTP_409_CONFLICT
    favori = Favori(**favori_data, request_user_id=current_user)
    db.session.add(favori)
    db.session.commit()
    return (
        jsonify(favori),
        HTTP_201_CREATED,
    )


@favoris.route("/", methods=["GET"])
@jwt_required()
@swag_from("../docs/favoris/getFavoris.yaml")
def get_favoris_by_user_id() -> Response | Literal:
    current_user = get_jwt_identity()
    favoris = Favori.query.filter_by(request_user_id=current_user).all()
    return jsonify({"size": len(favoris), "results": favoris}), HTTP_200_OK


# Remove_favoris function need JWT token and delete favoris for this user


@favoris.delete("/<int:id>")
@jwt_required()
@swag_from("../docs/favoris/remove.yaml")
def remove_favori(id: int) -> Response | Literal:
    current_user = get_jwt_identity()

    favori = Favori.query.filter_by(request_user_id=current_user, id=id).first()

    if not favori:
        return jsonify({"message": "Item not found"}), HTTP_404_NOT_FOUND

    db.session.delete(favori)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
