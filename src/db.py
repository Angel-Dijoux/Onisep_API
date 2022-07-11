from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    favoris = db.relationship('Favori', backref="user")

    def __repr__(self) -> str:
        return 'User>>> {self.username}'


class Favori(db.Model):
    __tablename__ = 'favori'

    id = db.Column(db.Integer, primary_key=True)
    onisep_url = db.Column(db.Text, nullable=False)
    request_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return 'Favori>>> {self.onisep_url}'
