from flask import Response


def add_security_headers(response: Response) -> Response:
    response.headers.add("X-Content-Type-Options", "nosniff")
    response.headers.add(
        "Strict-Transport-Security", "max-age=86400; includeSubDomains"
    )
    response.headers.add("X-Frame-Options", "deny")
    response.headers.add("Access-Control-Allow-Methods", ["GET", "POST", "DELETE"])
    response.headers.add("X-XSS-Protection", "1; mode=block")
    response.headers.set("Server", "Jojo's")

    return response


def after_request(response: Response) -> Response:
    return add_security_headers(response)
