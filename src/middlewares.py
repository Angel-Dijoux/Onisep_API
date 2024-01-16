from flask import Response

from src.constants.env import is_dev


def add_security_headers(response: Response) -> Response:
    response.headers.add("X-Content-Type-Options", "nosniff")
    response.headers.add(
        "Strict-Transport-Security", "max-age=86400; includeSubDomains"
    )
    response.headers.add("X-Frame-Options", "deny")
    response.headers.add(
        "Access-Control-Allow-Methods", ",".join(["GET", "POST", "DELETE"])
    )
    response.headers.add(
        "Access-Control-Allow-Origin",
        "".join(
            ["http://127.0.0.1:5005" if is_dev() else "https://api.nc-elki.v6.army"]
        ),
    )
    response.headers.add("Access-Control-Allow-Headers", "Authorization, Content-Type")
    response.headers.add("Access-Control-Max-Age", "1728000")
    response.headers.add("X-XSS-Protection", "1; mode=block")
    response.headers.set("Server", "Jojo's")

    return response


def after_request(response: Response) -> Response:
    return add_security_headers(response)
