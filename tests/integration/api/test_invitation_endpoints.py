from datetime import datetime, timedelta

from app.core.entities.invitation_code import InvitationCode
from app.infrastructure.password_hasher import Sha256PasswordHasher
from app.infrastructure.token_service import JwtTokenService
from app.repository.invitation_repository import SqlAlchemyInvitationRepository
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
    WHEN GET /invitation/codes/{code} is requested
    THEN it should return 200 with the invitation code details
    """
    # Arrange
    invitation = await create_test_invitation_code(api_session)

    # Act
    response = await client.get(f'/invitation/codes/{invitation.code}')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['code'] == invitation.code
    assert data['is_disabled'] is False


async def test_update_invitation_code_status(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an admin manager user and an existing invitation code
    WHEN updating the code's disabled status to True via PATCH
    THEN it should return 200 with the updated invitation code showing is_disabled=True
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
    data = response.json()
    assert data['is_disabled'] is True
    assert data['id'] == invitation.id


async def test_list_invitation_codes(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an admin user and invitation codes exist
    WHEN GET /invitation/codes is requested
    THEN it should return 200 with a list of all invitation codes
    """
    # Arrange
    token, admin = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='listadmin',
        email='listadmin@example.com',
        is_admin=True,
        is_manager=True,
    )
    await create_test_invitation_code(api_session, created_by=admin.id)

    # Act
    response = await client.get(
        '/invitation/codes',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert 'code' in data[0]
    assert 'is_disabled' in data[0]


async def test_list_codes_as_non_manager(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a regular (non-manager) authenticated user
    WHEN requesting GET /invitation/codes
    THEN it should return 403 Forbidden
    """
    # Arrange
    token, _user = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='regular_user',
        email='regular@example.com',
        is_admin=False,
        is_manager=False,
    )

    # Act
    response = await client.get(
        '/invitation/codes',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 403


async def test_generate_code_as_non_manager(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a regular (non-manager) authenticated user
    WHEN requesting POST /invitation/codes
    THEN it should return 403 Forbidden
    """
    # Arrange
    token, _user = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='nonadmin_user',
        email='nonadmin@example.com',
        is_admin=False,
        is_manager=False,
    )

    # Act
    response = await client.post(
        '/invitation/codes',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 403


async def test_get_expired_invitation_code(
    client: AsyncClient,
    api_session: AsyncSession,
):
    """
    GIVEN an invitation code that has already expired
    WHEN GET /invitation/codes/{code} is requested
    THEN it should return 410 Gone
    """
    # Arrange
    repo = SqlAlchemyInvitationRepository(api_session)
    expired_invitation = InvitationCode(
        id=0,
        code='EXPIREDCODE1',
        created_by=1,
        expires_at=datetime.now() - timedelta(hours=1),
    )
    created = await repo.create(expired_invitation)

    # Act
    response = await client.get(f'/invitation/codes/{created.code}')

    # Assert
    assert response.status_code == 410


async def test_get_disabled_invitation_code(
    client: AsyncClient,
    api_session: AsyncSession,
):
    """
    GIVEN an invitation code that is disabled
    WHEN GET /invitation/codes/{code} is requested
    THEN it should return 410 Gone
    """
    # Arrange
    repo = SqlAlchemyInvitationRepository(api_session)
    disabled_invitation = InvitationCode(
        id=0,
        code='DISABLEDCD01',
        created_by=1,
        expires_at=datetime.now() + timedelta(hours=48),
        is_disabled=True,
    )
    created = await repo.create(disabled_invitation)

    # Act
    response = await client.get(f'/invitation/codes/{created.code}')

    # Assert
    assert response.status_code == 410


async def test_get_nonexistent_invitation_code(
    client: AsyncClient,
):
    """
    GIVEN no invitation code with code 'NONEXISTENT' exists
    WHEN GET /invitation/codes/NONEXISTENT is requested
    THEN it should return 404 Not Found
    """
    # Act
    response = await client.get('/invitation/codes/NONEXISTENT')

    # Assert
    assert response.status_code == 404


async def test_update_nonexistent_invitation_code(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an admin user and no invitation code with id 99999 exists
    WHEN PATCH /invitation/codes/99999 is requested with is_disabled=True
    THEN it should return 400 Bad Request
    """
    # Arrange
    token, _admin = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='updateadmin',
        email='updateadmin@example.com',
        is_admin=True,
        is_manager=True,
    )

    # Act
    response = await client.patch(
        '/invitation/codes/99999',
        json={'is_disabled': True},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 400
