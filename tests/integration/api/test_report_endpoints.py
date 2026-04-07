from app.infrastructure.password_hasher import Sha256PasswordHasher
from app.infrastructure.token_service import JwtTokenService
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import get_auth_token


async def test_list_reports_as_admin(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an admin user and a report exists
    WHEN GET /admin/reports is requested
    THEN it returns 200 with the list of all reports
    """
    # Arrange – create a normal user and submit a report
    user_token, _user = await get_auth_token(
        api_session, password_hasher, token_service, username='reporter', email='reporter@example.com'
    )
    await client.post(
        '/reports/',
        json={'description': 'Wrong lyrics in verse 2', 'song_sid': '1011054'},
        headers={'Authorization': f'Bearer {user_token}'},
    )

    # Arrange – get admin token
    admin_token, _admin = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='reportadmin',
        email='reportadmin@example.com',
        is_admin=True,
        is_manager=True,
    )

    # Act
    response = await client.get(
        '/admin/reports',
        headers={'Authorization': f'Bearer {admin_token}'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]['song_sid'] == '1011054'


async def test_list_reports_requires_admin(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a non-admin user
    WHEN GET /admin/reports is requested
    THEN it returns 403
    """
    # Arrange
    token, _user = await get_auth_token(
        api_session, password_hasher, token_service, username='normalreport', email='normalreport@example.com'
    )

    # Act
    response = await client.get(
        '/admin/reports',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 403


async def test_create_report(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an authenticated user
    WHEN creating a song report via POST /reports/
    THEN it should return 201 with the report data including the user's id
    """
    # Arrange
    token, user = await get_auth_token(api_session, password_hasher, token_service)

    # Act
    response = await client.post(
        '/reports/',
        json={
            'description': 'This song has wrong lyrics in verse 2',
            'song_sid': '1011054',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data['description'] == 'This song has wrong lyrics in verse 2'
    assert data['song_sid'] == '1011054'
    assert data['user_id'] == user.id
