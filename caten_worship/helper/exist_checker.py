# helper/exist_checker.py

from caten_worship import models


class checkExist:

    def username(self, username):

        if models.User.query.filter_by(username=username).first():
            return True
        else:
            return False

    def email(self, email):

        if models.User.query.filter_by(email=email).first():
            return True
        else:
            return False
