from src import db


class Favori(db.Model):
    __tablename__ = "favori"

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

    def __repr__(self) -> str:
        return "Favori>>> {self.onisep_url}"
