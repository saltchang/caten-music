import re

USERNAME_PATTERN = re.compile(r'^[A-Za-z_0-9]{4,25}$')
EMAIL_PATTERN = re.compile(r'^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]{3,65}$')
PASSWORD_PATTERN = re.compile(r'^([a-zA-Z0-9!_@#\$%\^&\*\+\-\/\:]){8,65}$')
DISPLAYNAME_PATTERN = re.compile(r'^[\u4e00-\u9fa5_a-zA-Z0-9]{1,17}$')
CHINESE_CHAR_PATTERN = re.compile(r'^[\u4e00-\u9fa5]+$')


def validate_username(username: str) -> bool:
    return bool(USERNAME_PATTERN.fullmatch(username))


def validate_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(email))


def validate_password(password: str) -> bool:
    return bool(PASSWORD_PATTERN.fullmatch(password))


def validate_displayname(displayname: str) -> bool:
    if not DISPLAYNAME_PATTERN.fullmatch(displayname):
        return False

    width = 0
    for char in displayname:
        if CHINESE_CHAR_PATTERN.fullmatch(char):
            width += 2
        else:
            width += 1

    return width <= 16


def check_login_format(primary: str, password: str) -> dict:
    result: dict = {'primary_type': None, 'password_valid': False}

    if EMAIL_PATTERN.fullmatch(primary):
        result['primary_type'] = 'email'

    if USERNAME_PATTERN.fullmatch(primary):
        result['primary_type'] = 'username'

    if PASSWORD_PATTERN.fullmatch(password):
        result['password_valid'] = True

    return result
