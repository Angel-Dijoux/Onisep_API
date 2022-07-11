from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required
from flasgger import swag_from

from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from src.db import User, db

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
@swag_from('./docs/auth/login/register.yaml')
def register():
    username = request.json['username']
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({"error": "Password is too short"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({"error": "Username is too short"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({"error": "Username shloud be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

    if not name.isalnum() or " " in name:
        return jsonify({"error": "Name shloud be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({"error": "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email is taken"}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "username is taken"}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, password=pwd_hash, email=email, name=name)
    db.session.add(user)
    db.session.commit()

    return jsonify(
        {
            "message": "User created",
            "user": {
                "username": username,
                "name": name,
                "email": email,
            }

        }
    ), HTTP_201_CREATED


@auth.post('/login')
@swag_from('./docs/auth/login/login.yaml')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify(
                {
                    'user': {
                        "refresh": refresh,
                        "access": access,
                        "username": user.username,
                        "email": user.email
                    }
                }
            ), HTTP_200_OK
    return jsonify({"error": "Wrong credendials"}), HTTP_401_UNAUTHORIZED


@auth.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return jsonify({
        "username": user.username,
        "email": user.email,
        "name": user.name
    }), HTTP_200_OK


@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        "access": access
    }), HTTP_200_OK
