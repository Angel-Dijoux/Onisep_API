from datetime import datetime
from src.business_logic.favoris.is_favorite import check_if_is_favorite
from src.business_logic.formation.scrap.types import (
    FormationIsFavorite,
)
from src.models.formation import Formation


def _create_formation_from_dict(formation: dict) -> Formation:
    return Formation(
        code_nsf=int(formation.get("code_nsf") or 0),
        type=formation.get("sigle_type_formation")
        or formation.get("libelle_type_formation"),
        libelle=formation.get("libelle_formation_principal"),
        tutelle=formation.get("tutelle"),
        url=formation.get("url_et_id_onisep"),
        domain=formation.get("domainesous-domaine"),
        niveau_de_sortie=formation.get("niveau_de_sortie_indicatif"),
        duree=formation.get("duree"),
        created_at=datetime.strptime("01/01/2024", "%m/%d/%Y").date(),
        updated_at=datetime.strptime("01/01/2024", "%m/%d/%Y").date(),
    )


def format_formations(data: list[dict]) -> list[Formation]:
    return [
        FormationIsFavorite(
            formation=_create_formation_from_dict(formation).to_dict(),
            is_favorite=False,
        )
        for formation in data
    ]


def format_formation_with_is_favorite(
    user_id: int, data: list[dict]
) -> list[FormationIsFavorite]:
    return [
        FormationIsFavorite(
            formation=_create_formation_from_dict(formation).to_dict(),
            is_favorite=check_if_is_favorite(user_id, formation["url_et_id_onisep"]),
        )
        for formation in data
    ]
