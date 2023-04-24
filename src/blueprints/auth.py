from flask import Blueprint, jsonify, request
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
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from src import db
from src.models import User, Favori

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

# Register function in "/api/v1/auth/register" with flasgger


@auth.post("/register")
@swag_from("../docs/auth/login/register.yaml")
def register():
    # Collect informations
    data = request.json
    try: 
        username = data["username"]
        name = data["name"]
        email = data["email"]
        password = data["password"]
    except KeyError:
        return jsonify({"error": "Invalid request body"}), HTTP_400_BAD_REQUEST

    # Verify if password is large enought
    if len(password) < 6:
        return jsonify({"error": "Password is too short"}), HTTP_400_BAD_REQUEST
    # Verify if username is large enought
    if len(username) < 3:
        return jsonify({"error": "Username is too short"}), HTTP_400_BAD_REQUEST
    # Verify if username have alphanumeric characters or space
    if not username.isalnum() or " " in username:
        return (
            jsonify({"error": "Username shloud be alphanumeric, also no spaces"}),
            HTTP_400_BAD_REQUEST,
        )
    # Verify if name have alphanumeric characters or space
    if not name.isalnum() or " " in name:
        return (
            jsonify({"error": "Name shloud be alphanumeric, also no spaces"}),
            HTTP_400_BAD_REQUEST,
        )
    # Verify with "validators" if email is valid
    if not validators.email(email):
        return jsonify({"error": "Email is not valid"}), HTTP_400_BAD_REQUEST
    # Verify if email is in database
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email is taken"}), HTTP_409_CONFLICT
    # Verify if username is in database
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "username is taken"}), HTTP_409_CONFLICT
    # Hash password
    pwd_hash = generate_password_hash(password)

    user = User(username=username, password=pwd_hash, email=email, name=name)
    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "User created",
                "user": {
                    "username": username,
                    "name": name,
                    "email": email,
                },
            }
        ),
        HTTP_201_CREATED,
    )


# Login function in "/api/v1/auth/login" with flasgger


@auth.post("/login")
@swag_from("../docs/auth/login/login.yaml")
def login():
    # Collect informations
    data = request.json
    try: 
        email = data["email"]
        password = data["password"]

    except KeyError:
        return jsonify({"error": "Invalid request body"}), HTTP_400_BAD_REQUEST
    
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
                            "refresh": refresh,
                            "access": access,
                            "username": user.username,
                            "email": user.email,
                        }
                    }
                ),
                HTTP_200_OK,
            )
    return jsonify({"error": "Wrong credendials"}), HTTP_401_UNAUTHORIZED


# Me function need JWT token return userInfo


@auth.get("/me")
@jwt_required()
@swag_from("../docs/auth/me.yaml")
def me():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return (
        jsonify(
            {
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "pdp": user.pdp_url,
                "password": user.password,
            }
        ),
        HTTP_200_OK,
    )


# Refresh token need JWT refresh token for refresh access token


@auth.get("/token/refresh")
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({"access": access}), HTTP_200_OK


# Edit_user function need JWT token, this edit user info and return modified data


@auth.post("/me/edit")
@jwt_required()
@swag_from("../docs/auth/edit.yaml")
def edit_user():
    user_id = get_jwt_identity()


    user = User.query.filter_by(id=user_id).first()

    username = request.json.get("username", user.username)
    name = request.json.get("name", user.name)
    pdp_url = request.json.get("pdp_url", user.pdp_url)
    email = request.json.get("email", user.email)
    password = request.json.get("password")
    old_password = request.json.get("old_password")

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
    if name != user.name:
        if not name.isalnum() or " " in name:
            errors["name"] = "Name should be alphanumeric, also no spaces"
        else:
            user.name = name
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
        return jsonify({"errors": errors}), HTTP_400_BAD_REQUEST

    db.session.commit()

    return (
        jsonify(
            {
                "message": "User updated",
                "user": {
                    "username": user.username,
                    "name": user.name,
                    "pdp_url": user.pdp_url,
                    "email": user.email,
                },
            }
        )
    ), HTTP_200_OK


# Remove_user funtion need JWT token and remove user in database


def remove_favoris(user_id: int) -> None:
    favoris = Favori.query.filter_by(request_user_id=user_id).all()
    list(map(lambda f: db.session.delete(f), favoris))
    db.session.commit()


@auth.delete("/me/remove")
@jwt_required()
@swag_from("../docs/auth/remove.yaml")
def remove_user():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), HTTP_404_NOT_FOUND
    
    remove_favoris(user_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
