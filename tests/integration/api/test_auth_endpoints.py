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
        '/api/auth/register',
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
        '/api/auth/register',
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
    WHEN logging in with correct credentials
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
        '/api/auth/login',
        json={
            'primary': 'loginuser',
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
    WHEN logging in with the wrong password
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
        '/api/auth/login',
        json={
            'primary': 'loginuser2',
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
        '/api/auth/activate',
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
        '/api/auth/refresh',
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
    WHEN checking availability for that username and a free email
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
    response = await client.post(
        '/api/auth/check-availability',
        json={'username': 'takenuser', 'email': 'free@example.com'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['username_taken'] is True
    assert data['email_taken'] is False
