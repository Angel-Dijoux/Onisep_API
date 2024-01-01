from flask import Blueprint, render_template


legal = Blueprint("legal", __name__, template_folder="templates")


@legal.route("/privacy_policy")
def privacy_policy():
    return render_template("privacy_policy.html.jinja")
