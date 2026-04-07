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
    WHEN creating a songlist via POST /songlists/
    THEN it should return 201 with the songlist data including a generated out_id
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)

    # Act
    response = await client.post(
        '/songlists/',
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
    WHEN requesting GET /songlists/
    THEN it should return 200 with both songlists
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    await client.post(
        '/songlists/',
        json={'title': 'Songlist 1'},
        headers={'Authorization': f'Bearer {token}'},
    )
    await client.post(
        '/songlists/',
        json={'title': 'Songlist 2'},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Act
    response = await client.get(
        '/songlists/',
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
    WHEN requesting GET /songlists/{out_id}
    THEN it should return 200 with the songlist details
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    create_resp = await client.post(
        '/songlists/',
        json={'title': 'Detail Songlist'},
        headers={'Authorization': f'Bearer {token}'},
    )
    out_id = create_resp.json()['out_id']

    # Act
    response = await client.get(
        f'/songlists/{out_id}',
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
        '/songlists/',
        json={'title': 'To Delete'},
        headers={'Authorization': f'Bearer {token}'},
    )
    out_id = create_resp.json()['out_id']

    # Act
    response = await client.delete(
        f'/songlists/{out_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()['message'] == 'Songlist deleted successfully'

    get_resp = await client.get(
        f'/songlists/{out_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert get_resp.status_code == 404


async def test_update_songlist_partial(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a songlist exists for an authenticated user
    WHEN PATCH /songlists/{out_id} is requested with only a new title
    THEN it should return 200 with the title updated and other fields unchanged
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    create_resp = await client.post(
        '/songlists/',
        json={'title': 'Original Title'},
        headers={'Authorization': f'Bearer {token}'},
    )
    out_id = create_resp.json()['out_id']

    # Act
    response = await client.patch(
        f'/songlists/{out_id}',
        json={'title': 'Updated Title'},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Updated Title'
    assert data['is_private'] is False  # unchanged


async def test_add_song_to_songlist(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a songlist exists for an authenticated user
    WHEN PUT /songlists/{out_id}/songs/{sid} is requested
    THEN the song is added and the updated songlist is returned
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    create_resp = await client.post(
        '/songlists/',
        json={'title': 'Song Sub-resource Songlist'},
        headers={'Authorization': f'Bearer {token}'},
    )
    out_id = create_resp.json()['out_id']

    # Act
    response = await client.put(
        f'/songlists/{out_id}/songs/123',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert '123' in data['songs_sid_list']
    assert data['songs_amount'] == 1


async def test_add_song_idempotent(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a song is already in the songlist
    WHEN PUT /songlists/{out_id}/songs/{sid} is requested again
    THEN the song is still present (idempotent) and amount unchanged
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    create_resp = await client.post(
        '/songlists/',
        json={'title': 'Idempotent Songlist'},
        headers={'Authorization': f'Bearer {token}'},
    )
    out_id = create_resp.json()['out_id']
    await client.put(
        f'/songlists/{out_id}/songs/123',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Act — add same song again
    response = await client.put(
        f'/songlists/{out_id}/songs/123',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['songs_sid_list'].count('123') == 1
    assert data['songs_amount'] == 1


async def test_remove_song_from_songlist(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a songlist contains song '123'
    WHEN DELETE /songlists/{out_id}/songs/123 is requested
    THEN the song is removed and the updated songlist is returned
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    create_resp = await client.post(
        '/songlists/',
        json={'title': 'Remove Song Songlist'},
        headers={'Authorization': f'Bearer {token}'},
    )
    out_id = create_resp.json()['out_id']
    await client.put(
        f'/songlists/{out_id}/songs/123',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Act
    response = await client.delete(
        f'/songlists/{out_id}/songs/123',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert '123' not in data['songs_sid_list']
    assert data['songs_amount'] == 0


async def test_remove_song_idempotent(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a songlist does not contain song '999'
    WHEN DELETE /songlists/{out_id}/songs/999 is requested
    THEN it returns 200 with the songlist unchanged (idempotent)
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    create_resp = await client.post(
        '/songlists/',
        json={'title': 'Idempotent Remove Songlist'},
        headers={'Authorization': f'Bearer {token}'},
    )
    out_id = create_resp.json()['out_id']

    # Act
    response = await client.delete(
        f'/songlists/{out_id}/songs/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['songs_amount'] == 0
