import re
from typing import Tuple

import validators
from flasgger import swag_from
from flask import Blueprint, Response, abort, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash, generate_password_hash

from src import db
from src.business_logic.favoris.delete_favoris_for_one_user import (
    delete_favoris_for_one_user,
)
from src.business_logic.user.exceptions import AuthenticationException
from src.business_logic.user.validate_user import validate_user
from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from src.models import User

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

# Register function in "/api/v1/auth/register" with flasgger


@auth.post("/register")
@swag_from("../docs/auth/login/register.yaml")
def register() -> Tuple[Response, int]:
    # Collect informations
    data = request.json
    if data is not None:
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if len(password) < 6 or not re.match(r"^[a-zA-Z0-9]{3,20}$", username):
            return {"error": "Invalid password or username"}, HTTP_400_BAD_REQUEST
        # Verify with "validators" if email is valid
        if not validators.email(email):
            return {"error": "Email is not valid"}, HTTP_409_CONFLICT
        # Verify if email is in database
        if db.session.query(User).filter_by(email=email).first() is not None:
            return {"error": "Email is taken"}, HTTP_409_CONFLICT
        # Verify if username is in database
        if db.session.query(User).filter_by(username=username).first() is not None:
            return {"error": "username is taken"}, HTTP_409_CONFLICT
        # Hash password
        pwd_hash = generate_password_hash(password)

        user_profile_picture = (
            f"https://api.dicebear.com/7.x/notionists-neutral/svg?seed='{email}'"
        )

        user = User(
            username=username,
            password=pwd_hash,
            email=email,
            profile_pic_url=user_profile_picture,
        )
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
    return {"error": "Invalid request body"}, HTTP_400_BAD_REQUEST


# Login function in "/api/v1/auth/login" with flasgger


@auth.post("/login")
@swag_from("../docs/auth/login/login.yaml")
def login() -> Tuple[Response, int] | HTTPException:
    try:
        data = request.json
        if data is None:
            raise AuthenticationException("Invalid request body")

        email = data.get("email")
        password = data.get("password")

        user = validate_user(email, password)

        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)

        response_data = {
            "user": {
                "id": user.id,
                "refresh": refresh,
                "access": access,
                "username": user.username,
                "email": user.email,
            }
        }

        return jsonify(response_data), HTTP_200_OK
    except AuthenticationException as e:
        return jsonify({"error": str(e)}), HTTP_401_UNAUTHORIZED


# Me function need JWT token return userInfo


@auth.get("/me")
@jwt_required()
@swag_from("../docs/auth/me.yaml")
def me() -> Tuple[Response, int]:
    user_id = get_jwt_identity()

    user: User = db.session.query(User).filter_by(id=user_id).first()
    if user.profile_pic_url is None:
        user.profile_pic_url = (
            f"https://api.dicebear.com/7.x/notionists-neutral/svg?seed='{user.email}'"
        )

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

    user = db.session.query(User).filter_by(id=user_id).first()

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


@auth.delete("/me/remove")
@jwt_required()
@swag_from("../docs/auth/remove.yaml")
def remove_user() -> Tuple[Response, int] | HTTPException:
    user_id = get_jwt_identity()
    user = db.session.query(User).filter_by(id=user_id).first()

    if not user:
        abort(HTTP_404_NOT_FOUND, "User not found")

    delete_favoris_for_one_user(user_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({}), HTTP_200_OK
