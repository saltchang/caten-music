# helper/login_checker.py

from caten_worship import models

def checkLogin(primary_type, primary, password):

    if primary_type == "email":
        user_to_check = models.User.query.filter_by(email=primary).first()
    elif primary_type == "username":
        user_to_check = models.User.query.filter_by(username=primary).first()

    return user_to_check.verify_password(password)
