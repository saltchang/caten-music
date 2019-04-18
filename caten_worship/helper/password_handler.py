# helper/password_handler.py

import hashlib
import os

hash_salt = os.environ.get("HASH_SALT")


def createPasswordHash(password):

    password = password + hash_salt

    password_hash = hashlib.sha256(
        bytes(password, encoding="utf8")).hexdigest()

    return str(password_hash)


def checkPasswordHash(password_tocheck, password_hash_in_db):

    password = password + hash_salt

    password_hash = hashlib.sha256(
        bytes(password_tocheck, encoding="utf8")).hexdigest()

    if str(password_hash) == password_hash_in_db:
        return True

    else:
        return False
