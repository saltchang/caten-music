from app.infrastructure.password_hasher import Sha256PasswordHasher
from app.infrastructure.token_service import JwtTokenService
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import create_test_invitation_code, create_test_user


async def test_register_success(client: AsyncClient, api_session: AsyncSession, password_hasher: Sha256PasswordHasher):
    """
    GIVEN a valid invitation code exists
    WHEN registering a new user with valid credentials
    THEN it should return 201 with a success message
    """
    # Arrange
    await create_test_invitation_code(api_session)

    # Act
    response = await client.post(
        '/auth/register',
        json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'displayname': 'New User',
            'password': 'Test1234!',
            'confirm_password': 'Test1234!',
            'invitation_code': 'TESTCODE1234',
        },
    )

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data['message'] == 'Registration successful. Please check your email to activate your account.'


async def test_register_duplicate_username(
    client: AsyncClient, api_session: AsyncSession, password_hasher: Sha256PasswordHasher
):
    """
    GIVEN a user with the username 'existinguser' already exists
    WHEN registering a new user with the same username
    THEN it should return 409 with a duplicate username error
    """
    # Arrange
    await create_test_invitation_code(api_session)
    await create_test_user(api_session, password_hasher, username='existinguser', email='existing@example.com')

    # Act
    response = await client.post(
        '/auth/register',
        json={
            'username': 'existinguser',
            'email': 'another@example.com',
            'displayname': 'Another User',
            'password': 'Test1234!',
            'confirm_password': 'Test1234!',
            'invitation_code': 'TESTCODE1234',
        },
    )

    # Assert
    assert response.status_code == 409
    assert 'Username already exists' in response.json()['detail']


async def test_login_success(client: AsyncClient, api_session: AsyncSession, password_hasher: Sha256PasswordHasher):
    """
    GIVEN an active, authenticated user exists
    WHEN logging in with correct credentials via form data
    THEN it should return 200 with access and refresh tokens
    """
    # Arrange
    await create_test_user(
        api_session,
        password_hasher,
        username='loginuser',
        email='login@example.com',
        password='Test1234!',
        is_authenticated=True,
        is_active=True,
    )

    # Act
    response = await client.post(
        '/auth/login',
        data={
            'username': 'loginuser',
            'password': 'Test1234!',
        },
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['token_type'] == 'bearer'


async def test_login_wrong_password(
    client: AsyncClient, api_session: AsyncSession, password_hasher: Sha256PasswordHasher
):
    """
    GIVEN a user exists with a known password
    WHEN logging in with the wrong password via form data
    THEN it should return 401 Unauthorized
    """
    # Arrange
    await create_test_user(
        api_session,
        password_hasher,
        username='loginuser2',
        email='login2@example.com',
        password='Test1234!',
    )

    # Act
    response = await client.post(
        '/auth/login',
        data={
            'username': 'loginuser2',
            'password': 'WrongPass1!',
        },
    )

    # Assert
    assert response.status_code == 401


async def test_activate_account(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a non-authenticated user and a valid activation token
    WHEN posting the activation token to the activate endpoint
    THEN it should return 200 with a success message
    """
    # Arrange
    user = await create_test_user(
        api_session,
        password_hasher,
        username='activateuser',
        email='activate@example.com',
        is_authenticated=False,
    )
    activation_token = token_service.create_activation_token(user.id)

    # Act
    response = await client.post(
        '/auth/activate',
        json={'token': activation_token},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()['message'] == 'Account activated successfully'


async def test_refresh_token(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a user exists and holds a valid refresh token
    WHEN posting the refresh token to the refresh endpoint
    THEN it should return 200 with new access and refresh tokens
    """
    # Arrange
    user = await create_test_user(
        api_session,
        password_hasher,
        username='refreshuser',
        email='refresh@example.com',
    )
    refresh_tok = token_service.create_refresh_token(user.id)

    # Act
    response = await client.post(
        '/auth/refresh',
        json={'refresh_token': refresh_tok},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data


async def test_check_availability(
    client: AsyncClient, api_session: AsyncSession, password_hasher: Sha256PasswordHasher
):
    """
    GIVEN a user with username 'takenuser' exists
    WHEN GET /auth/availability?username=takenuser&email=free@example.com is requested
    THEN it should return username_taken=True and email_taken=False
    """
    # Arrange
    await create_test_user(
        api_session,
        password_hasher,
        username='takenuser',
        email='taken@example.com',
    )

    # Act
    response = await client.get(
        '/auth/availability',
        params={'username': 'takenuser', 'email': 'free@example.com'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['username_taken'] is True
    assert data['email_taken'] is False


async def test_resend_activation_success(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
):
    """
    GIVEN a non-activated user exists
    WHEN POST /auth/resend-activation is requested with their email
    THEN it should return 200 with a generic success message
    """
    # Arrange
    await create_test_user(
        api_session,
        password_hasher,
        username='resenduser',
        email='resend@example.com',
        is_authenticated=False,
    )

    # Act
    response = await client.post(
        '/auth/resend-activation',
        json={'email': 'resend@example.com'},
    )

    # Assert
    assert response.status_code == 200
    assert 'Activation email sent' in response.json()['message']


async def test_resend_activation_already_activated(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
):
    """
    GIVEN a user who is already activated
    WHEN POST /auth/resend-activation is requested with their email
    THEN it should return 400 indicating the account is already activated
    """
    # Arrange
    await create_test_user(
        api_session,
        password_hasher,
        username='activateduser',
        email='activated@example.com',
        is_authenticated=True,
    )

    # Act
    response = await client.post(
        '/auth/resend-activation',
        json={'email': 'activated@example.com'},
    )

    # Assert
    assert response.status_code == 400
    assert 'already activated' in response.json()['detail']


async def test_resend_activation_unknown_email(
    client: AsyncClient,
):
    """
    GIVEN no user exists with the given email
    WHEN POST /auth/resend-activation is requested
    THEN it should return 200 with a generic message (no information leak)
    """
    # Act
    response = await client.post(
        '/auth/resend-activation',
        json={'email': 'unknown@example.com'},
    )

    # Assert
    assert response.status_code == 200
    assert 'Activation email sent' in response.json()['message']


async def test_request_password_reset_success(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
):
    """
    GIVEN a user exists with the given email
    WHEN POST /auth/request-password-reset is requested
    THEN it should return 200 with a generic success message
    """
    # Arrange
    await create_test_user(
        api_session,
        password_hasher,
        username='resetuser',
        email='reset@example.com',
    )

    # Act
    response = await client.post(
        '/auth/request-password-reset',
        json={'email': 'reset@example.com'},
    )

    # Assert
    assert response.status_code == 200
    assert 'Password reset email sent' in response.json()['message']


async def test_request_password_reset_unknown_email(
    client: AsyncClient,
):
    """
    GIVEN no user exists with the given email
    WHEN POST /auth/request-password-reset is requested
    THEN it should still return 200 (no information leak)
    """
    # Act
    response = await client.post(
        '/auth/request-password-reset',
        json={'email': 'nobody@example.com'},
    )

    # Assert
    assert response.status_code == 200
    assert 'Password reset email sent' in response.json()['message']


async def test_reset_password_success(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a user and a valid password reset token
    WHEN POST /auth/reset-password is requested with a new password
    THEN it should return 200 and the user can log in with the new password
    """
    # Arrange
    user = await create_test_user(
        api_session,
        password_hasher,
        username='resetpwuser',
        email='resetpw@example.com',
        password='OldPass1!',
        is_authenticated=True,
        is_active=True,
    )
    reset_token = token_service.create_password_reset_token(user.id)

    # Act
    response = await client.post(
        '/auth/reset-password',
        json={
            'token': reset_token,
            'password': 'NewPass1!',
            'confirm_password': 'NewPass1!',
        },
    )

    # Assert
    assert response.status_code == 200
    assert 'Password reset successfully' in response.json()['message']

    # Verify new password works
    login_resp = await client.post(
        '/auth/login',
        data={'username': 'resetpwuser', 'password': 'NewPass1!'},
    )
    assert login_resp.status_code == 200


async def test_reset_password_mismatch(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a valid password reset token
    WHEN POST /auth/reset-password is requested with mismatched passwords
    THEN it should return 400
    """
    # Arrange
    user = await create_test_user(
        api_session,
        password_hasher,
        username='mismatchuser',
        email='mismatch@example.com',
    )
    reset_token = token_service.create_password_reset_token(user.id)

    # Act
    response = await client.post(
        '/auth/reset-password',
        json={
            'token': reset_token,
            'password': 'NewPass1!',
            'confirm_password': 'Different1!',
        },
    )

    # Assert
    assert response.status_code == 400
    assert 'do not match' in response.json()['detail']


async def test_reset_password_invalid_token(
    client: AsyncClient,
):
    """
    GIVEN an invalid password reset token
    WHEN POST /auth/reset-password is requested
    THEN it should return 400
    """
    # Act
    response = await client.post(
        '/auth/reset-password',
        json={
            'token': 'invalid-token',
            'password': 'NewPass1!',
            'confirm_password': 'NewPass1!',
        },
    )

    # Assert
    assert response.status_code == 400
    assert 'Invalid or expired' in response.json()['detail']


async def test_login_deactivated_account(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
):
    """
    GIVEN a user with is_active=False and is_authenticated=True
    WHEN logging in with correct credentials
    THEN it should return 403 Forbidden indicating the account is deactivated
    """
    # Arrange
    await create_test_user(
        api_session,
        password_hasher,
        username='deactivated_user',
        email='deactivated@example.com',
        password='Test1234!',
        is_authenticated=True,
        is_active=False,
    )

    # Act
    response = await client.post(
        '/auth/login',
        data={
            'username': 'deactivated_user',
            'password': 'Test1234!',
        },
    )

    # Assert
    assert response.status_code == 403
    assert 'deactivated' in response.json()['detail'].lower()


async def test_login_not_activated_account(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
):
    """
    GIVEN a user with is_authenticated=False and is_active=True
    WHEN logging in with correct credentials
    THEN it should return 403 Forbidden indicating the account is not activated
    """
    # Arrange
    await create_test_user(
        api_session,
        password_hasher,
        username='not_activated_user',
        email='not_activated@example.com',
        password='Test1234!',
        is_authenticated=False,
        is_active=True,
    )

    # Act
    response = await client.post(
        '/auth/login',
        data={
            'username': 'not_activated_user',
            'password': 'Test1234!',
        },
    )

    # Assert
    assert response.status_code == 403
    assert 'not activated' in response.json()['detail'].lower()


async def test_activate_with_invalid_token(
    client: AsyncClient,
):
    """
    GIVEN an invalid activation token string
    WHEN POST /auth/activate is requested with that token
    THEN it should return 400 Bad Request
    """
    # Arrange
    invalid_token = 'invalid-token-string'

    # Act
    response = await client.post(
        '/auth/activate',
        json={'token': invalid_token},
    )

    # Assert
    assert response.status_code == 400


async def test_refresh_with_invalid_token(
    client: AsyncClient,
):
    """
    GIVEN an invalid JWT refresh token string
    WHEN POST /auth/refresh is requested with that token
    THEN it should return 400 Bad Request
    """
    # Arrange
    invalid_token = 'not-a-valid-jwt'

    # Act
    response = await client.post(
        '/auth/refresh',
        json={'refresh_token': invalid_token},
    )

    # Assert
    assert response.status_code == 400
