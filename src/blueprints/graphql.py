from flask import Blueprint, Response, jsonify
from strawberry.flask.views import GraphQLView

from src.constants.http_status_codes import HTTP_200_OK

from src.api.schema import schema

graphql = Blueprint("graphql", __name__, url_prefix="/api/graphql")


@graphql.route("/", methods=["POST", "GET"])
def gql() -> tuple[Response, int]:
    view = GraphQLView.as_view("graphql_view", schema=schema)
    return view()
