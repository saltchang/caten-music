# helper/password_handler.py

import hashlib

def hash_generator(password):

    password_hash = hashlib.sha512(
        bytes(password, encoding="utf8")).hexdigest()

    return password_hash


def check_password(password, hash_in_db):
    
    password_hash = hashlib.sha512(
        bytes(password, encoding="utf8")).hexdigest()

    if password_hash == hash_in_db:
        return True
    else:
        return False
