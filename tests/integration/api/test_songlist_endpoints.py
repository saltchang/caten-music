from app.infrastructure.password_hasher import Sha256PasswordHasher
from app.infrastructure.token_service import JwtTokenService
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import get_auth_token


async def test_create_songlist(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an authenticated user
    WHEN creating a songlist via POST /api/songlists/
    THEN it should return 201 with the songlist data including a generated out_id
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)

    # Act
    response = await client.post(
        '/api/songlists/',
        json={'title': 'My Songlist'},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == 'My Songlist'
    assert data['user_id'] == _user.id
    assert data['out_id'] is not None


async def test_get_songlists(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an authenticated user who owns two songlists
    WHEN requesting GET /api/songlists/
    THEN it should return 200 with both songlists
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    await client.post(
        '/api/songlists/',
        json={'title': 'Songlist 1'},
        headers={'Authorization': f'Bearer {token}'},
    )
    await client.post(
        '/api/songlists/',
        json={'title': 'Songlist 2'},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Act
    response = await client.get(
        '/api/songlists/',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


async def test_get_songlist_by_out_id(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a songlist exists for an authenticated user
    WHEN requesting GET /api/songlists/{out_id}
    THEN it should return 200 with the songlist details
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    create_resp = await client.post(
        '/api/songlists/',
        json={'title': 'Detail Songlist'},
        headers={'Authorization': f'Bearer {token}'},
    )
    out_id = create_resp.json()['out_id']

    # Act
    response = await client.get(
        f'/api/songlists/{out_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()['title'] == 'Detail Songlist'


async def test_delete_songlist(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a songlist exists for an authenticated user
    WHEN deleting the songlist and then fetching it
    THEN it should return 200 on delete and 404 on subsequent fetch

    Note: This test uses a multi-step pattern (delete then GET) to verify deletion.
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    create_resp = await client.post(
        '/api/songlists/',
        json={'title': 'To Delete'},
        headers={'Authorization': f'Bearer {token}'},
    )
    out_id = create_resp.json()['out_id']

    # Act
    response = await client.delete(
        f'/api/songlists/{out_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()['message'] == 'Songlist deleted successfully'

    get_resp = await client.get(
        f'/api/songlists/{out_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert get_resp.status_code == 404


async def test_toggle_song(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a songlist exists for an authenticated user
    WHEN toggling a song twice (add then remove)
    THEN the first toggle should add the song and the second should remove it

    Note: This test uses a multi-step pattern (toggle-add then toggle-remove) to verify
    both directions of the toggle behavior.
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    create_resp = await client.post(
        '/api/songlists/',
        json={'title': 'Toggle Songlist'},
        headers={'Authorization': f'Bearer {token}'},
    )
    out_id = create_resp.json()['out_id']

    # Act & Assert (toggle add)
    response = await client.put(
        f'/api/songlists/{out_id}/songs/123',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    data = response.json()
    assert data['action'] == 'add'
    assert data['song_sid'] == '123'

    # Act & Assert (toggle remove)
    response2 = await client.put(
        f'/api/songlists/{out_id}/songs/123',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response2.json()['action'] == 'remove'
