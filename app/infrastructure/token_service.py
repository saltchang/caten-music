from datetime import UTC, datetime, timedelta

import jwt


class JwtTokenService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = 'HS256',
        access_token_expire_minutes: int = 60 * 24 * 14,
        refresh_token_expire_minutes: int = 60 * 24 * 30,
        activation_token_expire_minutes: int = 120,
    ):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._access_expire = access_token_expire_minutes
        self._refresh_expire = refresh_token_expire_minutes
        self._activation_expire = activation_token_expire_minutes

    def create_access_token(self, user_id: int) -> str:
        payload = {
            'sub': str(user_id),
            'type': 'access',
            'exp': datetime.now(UTC) + timedelta(minutes=self._access_expire),
            'iat': datetime.now(UTC),
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def create_refresh_token(self, user_id: int) -> str:
        payload = {
            'sub': str(user_id),
            'type': 'refresh',
            'exp': datetime.now(UTC) + timedelta(minutes=self._refresh_expire),
            'iat': datetime.now(UTC),
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            payload['sub'] = int(payload['sub'])
            return payload
        except jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError, ValueError:
            return None

    def create_activation_token(self, user_id: int) -> str:
        payload = {
            'sub': str(user_id),
            'purpose': 'activation',
            'exp': datetime.now(UTC) + timedelta(minutes=self._activation_expire),
            'iat': datetime.now(UTC),
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def create_password_reset_token(self, user_id: int) -> str:
        payload = {
            'sub': str(user_id),
            'purpose': 'reset_password',
            'exp': datetime.now(UTC) + timedelta(minutes=self._activation_expire),
            'iat': datetime.now(UTC),
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def verify_purpose_token(self, token: str, purpose: str) -> dict | None:
        payload = self.decode_token(token)
        if payload is None:
            return None
        if payload.get('purpose') != purpose:
            return None
        return payload
