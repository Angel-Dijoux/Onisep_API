from flask import Blueprint, jsonify, request, Response, abort
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from flasgger import swag_from

from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from src import db
from src.models import User, UserFavori

import re
from typing import Tuple


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

# Register function in "/api/v1/auth/register" with flasgger


@auth.post("/register")
@swag_from("../docs/auth/login/register.yaml")
def register() -> Tuple[Response, int] | HTTPException:
    # Collect informations
    data = request.json
    if data is not None:
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if len(password) < 6 or not re.match(r"^[a-zA-Z0-9]{3,20}$", username):
            abort(HTTP_400_BAD_REQUEST, "Invalid password or username")
        # Verify with "validators" if email is valid
        if not validators.email(email):
            abort(HTTP_409_CONFLICT, "Email is not valid")
        # Verify if email is in database
        if User.query.filter_by(email=email).first() is not None:
            abort(HTTP_409_CONFLICT, "Email is taken")
        # Verify if username is in database
        if User.query.filter_by(username=username).first() is not None:
            abort(HTTP_409_CONFLICT, "username is taken")
        # Hash password
        pwd_hash = generate_password_hash(password)

        user = User(username=username, password=pwd_hash, email=email)
        db.session.add(user)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "User created",
                    "user": user,
                }
            ),
            HTTP_201_CREATED,
        )
    return abort(HTTP_400_BAD_REQUEST, "Invalid request body")


# Login function in "/api/v1/auth/login" with flasgger


@auth.post("/login")
@swag_from("../docs/auth/login/login.yaml")
def login() -> Tuple[Response, int] | HTTPException:
    # Collect informations
    data = request.json
    if data is not None:
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            # Verify if password check with password in database
            is_pass_correct = check_password_hash(user.password, password)

            if is_pass_correct:
                refresh = create_refresh_token(identity=user.id)
                access = create_access_token(identity=user.id)

                return (
                    jsonify(
                        {
                            "user": {
                                "id": user.id,
                                "refresh": refresh,
                                "access": access,
                                "username": user.username,
                                "email": user.email,
                            }
                        }
                    ),
                    HTTP_200_OK,
                )
        abort(HTTP_401_UNAUTHORIZED, "Wrong credendials")
    abort(HTTP_400_BAD_REQUEST, "Invalid request body")


# Me function need JWT token return userInfo


@auth.get("/me")
@jwt_required()
@swag_from("../docs/auth/me.yaml")
def me() -> Tuple[Response, int]:
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return (
        jsonify(user),
        HTTP_200_OK,
    )


# Refresh token need JWT refresh token for refresh access token


@auth.get("/token/refresh")
@jwt_required(refresh=True)
def refresh_token() -> Tuple[Response, int]:
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({"access": access}), HTTP_200_OK


# Edit_user function need JWT token, this edit user info and return modified data


@auth.post("/me/edit")
@jwt_required()
@swag_from("../docs/auth/edit.yaml")
def edit_user() -> Tuple[Response, int] | HTTPException:
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    data = request.json

    if data is not None:
        username = data.get("username", user.username)
        pdp_url = data.get("pdp_url", user.pdp_url)
        email = data.get("email", user.email)
        password = data.get("password")
        old_password = data.get("old_password")

        errors = {}

        # Data check before sending
        if username != user.username:
            if len(username) < 3:
                errors["username"] = "Username is too short"
            elif not username.isalnum() or " " in username:
                errors["username"] = "Username should be alphanumeric, also no spaces"
            elif User.query.filter_by(username=username).first() is not None:
                errors["username"] = "Username is taken"
            else:
                user.username = username
        if pdp_url != user.pdp_url:
            user.pdp_url = pdp_url

        if email != user.email:
            if not validators.email(email):
                errors["email"] = "Email is not valid"
            elif User.query.filter_by(email=email).first() is not None:
                errors["email"] = "Email is taken"
            else:
                user.email = email

        if password and old_password:
            if password == old_password:
                errors["password"] = "New password must be different from old password"
            elif len(password) < 6:
                errors["password"] = "Password is too short"
            elif not check_password_hash(user.password, old_password):
                errors["password"] = "Invalid old password"
            else:
                user.password = generate_password_hash(password)

        if errors:
            abort(HTTP_400_BAD_REQUEST, errors)

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "User updated",
                    "user": user,
                }
            )
        ), HTTP_200_OK
    abort(HTTP_400_BAD_REQUEST, "Invalid request body")


# Remove_user funtion need JWT token and remove user in database


def remove_favoris(user_id: int) -> None:
    favoris = UserFavori.query.filter(UserFavori.user_id == user_id).all()
    [db.session.delete(f) for f in favoris]
    db.session.commit()


@auth.delete("/me/remove")
@jwt_required()
@swag_from("../docs/auth/remove.yaml")
def remove_user() -> Tuple[Response, int] | HTTPException:
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        abort(HTTP_404_NOT_FOUND, "User not found")

    remove_favoris(user_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({}), HTTP_200_OK
