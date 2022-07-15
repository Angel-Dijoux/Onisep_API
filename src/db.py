from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    pdp_url = db.Column(db.Text)
    favoris = db.relationship('Favori', backref="user")

    def __repr__(self) -> str:
        return 'User>>> {self.username}'


class Favori(db.Model):
    __tablename__ = 'favori'

    id = db.Column(db.Integer, primary_key=True)
    code_nsf = db.Column(db.Integer)
    sigle_type_formation = db.Column(db.Text)
    libelle_type_formation = db.Column(db.Text)
    libelle_formation_principal = db.Column(db.Text)
    sigle_formation = db.Column(db.Text)
    duree = db.Column(db.Text)
    niveau_de_sortie_indicatif = db.Column(db.Text)
    code_rncp = db.Column(db.Integer)
    niveau_de_certification = db.Column(db.Text)
    libelle_niveau_de_certification = db.Column(db.Text)
    tutelle = db.Column(db.Text)
    url_et_id_onisep = db.Column(db.Text, nullable=False)
    request_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return 'Favori>>> {self.onisep_url}'
