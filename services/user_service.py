from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from repositories.user import UserRepository
import logging

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def register_user(username: str, password: str):
        """Registers a new user with a hashed password"""
        username = username.lower()  # Normalize username

        # Check if user already exists
        existing_user = UserRepository.get_user_by_username(username)
        if existing_user:
            return {"msg": "User already exists"}, 422

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create user
        new_user = UserRepository.create_user(username, hashed_password)

        logger.info(f"New user registered: {username}")
        return {"msg": "User created successfully", "user_id": new_user.id}, 201

    @staticmethod
    def authenticate_user(username: str, password: str):
        """Authenticates a user and generates an access token"""
        username = username.lower()  # Normalize username
        user = UserRepository.get_user_by_username(username)

        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id)
            logger.info(f"User logged in: {username}")
            return {"access_token": access_token}, 200

        logger.warning(f"Failed login attempt for user: {username}")
        return {"msg": "Invalid credentials"}, 401
