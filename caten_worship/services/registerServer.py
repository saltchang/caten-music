# services/registerServer.py

from caten_worship.models import User, db


class Validator:

    def username(self, username_to_validate):
        if User.query.filter_by(username=username_to_validate).first():
            return False

    def email(self, email_to_validate):
        if User.query.filter_by(email=email_to_validate).first():
            return False


class RegisterHandler:

    def register_user(self, username, email, password, displayname):

        user = User(username=username, email=email, password=password, displayname=displayname)

        db.session.add(user)
        db.session.commit()

        return user.create_activate_token()


class Activator:

    def activate_user(self, check_result):

        user = User.query.filter_by(id=check_result.get("user_id")).first()
        user.activated = True
        db.session.add(user)
        db.session.commit()
