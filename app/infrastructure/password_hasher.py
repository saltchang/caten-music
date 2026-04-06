import hashlib


class Sha256PasswordHasher:
    def __init__(self, salt: str):
        self._salt = salt

    def hash(self, password: str) -> str:
        salted = password + self._salt
        return hashlib.sha256(bytes(salted, encoding='utf8')).hexdigest()

    def verify(self, password: str, password_hash: str) -> bool:
        return self.hash(password) == password_hash
