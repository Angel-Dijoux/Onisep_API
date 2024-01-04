from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from src.models.formation import Formation
from src.models.user import User
from src.models.user_favori import UserFavori


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("created_at", "updated_at", "password")


class FormationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Formation
        include_relationships = True


class UserFavoriSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserFavori

    formation = fields.Nested(FormationSchema)
    users = fields.Nested(UserSchema)
