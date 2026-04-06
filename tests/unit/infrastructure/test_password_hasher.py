import hashlib

from app.infrastructure.password_hasher import Sha256PasswordHasher


class TestSha256PasswordHasher:
    def setup_method(self):
        self.hasher = Sha256PasswordHasher(salt='test-salt')

    def test_hash_produces_64_char_hex(self):
        """
        GIVEN a password hasher with a configured salt
        WHEN hashing a password
        THEN the result is a 64-character lowercase hex string
        """
        # Act
        result = self.hasher.hash('mypassword')

        # Assert
        assert len(result) == 64
        assert all(c in '0123456789abcdef' for c in result)

    def test_hash_is_deterministic(self):
        """
        GIVEN a password hasher with a configured salt
        WHEN hashing the same password twice
        THEN both hashes are identical
        """
        # Act
        hash1 = self.hasher.hash('mypassword')
        hash2 = self.hasher.hash('mypassword')

        # Assert
        assert hash1 == hash2

    def test_different_passwords_produce_different_hashes(self):
        """
        GIVEN a password hasher with a configured salt
        WHEN hashing two different passwords
        THEN the resulting hashes differ
        """
        # Act
        hash1 = self.hasher.hash('password1')
        hash2 = self.hasher.hash('password2')

        # Assert
        assert hash1 != hash2

    def test_verify_correct_password(self):
        """
        GIVEN a hashed password
        WHEN verifying with the correct plaintext password
        THEN it returns True
        """
        # Arrange
        password_hash = self.hasher.hash('mypassword')

        # Act
        result = self.hasher.verify('mypassword', password_hash)

        # Assert
        assert result is True

    def test_verify_wrong_password(self):
        """
        GIVEN a hashed password
        WHEN verifying with an incorrect plaintext password
        THEN it returns False
        """
        # Arrange
        password_hash = self.hasher.hash('mypassword')

        # Act
        result = self.hasher.verify('wrongpassword', password_hash)

        # Assert
        assert result is False

    def test_backward_compat_with_flask_implementation(self):
        """
        GIVEN the legacy Flask password hashing logic (sha256 of password + salt)
        WHEN hashing the same password with Sha256PasswordHasher
        THEN the output matches the legacy implementation exactly
        """
        # Arrange
        salt = 'test-salt'
        password = 'TestPassword123'

        # Replicate the old Flask logic exactly:
        # password_hash = hashlib.sha256(bytes(password + salt, encoding='utf8')).hexdigest()
        expected = hashlib.sha256(bytes(password + salt, encoding='utf8')).hexdigest()

        hasher = Sha256PasswordHasher(salt=salt)

        # Act
        result = hasher.hash(password)

        # Assert
        assert result == expected
