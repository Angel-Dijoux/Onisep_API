from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

from src import db
from src.business_logic.favoris.delete_favoris_for_one_user import (
    delete_favoris_for_one_user,
)
from src.business_logic.user.exceptions import AuthenticationException
from src.business_logic.user.validate_user import validate_user


class DeleteUserForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])


legal = Blueprint("legal", __name__, template_folder="templates")


@legal.route("/privacy_policy")
def privacy_policy():
    return render_template("privacy_policy.html.jinja")


@legal.route("/me/delete", methods=["GET", "POST"])
def delete_my_account():
    form = DeleteUserForm()
    try:
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = validate_user(email, password)

            delete_favoris_for_one_user(user.id)

            db.session.delete(user)
            db.session.commit()

            return render_template("delete_successfully.html.jinja", name=email)
    except AuthenticationException as e:
        return render_template("error.html.jinja", error=str(e))
    return render_template("delete_me.html.jinja", form=form)
