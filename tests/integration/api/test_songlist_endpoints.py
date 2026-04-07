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
    WHEN creating a songlist via POST /songlists
    THEN it should return 201 with the songlist data including a generated out_id
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)

    # Act
    response = await client.post(
        '/songlists',
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
    WHEN requesting GET /songlists
    THEN it should return 200 with both songlists
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    await client.post(
        '/songlists',
        json={'title': 'Songlist 1'},
        headers={'Authorization': f'Bearer {token}'},
    )
    await client.post(
        '/songlists',
        json={'title': 'Songlist 2'},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Act
    response = await client.get(
        '/songlists',
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
        '/songlists',
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
    THEN it should return 204 No Content on delete and 404 on subsequent fetch
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)
    create_resp = await client.post(
        '/songlists',
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
    assert response.status_code == 204
    assert response.content == b''

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
        '/songlists',
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
        '/songlists',
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
        '/songlists',
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
        '/songlists',
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
        '/songlists',
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


async def test_get_other_users_private_songlist(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN User A owns a private songlist
    WHEN User B tries to GET /songlists/{out_id} for that songlist
    THEN it should return 403 Forbidden
    """
    # Arrange
    token_a, _user_a = await get_auth_token(
        api_session, password_hasher, token_service, username='owner_user', email='owner@example.com'
    )
    create_resp = await client.post(
        '/songlists',
        json={'title': 'Private Songlist', 'is_private': True},
        headers={'Authorization': f'Bearer {token_a}'},
    )
    out_id = create_resp.json()['out_id']

    token_b, _user_b = await get_auth_token(
        api_session, password_hasher, token_service, username='other_user', email='other@example.com'
    )

    # Act
    response = await client.get(
        f'/songlists/{out_id}',
        headers={'Authorization': f'Bearer {token_b}'},
    )

    # Assert
    assert response.status_code == 403


async def test_update_other_users_songlist(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN User A owns a songlist
    WHEN User B tries to PATCH /songlists/{out_id} for that songlist
    THEN it should return 403 Forbidden
    """
    # Arrange
    token_a, _user_a = await get_auth_token(
        api_session, password_hasher, token_service, username='patch_owner', email='patch_owner@example.com'
    )
    create_resp = await client.post(
        '/songlists',
        json={'title': 'Owner Songlist'},
        headers={'Authorization': f'Bearer {token_a}'},
    )
    out_id = create_resp.json()['out_id']

    token_b, _user_b = await get_auth_token(
        api_session, password_hasher, token_service, username='patch_intruder', email='patch_intruder@example.com'
    )

    # Act
    response = await client.patch(
        f'/songlists/{out_id}',
        json={'title': 'Hijacked Title'},
        headers={'Authorization': f'Bearer {token_b}'},
    )

    # Assert
    assert response.status_code == 403


async def test_delete_other_users_songlist(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN User A owns a songlist
    WHEN User B tries to DELETE /songlists/{out_id} for that songlist
    THEN it should return 403 Forbidden
    """
    # Arrange
    token_a, _user_a = await get_auth_token(
        api_session, password_hasher, token_service, username='del_owner', email='del_owner@example.com'
    )
    create_resp = await client.post(
        '/songlists',
        json={'title': 'Owner Only Songlist'},
        headers={'Authorization': f'Bearer {token_a}'},
    )
    out_id = create_resp.json()['out_id']

    token_b, _user_b = await get_auth_token(
        api_session, password_hasher, token_service, username='del_intruder', email='del_intruder@example.com'
    )

    # Act
    response = await client.delete(
        f'/songlists/{out_id}',
        headers={'Authorization': f'Bearer {token_b}'},
    )

    # Assert
    assert response.status_code == 403


async def test_patch_songlist_with_empty_body(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN a songlist exists for an authenticated user
    WHEN PATCH /songlists/{out_id} is requested with an empty JSON body
    THEN it returns 200 with no changes applied and the title remains unchanged
    """
    # Arrange
    token, _user = await get_auth_token(
        api_session,
        password_hasher,
        token_service,
        username='emptypatch',
        email='emptypatch@example.com',
    )
    create_resp = await client.post(
        '/songlists',
        json={'title': 'Unchanged Title'},
        headers={'Authorization': f'Bearer {token}'},
    )
    out_id = create_resp.json()['out_id']

    # Act
    response = await client.patch(
        f'/songlists/{out_id}',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Unchanged Title'


async def test_get_nonexistent_songlist(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an authenticated user
    WHEN GET /songlists/{out_id} is requested with a nonexistent out_id
    THEN it should return 404 Not Found
    """
    # Arrange
    token, _user = await get_auth_token(api_session, password_hasher, token_service)

    # Act
    response = await client.get(
        '/songlists/nonexistent-id',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 404


async def test_update_nonexistent_songlist(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an authenticated user
    WHEN PATCH /songlists/{out_id} is requested with a nonexistent out_id
    THEN it should return 404 Not Found
    """
    # Arrange
    token, _user = await get_auth_token(
        api_session, password_hasher, token_service, username='patchuser', email='patchuser@example.com'
    )

    # Act
    response = await client.patch(
        '/songlists/nonexistent-id',
        json={'title': 'Updated Title'},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 404


async def test_delete_nonexistent_songlist(
    client: AsyncClient,
    api_session: AsyncSession,
    password_hasher: Sha256PasswordHasher,
    token_service: JwtTokenService,
):
    """
    GIVEN an authenticated user
    WHEN DELETE /songlists/{out_id} is requested with a nonexistent out_id
    THEN it should return 404 Not Found
    """
    # Arrange
    token, _user = await get_auth_token(
        api_session, password_hasher, token_service, username='deluser', email='deluser@example.com'
    )

    # Act
    response = await client.delete(
        '/songlists/nonexistent-id',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == 404
