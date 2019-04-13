# services/validateServer.py

from caten_worship.models import User, db

class Validator:

    def username(self, username_to_validate):
        if User.query.filter_by(username=username_to_validate).first():
            return False
    
    def email(self, email_to_validate):
        if User.query.filter_by(email=email_to_validate).first():
            return False

class RegisterHandler:

    def register_user(self, username, email, password):

        user = User(username=username, email=email, password=password)

        return user.create_activate_token()

        db.session.add(user)
        db.session.commit()


class Activator:

    def activate_user(self, check_result):

        user = User.query.filter_by(id=check_result.get("user_id")).first()
        user.activated = True
        db.session.add(user)
        db.session.commit()
