from datetime import datetime

from app.core.entities.user import User
from app.core.entities.user_profile import UserProfile
from app.core.exceptions import (
    EmailExistsError,
    InvalidCredentialsError,
    InvalidInputError,
    InvitationCodeDisabledError,
    InvitationCodeExpiredError,
    InvitationCodeInvalidError,
    TokenInvalidError,
    UserDeactivatedError,
    UsernameExistsError,
    UserNotActivatedError,
    UserNotFoundError,
)
from app.core.interfaces.invitation_repository import InvitationRepository
from app.core.interfaces.mail_service import MailService
from app.core.interfaces.password_hasher import PasswordHasher
from app.core.interfaces.token_service import TokenService
from app.core.interfaces.user_profile_repository import UserProfileRepository
from app.core.interfaces.user_repository import UserRepository
from app.core.validators import check_login_format, validate_email, validate_password, validate_username


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        user_profile_repo: UserProfileRepository,
        invitation_repo: InvitationRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
        mail_service: MailService,
    ):
        self._user_repo = user_repo
        self._user_profile_repo = user_profile_repo
        self._invitation_repo = invitation_repo
        self._password_hasher = password_hasher
        self._token_service = token_service
        self._mail_service = mail_service

    async def login(self, primary: str, password: str) -> dict:
        login_check = check_login_format(primary, password)

        if login_check['primary_type'] is None or not login_check['password_valid']:
            raise InvalidInputError('Invalid login format')

        if login_check['primary_type'] == 'email':
            user = await self._user_repo.get_by_email(primary)
        else:
            user = await self._user_repo.get_by_username(primary)

        if not user:
            raise InvalidCredentialsError('Invalid credentials')

        if not self._password_hasher.verify(password, user.password_hash):
            raise InvalidCredentialsError('Invalid credentials')

        if not user.is_authenticated:
            raise UserNotActivatedError('Account not activated')

        if not user.is_active:
            raise UserDeactivatedError('Account deactivated')

        user.last_login_time = datetime.now()
        await self._user_repo.update(user)

        return {
            'access_token': self._token_service.create_access_token(user.id),
            'refresh_token': self._token_service.create_refresh_token(user.id),
            'token_type': 'bearer',
        }

    async def register(
        self,
        username: str,
        email: str,
        displayname: str,
        password: str,
        confirm_password: str,
        invitation_code: str,
    ) -> User:
        if password != confirm_password:
            raise InvalidInputError('Passwords do not match')

        if not validate_username(username):
            raise InvalidInputError('Invalid username format')

        if not validate_email(email):
            raise InvalidInputError('Invalid email format')

        if not validate_password(password):
            raise InvalidInputError('Invalid password format')

        if await self._user_repo.exists_username(username):
            raise UsernameExistsError('Username already exists')

        if await self._user_repo.exists_email(email):
            raise EmailExistsError('Email already exists')

        invitation = await self._invitation_repo.get_by_code(invitation_code)
        if not invitation:
            raise InvitationCodeInvalidError('Invalid invitation code')

        if invitation.is_disabled:
            raise InvitationCodeDisabledError('Invitation code is disabled')

        if not invitation.is_valid():
            raise InvitationCodeExpiredError('Invitation code expired')

        password_hash = self._password_hasher.hash(password)

        new_user = User(
            id=0,
            username=username,
            email=email,
            password_hash=password_hash,
            displayname=displayname,
            is_authenticated=False,
        )

        created_user = await self._user_repo.create(new_user)

        profile = UserProfile(id=0, user_id=created_user.id)
        await self._user_profile_repo.create(profile)

        invitation.usage_count += 1
        invitation.last_used_at = datetime.now()
        await self._invitation_repo.update(invitation)

        token = self._token_service.create_activation_token(created_user.id)
        self._mail_service.send_activation_email(
            email=email,
            username=username,
            activation_url=token,
        )

        return created_user

    async def activate_account(self, token: str) -> None:
        payload = self._token_service.verify_purpose_token(token, 'activation')
        if not payload:
            raise TokenInvalidError('Invalid or expired activation token')

        user = await self._user_repo.get_by_id(payload['sub'])
        if not user:
            raise UserNotFoundError('User not found')

        user.is_authenticated = True
        user.is_active = True
        await self._user_repo.update(user)

    async def request_password_reset(self, email: str) -> None:
        user = await self._user_repo.get_by_email(email)
        if not user:
            return

        token = self._token_service.create_password_reset_token(user.id)
        self._mail_service.send_password_reset_email(
            email=email,
            username=user.username,
            reset_url=token,
        )

    async def reset_password(self, token: str, password: str, confirm_password: str) -> None:
        if password != confirm_password:
            raise InvalidInputError('Passwords do not match')

        if not validate_password(password):
            raise InvalidInputError('Invalid password format')

        payload = self._token_service.verify_purpose_token(token, 'reset_password')
        if not payload:
            raise TokenInvalidError('Invalid or expired reset token')

        user = await self._user_repo.get_by_id(payload['sub'])
        if not user:
            raise UserNotFoundError('User not found')

        user.password_hash = self._password_hasher.hash(password)
        await self._user_repo.update(user)

    async def refresh_token(self, refresh_token_str: str) -> dict:
        payload = self._token_service.decode_token(refresh_token_str)
        if not payload or payload.get('type') != 'refresh':
            raise TokenInvalidError('Invalid refresh token')

        user = await self._user_repo.get_by_id(payload['sub'])
        if not user:
            raise UserNotFoundError('User not found')

        return {
            'access_token': self._token_service.create_access_token(user.id),
            'refresh_token': self._token_service.create_refresh_token(user.id),
            'token_type': 'bearer',
        }

    async def check_availability(self, username: str | None = None, email: str | None = None) -> dict:
        result = {}
        if username is not None:
            result['username_taken'] = await self._user_repo.exists_username(username)
        if email is not None:
            result['email_taken'] = await self._user_repo.exists_email(email)
        return result

    async def resend_activation_email(self, email: str) -> None:
        user = await self._user_repo.get_by_email(email)
        if not user:
            return

        if user.is_authenticated:
            raise InvalidInputError('Account already activated')

        token = self._token_service.create_activation_token(user.id)
        self._mail_service.send_activation_email(
            email=email,
            username=user.username,
            activation_url=token,
        )
