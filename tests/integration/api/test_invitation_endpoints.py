from app.infrastructure.password_hasher import Sha256PasswordHasher
from app.infrastructure.token_service import JwtTokenService
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import create_test_invitation_code, get_auth_token


async def test_generate_invitation_code(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an admin manager user
    WHEN requesting POST /invitation/codes
    THEN it should return 201 with a generated 12-character invitation code and expiry
    """
    # Arrange
    token, _admin = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='invadmin',
        email='invadmin@example.com',
        is_admin=True,
        is_manager=True,
    )

    # Act
    response = await client.post(
        '/invitation/codes',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert 'code' in data
    assert 'expires_at' in data
    assert len(data['code']) == 12


async def test_validate_invitation_code(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
):
    """
    GIVEN a valid invitation code exists
    WHEN validating the code via GET /invitation/validate/{code}
    THEN it should return 200 with a validity message
    """
    # Arrange
    invitation = await create_test_invitation_code(api_session)

    # Act
    response = await client.get(f'/invitation/validate/{invitation.code}')

    # Assert
    assert response.status_code == 200
    assert response.json()['message'] == 'Invitation code is valid'


async def test_toggle_invitation_code(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an admin manager user and an existing invitation code
    WHEN toggling the code's disabled status to True
    THEN it should return 200 with a disabled confirmation message
    """
    # Arrange
    token, admin = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='togadmin',
        email='togadmin@example.com',
        is_admin=True,
        is_manager=True,
    )
    invitation = await create_test_invitation_code(api_session, created_by=admin.id)

    # Act
    response = await client.patch(
        f'/invitation/codes/{invitation.id}',
        json={'is_disabled': True},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    assert 'disabled' in response.json()['message']
