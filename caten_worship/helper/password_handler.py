# helper/password_handler.py

import hashlib

def hash_generator(password):

    password_hash = hashlib.sha512(
        bytes(password, encoding="utf8")).hexdigest()

    return str(password_hash)


def check_password(password_tocheck, password_hash_in_db):
    
    password_hash = hashlib.sha512(
        bytes(password_tocheck, encoding="utf8")).hexdigest()

    if str(password_hash) == password_hash_in_db:
        return True
    else:
        return False
