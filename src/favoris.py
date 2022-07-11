from flask import Blueprint, jsonify, request
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from flasgger import swag_from

from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from src.db import Favori, db

favoris = Blueprint("favoris", __name__, url_prefix="/api/v1/favoris")


@favoris.route('/', methods=['POST', 'GET'])
@jwt_required()
@swag_from('./docs/favoris/favoris.yaml')
def handle_favoris():
    current_user = get_jwt_identity()

    if request.method == "POST":

        onisep_url = request.get_json().get('onisep_url', '')

        if not validators.url(onisep_url):
            return jsonify({
                "error": "Enter valid url"
            }), HTTP_400_BAD_REQUEST

        favoris = Favori.query.filter_by(request_user_id=current_user)

        data = []

        for item in favoris:
            data.append(item.onisep_url)

        if onisep_url in data:
            return jsonify({
                "error": "URL already exists"
            }), HTTP_409_CONFLICT

        favori = Favori(onisep_url=onisep_url, request_user_id=current_user)
        db.session.add(favori)
        db.session.commit()

        return jsonify({
            "id": favori.id,
            "onisep_url": favori.onisep_url,
            "user_id": favori.request_user_id
        }), HTTP_201_CREATED

    else:

        favoris = Favori.query.filter_by(request_user_id=current_user)

        data = []

        for item in favoris:
            data.append({
                "id": item.id,
                "onisep_url": item.onisep_url,
            })

        return jsonify({"data": data}), HTTP_200_OK


@favoris.delete("/<int:id>")
@jwt_required()
@swag_from('./docs/favoris/remove.yaml')
def remove_favori(id):
    current_user = get_jwt_identity()

    favori = Favori.query.filter_by(
        request_user_id=current_user, id=id).first()

    if not favori:
        return jsonify({"message": "Item not found"}), HTTP_404_NOT_FOUND

    db.session.delete(favori)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
