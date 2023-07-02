from dataclasses import dataclass
from src import db
from src.models.base_model import BaseModel


@dataclass
class Favori(BaseModel):
    __tablename__ = "favori"

    id: int
    code_nsf: str
    sigle_type_formation: str
    libelle_type_formation: str
    libelle_formation_principal: str
    sigle_formation: str
    duree: str
    niveau_de_sortie_indicatif: str
    code_rncp: str
    niveau_de_certification: str
    libelle_niveau_de_certification: str
    tutelle: str
    url_et_id_onisep: str
    request_user_id: int

    id = db.Column(db.Integer, primary_key=True)
    code_nsf = db.Column(db.Text)
    sigle_type_formation = db.Column(db.Text)
    libelle_type_formation = db.Column(db.Text)
    libelle_formation_principal = db.Column(db.Text)
    sigle_formation = db.Column(db.Text)
    duree = db.Column(db.Text)
    niveau_de_sortie_indicatif = db.Column(db.Text)
    code_rncp = db.Column(db.Text)
    niveau_de_certification = db.Column(db.Text)
    libelle_niveau_de_certification = db.Column(db.Text)
    tutelle = db.Column(db.Text)
    url_et_id_onisep = db.Column(db.Text, nullable=False)
    request_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
