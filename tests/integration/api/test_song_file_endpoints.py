from unittest.mock import MagicMock

from app.infrastructure.password_hasher import Sha256PasswordHasher
from app.infrastructure.token_service import JwtTokenService
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import get_auth_token


async def test_get_ppt_redirects(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
    mock_file_service: MagicMock,
):
    """
    GIVEN an authenticated user and a song with a PPT file
    WHEN GET /songs/{sid}/files/ppt is requested
    THEN it should return a redirect to the file URL
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    mock_file_service.get_ppt_url.return_value = 'https://dropbox.com/ppt/123.pptx'

    # Act
    response = await client.get(
        '/songs/123/files/ppt',
        headers={'Authorization': f'Bearer {token}'},
        follow_redirects=False,
    )

    # Assert
    assert response.status_code == 307
    assert response.headers['location'] == 'https://dropbox.com/ppt/123.pptx'
    mock_file_service.get_ppt_url.assert_called_once_with('123')


async def test_get_ppt_not_found(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
    mock_file_service: MagicMock,
):
    """
    GIVEN an authenticated user and a song without a PPT file
    WHEN GET /songs/{sid}/files/ppt is requested
    THEN it should return 404
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    mock_file_service.get_ppt_url.return_value = None

    # Act
    response = await client.get(
        '/songs/999/files/ppt',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 404


async def test_get_sheet_redirects(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
    mock_file_service: MagicMock,
):
    """
    GIVEN an authenticated user and a song with a sheet file
    WHEN GET /songs/{sid}/files/sheet is requested
    THEN it should return a redirect to the file URL
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    mock_file_service.get_sheet_url.return_value = 'https://dropbox.com/sheet/456.pdf'

    # Act
    response = await client.get(
        '/songs/456/files/sheet',
        headers={'Authorization': f'Bearer {token}'},
        follow_redirects=False,
    )

    # Assert
    assert response.status_code == 307
    assert response.headers['location'] == 'https://dropbox.com/sheet/456.pdf'
    mock_file_service.get_sheet_url.assert_called_once_with('456')


async def test_get_sheet_not_found(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
    mock_file_service: MagicMock,
):
    """
    GIVEN an authenticated user and a song without a sheet file
    WHEN GET /songs/{sid}/files/sheet is requested
    THEN it should return 404
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    mock_file_service.get_sheet_url.return_value = None

    # Act
    response = await client.get(
        '/songs/999/files/sheet',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 404


async def test_get_ppt_requires_auth(client: AsyncClient):
    """
    GIVEN no authentication token
    WHEN GET /songs/{sid}/files/ppt is requested
    THEN it should return 401
    """
    # Act
    response = await client.get('/songs/123/files/ppt')

    # Assert
    assert response.status_code == 401
