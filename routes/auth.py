from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from repositories.user import UserRepository
from services.user_service import UserService
from validation.schemas import LoginSchema, RegisterSchema

auth = Blueprint("api/auth", __name__)

# Register a new user with a unique username and password


@auth.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    data = request.get_json()

    # Validate the input data
    errors = RegisterSchema().validate(data)
    if errors:
        return jsonify(errors), 422

    username = data["username"]
    password = data["password"]

    return jsonify(*UserService.register_user(username, password))


# Authenticate user and return sign-in token
@auth.route("/login", methods=["POST"])
def login():
    """Authenticate a user"""
    data = request.get_json()

    # Validate the input data
    errors = LoginSchema().validate(data)
    if errors:
        return jsonify(errors), 422

    username = data["username"]
    password = data["password"]

    return jsonify(*UserService.authenticate_user(username, password))
