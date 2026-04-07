from app.infrastructure.password_hasher import Sha256PasswordHasher
from app.infrastructure.token_service import JwtTokenService
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import create_test_user, get_auth_token


async def test_list_users_as_admin(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an admin user and a normal user exist
    WHEN the admin requests GET /users
    THEN it should return 200 with all users
    """
    # Arrange
    token, _admin = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='adminuser',
        email='admin@example.com',
        is_admin=True,
        is_manager=True,
    )
    await create_test_user(
        api_session,
        password_hasher,
        username='normaluser',
        email='normal@example.com',
    )

    # Act
    response = await client.get(
        '/users',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


async def test_list_users_unauthorized(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a non-admin user
    WHEN the user requests GET /users
    THEN it should return 403 Forbidden
    """
    # Arrange
    token, _user = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='normaluser2',
        email='normal2@example.com',
        is_admin=False,
    )

    # Act
    response = await client.get(
        '/users',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 403


async def test_update_user_role(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an admin user and a normal target user
    WHEN the admin requests PATCH /users/{id} with role 'manager'
    THEN it should return 200 with is_manager=True and is_admin=False
    """
    # Arrange
    token, _admin = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='adminuser3',
        email='admin3@example.com',
        is_admin=True,
        is_manager=True,
    )
    target_user = await create_test_user(
        api_session,
        password_hasher,
        username='targetuser',
        email='target@example.com',
    )

    # Act
    response = await client.patch(
        f'/users/{target_user.id}',
        json={'role': 'manager'},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['is_manager'] is True
    assert data['is_admin'] is False


async def test_update_user_role_invalid(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an admin user
    WHEN the admin requests PATCH /users/{id} with an invalid role value
    THEN it should return 422 because role must be a valid UserRole enum
    """
    # Arrange
    token, _admin = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='adminuser4',
        email='admin4@example.com',
        is_admin=True,
        is_manager=True,
    )
    target_user = await create_test_user(
        api_session,
        password_hasher,
        username='targetuser2',
        email='target2@example.com',
    )

    # Act
    response = await client.patch(
        f'/users/{target_user.id}',
        json={'role': 'superadmin'},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 422


async def test_update_nonexistent_user(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an admin user and no user with id 99999 exists
    WHEN PATCH /users/99999 is requested with a role update
    THEN it should return 404 Not Found
    """
    # Arrange
    token, _admin = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='adminuser5',
        email='admin5@example.com',
        is_admin=True,
        is_manager=True,
    )

    # Act
    response = await client.patch(
        '/users/99999',
        json={'role': 'manager'},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 404
