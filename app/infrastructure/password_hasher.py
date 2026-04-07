import hashlib


class Sha256PasswordHasher:
    """SHA-256 password hasher with static salt, compatible with legacy data."""

    def __init__(self, salt: str):
        self._salt = salt

    def hash(self, password: str) -> str:
        """Hash a password using SHA-256 with the configured salt.

        Args:
            password: Plain-text password.

        Returns:
            Hex-encoded hash string.
        """
        salted = password + self._salt
        return hashlib.sha256(bytes(salted, encoding='utf8')).hexdigest()

    def verify(self, password: str, password_hash: str) -> bool:
        """Verify a password against a stored hash.

        Args:
            password: Plain-text password to check.
            password_hash: Expected hex-encoded hash.

        Returns:
            True if the password matches.
        """
        return self.hash(password) == password_hash
