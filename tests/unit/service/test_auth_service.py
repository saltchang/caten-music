from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.core.entities.invitation_code import InvitationCode
from app.core.entities.user import User
from app.core.entities.user_profile import UserProfile
from app.core.exceptions import (
    EmailExistsError,
    InvalidCredentialsError,
    InvalidInputError,
    InvitationCodeExpiredError,
    InvitationCodeInvalidError,
    TokenInvalidError,
    UserDeactivatedError,
    UsernameExistsError,
    UserNotActivatedError,
)
from app.service.auth_service import AuthService


@pytest.fixture
def deps():
    return {
        'user_repo': AsyncMock(),
        'user_profile_repo': AsyncMock(),
        'invitation_repo': AsyncMock(),
        'password_hasher': MagicMock(),
        'token_service': MagicMock(),
        'mail_service': MagicMock(),
    }


@pytest.fixture
def auth_service(deps):
    return AuthService(**deps)


@pytest.fixture
def sample_user():
    return User(
        id=1,
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
        displayname='TestUser',
        is_authenticated=True,
        is_active=True,
    )


class TestLogin:
    async def test_login_with_valid_username(self, auth_service, deps, sample_user):
        """
        GIVEN a registered user with valid credentials
        WHEN login is called with a valid username and password
        THEN access and refresh tokens are returned
        """
        # Arrange
        deps['user_repo'].get_by_username.return_value = sample_user
        deps['password_hasher'].verify.return_value = True
        deps['token_service'].create_access_token.return_value = 'access_token'
        deps['token_service'].create_refresh_token.return_value = 'refresh_token'

        # Act
        result = await auth_service.login('testuser', 'password123')

        # Assert
        assert result.access_token == 'access_token'
        assert result.refresh_token == 'refresh_token'
        deps['user_repo'].get_by_username.assert_called_once_with('testuser')

    async def test_login_with_valid_email(self, auth_service, deps, sample_user):
        """
        GIVEN a registered user with valid credentials
        WHEN login is called with a valid email and password
        THEN access token is returned and email lookup is used
        """
        # Arrange
        deps['user_repo'].get_by_email.return_value = sample_user
        deps['password_hasher'].verify.return_value = True
        deps['token_service'].create_access_token.return_value = 'access_token'
        deps['token_service'].create_refresh_token.return_value = 'refresh_token'

        # Act
        result = await auth_service.login('test@example.com', 'password123')

        # Assert
        assert result.access_token == 'access_token'
        deps['user_repo'].get_by_email.assert_called_once_with('test@example.com')

    async def test_login_wrong_password(self, auth_service, deps, sample_user):
        """
        GIVEN a registered user
        WHEN login is called with an incorrect password
        THEN InvalidCredentialsError is raised
        """
        # Arrange
        deps['user_repo'].get_by_username.return_value = sample_user
        deps['password_hasher'].verify.return_value = False

        # Act & Assert
        with pytest.raises(InvalidCredentialsError):
            await auth_service.login('testuser', 'wrongpassword')

    async def test_login_nonexistent_user(self, auth_service, deps):
        """
        GIVEN no user exists with the given username
        WHEN login is called
        THEN InvalidCredentialsError is raised
        """
        # Arrange
        deps['user_repo'].get_by_username.return_value = None

        # Act & Assert
        with pytest.raises(InvalidCredentialsError):
            await auth_service.login('nouser', 'password123')

    async def test_login_unactivated_account(self, auth_service, deps):
        """
        GIVEN a user whose account is not yet activated
        WHEN login is called with correct credentials
        THEN UserNotActivatedError is raised
        """
        # Arrange
        user = User(
            id=1,
            username='testuser',
            email='t@e.com',
            password_hash='h',
            displayname='T',
            is_authenticated=False,
            is_active=True,
        )
        deps['user_repo'].get_by_username.return_value = user
        deps['password_hasher'].verify.return_value = True

        # Act & Assert
        with pytest.raises(UserNotActivatedError):
            await auth_service.login('testuser', 'password123')

    async def test_login_deactivated_account(self, auth_service, deps):
        """
        GIVEN a user whose account has been deactivated
        WHEN login is called with correct credentials
        THEN UserDeactivatedError is raised
        """
        # Arrange
        user = User(
            id=1,
            username='testuser',
            email='t@e.com',
            password_hash='h',
            displayname='T',
            is_authenticated=True,
            is_active=False,
        )
        deps['user_repo'].get_by_username.return_value = user
        deps['password_hasher'].verify.return_value = True

        # Act & Assert
        with pytest.raises(UserDeactivatedError):
            await auth_service.login('testuser', 'password123')

    async def test_login_invalid_format(self, auth_service):
        """
        GIVEN invalid login input format
        WHEN login is called with malformed credentials
        THEN InvalidInputError is raised
        """
        # Act & Assert
        with pytest.raises(InvalidInputError):
            await auth_service.login('!!', 'short')


class TestRegister:
    async def test_register_happy_path(self, auth_service, deps):
        """
        GIVEN valid registration data with a valid invitation code
        WHEN register is called
        THEN a new user is created, profile is set up, and activation email is sent

        NOTE: This test performs multiple assertions covering the full
        registration side effects (user creation, profile creation, email).
        """
        # Arrange
        deps['user_repo'].exists_username.return_value = False
        deps['user_repo'].exists_email.return_value = False
        invitation = InvitationCode(
            id=1,
            code='VALID123',
            created_by=1,
            expires_at=datetime.now() + timedelta(hours=24),
        )
        deps['invitation_repo'].get_by_code.return_value = invitation
        deps['password_hasher'].hash.return_value = 'hashed'
        created_user = User(
            id=1,
            username='newuser',
            email='new@example.com',
            password_hash='hashed',
            displayname='NewUser',
        )
        deps['user_repo'].create.return_value = created_user
        deps['user_profile_repo'].create.return_value = UserProfile(id=1, user_id=1)
        deps['token_service'].create_activation_token.return_value = 'activation_token'

        # Act
        result = await auth_service.register(
            username='newuser',
            email='new@example.com',
            displayname='NewUser',
            password='password123',
            confirm_password='password123',
            invitation_code='VALID123',
        )

        # Assert
        assert result.username == 'newuser'
        deps['user_repo'].create.assert_called_once()
        deps['user_profile_repo'].create.assert_called_once()
        deps['mail_service'].send_activation_email.assert_called_once()

    async def test_register_duplicate_username(self, auth_service, deps):
        """
        GIVEN a username that already exists in the system
        WHEN register is called with that username
        THEN UsernameExistsError is raised
        """
        # Arrange
        deps['user_repo'].exists_username.return_value = True

        # Act & Assert
        with pytest.raises(UsernameExistsError):
            await auth_service.register(
                username='existing',
                email='new@example.com',
                displayname='New',
                password='password123',
                confirm_password='password123',
                invitation_code='CODE',
            )

    async def test_register_duplicate_email(self, auth_service, deps):
        """
        GIVEN an email that already exists in the system
        WHEN register is called with that email
        THEN EmailExistsError is raised
        """
        # Arrange
        deps['user_repo'].exists_username.return_value = False
        deps['user_repo'].exists_email.return_value = True

        # Act & Assert
        with pytest.raises(EmailExistsError):
            await auth_service.register(
                username='newuser',
                email='existing@example.com',
                displayname='New',
                password='password123',
                confirm_password='password123',
                invitation_code='CODE',
            )

    async def test_register_invalid_invitation_code(self, auth_service, deps):
        """
        GIVEN an invitation code that does not exist
        WHEN register is called with that code
        THEN InvitationCodeInvalidError is raised
        """
        # Arrange
        deps['user_repo'].exists_username.return_value = False
        deps['user_repo'].exists_email.return_value = False
        deps['invitation_repo'].get_by_code.return_value = None

        # Act & Assert
        with pytest.raises(InvitationCodeInvalidError):
            await auth_service.register(
                username='newuser',
                email='new@example.com',
                displayname='New',
                password='password123',
                confirm_password='password123',
                invitation_code='INVALID',
            )

    async def test_register_expired_invitation_code(self, auth_service, deps):
        """
        GIVEN an invitation code that has expired
        WHEN register is called with that code
        THEN InvitationCodeExpiredError is raised
        """
        # Arrange
        deps['user_repo'].exists_username.return_value = False
        deps['user_repo'].exists_email.return_value = False
        expired = InvitationCode(
            id=1,
            code='EXPIRED',
            created_by=1,
            expires_at=datetime.now() - timedelta(hours=1),
        )
        deps['invitation_repo'].get_by_code.return_value = expired

        # Act & Assert
        with pytest.raises(InvitationCodeExpiredError):
            await auth_service.register(
                username='newuser',
                email='new@example.com',
                displayname='New',
                password='password123',
                confirm_password='password123',
                invitation_code='EXPIRED',
            )

    async def test_register_password_mismatch(self, auth_service):
        """
        GIVEN password and confirm_password that do not match
        WHEN register is called
        THEN InvalidInputError is raised
        """
        # Act & Assert
        with pytest.raises(InvalidInputError):
            await auth_service.register(
                username='newuser',
                email='new@example.com',
                displayname='New',
                password='password123',
                confirm_password='different123',
                invitation_code='CODE',
            )


class TestActivate:
    async def test_activate_valid_token(self, auth_service, deps, sample_user):
        """
        GIVEN a valid activation token for an unactivated user
        WHEN activate_account is called
        THEN the user record is updated to activated
        """
        # Arrange
        deps['token_service'].verify_purpose_token.return_value = {'sub': 1, 'purpose': 'activation'}
        sample_user.is_authenticated = False
        deps['user_repo'].get_by_id.return_value = sample_user
        deps['user_repo'].update.return_value = sample_user

        # Act
        await auth_service.activate_account('valid_token')

        # Assert
        deps['user_repo'].update.assert_called_once()

    async def test_activate_invalid_token(self, auth_service, deps):
        """
        GIVEN an invalid activation token
        WHEN activate_account is called
        THEN TokenInvalidError is raised
        """
        # Arrange
        deps['token_service'].verify_purpose_token.return_value = None

        # Act & Assert
        with pytest.raises(TokenInvalidError):
            await auth_service.activate_account('bad_token')


class TestResetPassword:
    async def test_request_password_reset(self, auth_service, deps, sample_user):
        """
        GIVEN an existing user email
        WHEN request_password_reset is called
        THEN a password reset email is sent
        """
        # Arrange
        deps['user_repo'].get_by_email.return_value = sample_user
        deps['token_service'].create_password_reset_token.return_value = 'reset_token'

        # Act
        await auth_service.request_password_reset('test@example.com')

        # Assert
        deps['mail_service'].send_password_reset_email.assert_called_once()

    async def test_reset_password_valid_token(self, auth_service, deps, sample_user):
        """
        GIVEN a valid password reset token and matching new passwords
        WHEN reset_password is called
        THEN the user's password is updated
        """
        # Arrange
        deps['token_service'].verify_purpose_token.return_value = {'sub': 1, 'purpose': 'reset_password'}
        deps['user_repo'].get_by_id.return_value = sample_user
        deps['password_hasher'].hash.return_value = 'new_hash'
        deps['user_repo'].update.return_value = sample_user

        # Act
        await auth_service.reset_password('valid_token', 'newpass123', 'newpass123')

        # Assert
        deps['user_repo'].update.assert_called_once()


class TestRefreshToken:
    async def test_refresh_token_success(self, auth_service, deps, sample_user):
        """
        GIVEN a valid refresh token for an active user
        WHEN refresh_token is called
        THEN new access and refresh tokens are returned
        """
        # Arrange
        deps['token_service'].decode_token.return_value = {'sub': 1, 'type': 'refresh'}
        deps['user_repo'].get_by_id.return_value = sample_user
        deps['token_service'].create_access_token.return_value = 'new_access'
        deps['token_service'].create_refresh_token.return_value = 'new_refresh'

        # Act
        result = await auth_service.refresh_token('valid_refresh')

        # Assert
        assert result.access_token == 'new_access'
        assert result.refresh_token == 'new_refresh'
