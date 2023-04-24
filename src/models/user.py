from src import db

# Create User row


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    pdp_url = db.Column(db.Text)
    favoris = db.relationship("Favori", backref="user")

    def __repr__(self) -> str:
        return "User>>> {self.username}"
