from flask import Blueprint, jsonify, request
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


@favoris.route("/", methods=["POST", "GET"])
@jwt_required()
@swag_from("../docs/favoris/favoris.yaml")
def handle_favoris():
    current_user = get_jwt_identity()
    # Register a favoris
    if request.method == "POST":
        # Collect informations
        code_nsf = request.get_json().get("code_nsf", "")
        sigle_type_formation = request.get_json().get("sigle_type_formation", "")
        libelle_type_formation = request.get_json().get("libelle_type_formation", "")
        libelle_formation_principal = request.get_json().get(
            "libelle_formation_principal", ""
        )
        sigle_formation = request.get_json().get("sigle_formation", "")
        duree = request.get_json().get("duree", "")
        niveau_de_sortie_indicatif = request.get_json().get(
            "niveau_de_sortie_indicatif", ""
        )
        code_rncp = request.get_json().get("code_rncp", "")
        niveau_de_certification = request.get_json().get("niveau_de_certification", "")
        libelle_niveau_de_certification = request.get_json().get(
            "libelle_niveau_de_certification", ""
        )
        tutelle = request.get_json().get("tutelle", "")
        url_et_id_onisep = request.get_json().get("url_et_id_onisep", "")

        if not validators.url(url_et_id_onisep):
            return jsonify({"error": "Enter valid url"}), HTTP_400_BAD_REQUEST

        favoris = Favori.query.filter_by(request_user_id=current_user)

        data = []

        for item in favoris:
            data.append(item.url_et_id_onisep)
        # Verify if is register in database for this user
        if url_et_id_onisep in data:
            return jsonify({"error": "URL already exists"}), HTTP_409_CONFLICT

        favori = Favori(
            code_nsf=code_nsf,
            sigle_type_formation=sigle_type_formation,
            libelle_type_formation=libelle_type_formation,
            libelle_formation_principal=libelle_formation_principal,
            sigle_formation=sigle_formation,
            duree=duree,
            niveau_de_sortie_indicatif=niveau_de_sortie_indicatif,
            code_rncp=code_rncp,
            niveau_de_certification=niveau_de_certification,
            libelle_niveau_de_certification=libelle_niveau_de_certification,
            tutelle=tutelle,
            url_et_id_onisep=url_et_id_onisep,
            request_user_id=current_user,
        )

        db.session.add(favori)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": favori.id,
                    "code_nsf": favori.code_nsf,
                    "sigle_type_formation": favori.sigle_type_formation,
                    "libelle_type_formation": favori.libelle_type_formation,
                    "libelle_formation_principal": favori.libelle_formation_principal,
                    "sigle_formation": favori.sigle_formation,
                    "duree": favori.duree,
                    "niveau_de_sortie_indicatif": favori.niveau_de_sortie_indicatif,
                    "code_rncp": favori.code_rncp,
                    "niveau_de_certification": favori.niveau_de_certification,
                    "libelle_niveau_de_certification": favori.libelle_niveau_de_certification,
                    "tutelle": favori.tutelle,
                    "url_et_id_onisep": favori.url_et_id_onisep,
                    "user_id": favori.request_user_id,
                }
            ),
            HTTP_201_CREATED,
        )
    # Get favoris for this user
    else:
        favoris = Favori.query.filter_by(request_user_id=current_user)

        data = []

        count_item = 0
        for item in favoris:
            count_item += 1
            data.append(
                {
                    "id": item.id,
                    "code_nsf": item.code_nsf,
                    "sigle_type_formation": item.sigle_type_formation,
                    "libelle_type_formation": item.libelle_type_formation,
                    "libelle_formation_principal": item.libelle_formation_principal,
                    "sigle_formation": item.sigle_formation,
                    "duree": item.duree,
                    "niveau_de_sortie_indicatif": item.niveau_de_sortie_indicatif,
                    "code_rncp": item.code_rncp,
                    "niveau_de_certification": item.niveau_de_certification,
                    "libelle_niveau_de_certification": item.libelle_niveau_de_certification,
                    "tutelle": item.tutelle,
                    "url_et_id_onisep": item.url_et_id_onisep,
                }
            )

        return jsonify({"size": count_item, "results": data}), HTTP_200_OK


# Remove_favoris function need JWT token and delete favoris for this user


@favoris.delete("/<int:id>")
@jwt_required()
@swag_from("../docs/favoris/remove.yaml")
def remove_favori(id):
    current_user = get_jwt_identity()

    favori = Favori.query.filter_by(request_user_id=current_user, id=id).first()

    if not favori:
        return jsonify({"message": "Item not found"}), HTTP_404_NOT_FOUND

    db.session.delete(favori)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
