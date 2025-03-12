# helper/login_checker.py

import re

from caten_music import models


def checkLogin(primary_type, primary, password):
    if primary_type == "email":
        user_to_check = models.UserModel.query.filter_by(email=primary).first()

    elif primary_type == "username":
        user_to_check = models.UserModel.query.filter_by(username=primary).first()

    if user_to_check and user_to_check.verify_password(password):
        return user_to_check
    else:
        return False


def checkLoginFormat(primary, password):
    check_result = {"primary_check": "failed", "password_check": False}

    pattern = {
        "username": r"^[A-Za-z_0-9]{4,25}$",
        "email": r"^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]{3,65}$",
        "password": r"^([a-zA-Z0-9!_@#\$%\^&\*\+\-\/\:]){8,65}$",
    }

    # Check if Primary is Email
    if re.fullmatch(pattern["email"], primary):
        check_result["primary_check"] = "email"

    # Check Username
    if re.fullmatch(pattern["username"], primary):
        check_result["primary_check"] = "username"

    # Check Passowrd
    if re.fullmatch(pattern["password"], password):
        check_result["password_check"] = True

    return check_result
