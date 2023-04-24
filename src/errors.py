from flask import jsonify, Flask
from werkzeug.exceptions import HTTPException


def handle_404(e: HTTPException) -> tuple:
    return jsonify({"error": "404 not found"}), e


def handle_500(e: Exception) -> tuple:
    return (
        jsonify({"error": "Something went wrong, we are working on it"}),
        e,
    )


def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(HTTPException, handle_404)
    app.register_error_handler(Exception, handle_500)
