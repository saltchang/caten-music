# helper/register_format_checker.py

import re


def checkFormat(username, email, displayname, password):

    check_result = {
        "username_check": False,
        "email_check": False,
        "displayname_check": False,
        "password_check": False
    }

    pattern = {
        "username": r"^[A-Za-z_0-9]{4,25}$",
        "email": r"^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]{3,65}$",
        "displayname": r"^[\u4e00-\u9fa5_a-zA-Z0-9]{1,17}$",
        "chinese_char": r"^[\u4e00-\u9fa5]+$",
        "password": r"^([a-zA-Z0-9!_@#\$%\^&\*\+\-\/\:]){8,65}$"
    }

    # Check Username
    if re.fullmatch(pattern["username"], username):
        check_result["username_check"] = True

    # Check Email
    if re.fullmatch(pattern["email"], email):
        check_result["email_check"] = True

    # Check Displayname
    if re.fullmatch(pattern["displayname"], displayname):
        stringLen = 0

        for c in displayname:
            if re.fullmatch(pattern["chinese_char"], c):
                stringLen += 2
            else:
                stringLen += 1

        if stringLen <= 16:
            check_result["displayname_check"] = True

    # Check Passowrd
    if re.fullmatch(pattern["password"], password):
        check_result["password_check"] = True

    return check_result
