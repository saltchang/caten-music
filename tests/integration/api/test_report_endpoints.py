from app.infrastructure.password_hasher import Sha256PasswordHasher
from app.infrastructure.token_service import JwtTokenService
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import get_auth_token


async def test_create_report(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an authenticated user
    WHEN creating a song report via POST /api/reports/
    THEN it should return 201 with the report data including the user's id
    """
    # Arrange
    token, user = await get_auth_token(api_session, password_hasher, token_service)

    # Act
    response = await client.post(
        '/api/reports/',
        json={
            'description': 'This song has wrong lyrics in verse 2',
            'song_sid': 42,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data['description'] == 'This song has wrong lyrics in verse 2'
    assert data['song_sid'] == 42
    assert data['user_id'] == user.id
