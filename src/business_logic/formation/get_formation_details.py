from dataclasses import dataclass
from datetime import date
import json
from typing import Any, Optional
from src.business_logic.formation.exceptions import ProcessFormationException
from src.business_logic.formation.job.get_job_by_formation import Job, process_jobs
from src.business_logic.formation.parcoursup.get_parcoursup_expectations import (
    get_parcoursup_expectations,
)

from src.business_logic.formation.parcoursup.helper.html_parser import (
    ParcourSupExpectations,
)
from src.business_logic.formation.study.get_continuation_of_study import (
    ContinuationOfStudies,
    process_continuation_studies,
)


@dataclass
class FormationDetail:
    id: str
    exceptions: Optional[ParcourSupExpectations]
    duree: str
    libelle: str
    tutelle: str
    certificat: str
    sigle: Optional[str]
    type: str
    jobs: Optional[list[Job]]
    continuation_studies: Optional[ContinuationOfStudies]
    updated_at: date


def _filter_by_link(formations: list[dict[str, Any]], for_id: str) -> dict[str, Any]:
    filtered_list = list(filter(lambda f: f["identifiant"] == for_id, formations))
    return filtered_list[0] if filtered_list else {}


def _read_json_formation(for_id: str) -> Optional[dict[str, Any]]:
    with open("assets/formation/data.json", "r") as json_file:
        result = _filter_by_link(
            json.load(json_file)["formations"]["formation"], for_id
        )
    return result if len(result) > 0 else None


def _process_formation(for_id: str) -> FormationDetail:
    formation = _read_json_formation(for_id)

    if formation:
        identifiant = formation["identifiant"]

        attendus = formation["attendus"]
        exceptions = get_parcoursup_expectations(attendus if attendus else None)

        duree = formation["duree_formation"]
        libelle = formation["libelle_complet"]
        tutelle = formation["sous_tutelle"]
        certificat = formation["nature_certificat"]["libelle_nature_certificat"]
        sigle = formation["sigle"] if formation["sigle"] else None
        type_sigle = formation["type_Formation"]["type_formation_sigle"]

        metier = formation["metiers_formation"]["metier"]
        jobs = process_jobs(metier if metier else None)

        poursuite_etudes = formation["poursuites_etudes"]
        continuation_studies = process_continuation_studies(
            poursuite_etudes if poursuite_etudes else None
        )
        updated_at = formation["modification_date"]
        return FormationDetail(
            id=identifiant,
            exceptions=exceptions,
            duree=duree,
            libelle=libelle,
            tutelle=tutelle,
            certificat=certificat,
            sigle=sigle,
            type=type_sigle,
            jobs=jobs,
            continuation_studies=continuation_studies,
            updated_at=updated_at,
        )


def get_formation_by_id(for_id: str) -> FormationDetail:
    try:
        return _process_formation(for_id)
    except Exception as e:
        raise ProcessFormationException(
            "Error during formation processing : " + e
        ) from e
