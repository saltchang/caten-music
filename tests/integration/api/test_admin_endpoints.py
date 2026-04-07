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
    WHEN the admin requests GET /admin/users
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
        '/admin/users',
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
    WHEN the user requests GET /admin/users
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
        '/admin/users',
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
    WHEN the admin requests PUT /admin/users/{id} with role 'manager'
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
    response = await client.put(
        f'/admin/users/{target_user.id}',
        json={'role': 'manager'},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['is_manager'] is True
    assert data['is_admin'] is False
