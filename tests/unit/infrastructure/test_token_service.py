import time

from app.infrastructure.token_service import JwtTokenService


class TestJwtTokenService:
    def setup_method(self):
        self.service = JwtTokenService(
            secret_key='test-secret-key-that-is-long-enough-for-hs256',
            algorithm='HS256',
            access_token_expire_minutes=60,
            refresh_token_expire_minutes=120,
            activation_token_expire_minutes=5,
        )

    def test_create_access_token_contains_user_id(self):
        """
        GIVEN a configured JWT token service
        WHEN creating an access token for a user
        THEN the decoded payload contains the user ID and access type
        """
        # Act
        token = self.service.create_access_token(user_id=42)
        payload = self.service.decode_token(token)

        # Assert
        assert payload is not None
        assert payload['sub'] == 42
        assert payload['type'] == 'access'

    def test_create_access_token_has_expiry(self):
        """
        GIVEN a configured JWT token service
        WHEN creating an access token
        THEN the decoded payload contains an expiration claim
        """
        # Act
        token = self.service.create_access_token(user_id=1)
        payload = self.service.decode_token(token)

        # Assert
        assert payload is not None
        assert 'exp' in payload

    def test_decode_valid_token(self):
        """
        GIVEN a valid access token
        WHEN decoding the token
        THEN the payload contains the correct user ID
        """
        # Arrange
        token = self.service.create_access_token(user_id=10)

        # Act
        payload = self.service.decode_token(token)

        # Assert
        assert payload is not None
        assert payload['sub'] == 10

    def test_decode_expired_token(self):
        """
        GIVEN a token service configured with a negative expiry (already expired)
        WHEN decoding the token
        THEN the result is None
        """
        # Arrange
        service = JwtTokenService(
            secret_key='test-secret-key-that-is-long-enough-for-hs256',
            algorithm='HS256',
            access_token_expire_minutes=-1,
            refresh_token_expire_minutes=120,
            activation_token_expire_minutes=5,
        )
        token = service.create_access_token(user_id=1)

        # Act
        payload = service.decode_token(token)

        # Assert
        assert payload is None

    def test_decode_invalid_token(self):
        """
        GIVEN an invalid token string
        WHEN decoding the token
        THEN the result is None
        """
        # Act
        payload = self.service.decode_token('invalid.token.string')

        # Assert
        assert payload is None

    def test_create_refresh_token(self):
        """
        GIVEN a configured JWT token service
        WHEN creating a refresh token for a user
        THEN the decoded payload contains the user ID and refresh type
        """
        # Act
        token = self.service.create_refresh_token(user_id=42)
        payload = self.service.decode_token(token)

        # Assert
        assert payload is not None
        assert payload['sub'] == 42
        assert payload['type'] == 'refresh'

    def test_refresh_token_differs_from_access(self):
        """
        GIVEN an access token and a refresh token for the same user
        WHEN comparing the two tokens
        THEN they are different strings

        Note: time.sleep(0.01) in Arrange ensures distinct timestamps.
        """
        # Arrange
        access = self.service.create_access_token(user_id=1)
        time.sleep(0.01)

        # Act
        refresh = self.service.create_refresh_token(user_id=1)

        # Assert
        assert access != refresh

    def test_create_activation_token(self):
        """
        GIVEN a configured JWT token service
        WHEN creating an activation token for a user
        THEN the verified payload contains the user ID and activation purpose
        """
        # Act
        token = self.service.create_activation_token(user_id=5)
        payload = self.service.verify_purpose_token(token, 'activation')

        # Assert
        assert payload is not None
        assert payload['sub'] == 5
        assert payload['purpose'] == 'activation'

    def test_create_password_reset_token(self):
        """
        GIVEN a configured JWT token service
        WHEN creating a password reset token for a user
        THEN the verified payload contains the user ID and reset_password purpose
        """
        # Act
        token = self.service.create_password_reset_token(user_id=5)
        payload = self.service.verify_purpose_token(token, 'reset_password')

        # Assert
        assert payload is not None
        assert payload['sub'] == 5
        assert payload['purpose'] == 'reset_password'

    def test_verify_purpose_token_wrong_purpose(self):
        """
        GIVEN an activation token
        WHEN verifying it with the wrong purpose (reset_password)
        THEN the result is None
        """
        # Arrange
        token = self.service.create_activation_token(user_id=5)

        # Act
        payload = self.service.verify_purpose_token(token, 'reset_password')

        # Assert
        assert payload is None

    def test_activation_token_expired(self):
        """
        GIVEN a token service configured with a negative activation expiry
        WHEN creating and verifying an activation token
        THEN the result is None
        """
        # Arrange
        service = JwtTokenService(
            secret_key='test-secret-key-that-is-long-enough-for-hs256',
            algorithm='HS256',
            access_token_expire_minutes=60,
            refresh_token_expire_minutes=120,
            activation_token_expire_minutes=-1,
        )
        token = service.create_activation_token(user_id=1)

        # Act
        payload = service.verify_purpose_token(token, 'activation')

        # Assert
        assert payload is None
