from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.user import db, User

auth = Blueprint("api/auth", __name__)

# Register a new user with a unique username and password
@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    hashed_password = generate_password_hash(password)

    # Check for existing user
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"msg": f"User with {username} already exists"}), 422

    # Register new user
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

# Authenticate user and return sign-in token
@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid credentials"}), 401
