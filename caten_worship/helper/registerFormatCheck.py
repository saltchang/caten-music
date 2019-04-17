# helper/registerFormatCheck.py

import re

def formatCheck(username, email, displayname, password):
    check_result = {
        "username_check": False,
        "email_check": False,
        "displayname_check": False,
        "password_check": False
    }
    if re.fullmatch(r"^[A-Za-z_0-9]{4,25}$", username):
        check_result["username_check"] = True

    if re.fullmatch(r"^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$", email):
        if len(email) > 2 and len(email) < 65:
            check_result["email_check"] = True
    
    if re.fullmatch(r"^[\u4e00-\u9fa5_a-zA-Z0-9]{1,17}$", displayname):
        stringLen = 0
        for c in displayname:
            if re.fullmatch(r"^[\u4e00-\u9fa5]+$", c):
                stringLen += 2
            else:
                stringLen += 1
        if stringLen <= 16:
            check_result["displayname_check"] = True
    
    if re.fullmatch(r"^([a-zA-Z0-9!_@#\$%\^&\*\+\-\/\:]){8,65}$", password):
        check_result["password_check"] = True

    return check_result
