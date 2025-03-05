from repositories.user import UserRepository
from models.user import db, User


def test_create_user():
    user = UserRepository.create_user("testuser", "hashedpassword")
    assert user.username == "testuser"


def test_get_user_by_username():
    user = UserRepository.get_user_by_username("testuser")
    assert user is not None
