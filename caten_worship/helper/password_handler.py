# helper/password_handler.py

import hashlib
import os

hash_salt = os.environ.get("HASH_SALT")


def createPasswordHash(password_in):

    password = password_in
    password = password + hash_salt

    password_hash = hashlib.sha256(
        bytes(password, encoding="utf8")).hexdigest()

    return str(password_hash)


def checkPasswordHash(password_tocheck, password_hash_in_db):

    hash_to_check = createPasswordHash(password_tocheck)

    if hash_to_check == password_hash_in_db:
        return True

    else:
        return False  
