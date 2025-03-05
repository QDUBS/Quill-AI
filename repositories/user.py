from models.user import User, db


class UserRepository:
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter(User.username.ilike(username)).first()

    @staticmethod
    def create_user(username, hashed_password):
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
