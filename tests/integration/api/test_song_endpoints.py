from app.core.entities.music_version import MusicVersion
from app.core.entities.music_work import MusicWork
from app.infrastructure.password_hasher import Sha256PasswordHasher
from app.infrastructure.token_service import JwtTokenService
from app.repository.song_repository import SqlAlchemySongRepository
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import get_auth_token


def _make_work(
    title_original: str = '我獻上我心',
    composer: str | None = 'Reuben Morgan',
    lyricist: str | None = 'Reuben Morgan',
) -> MusicWork:
    return MusicWork(
        id=0,
        title_original=title_original,
        composer=composer,
        lyricist=lyricist,
    )


def _make_version(
    sid: str = '1011054',
    num_c: str = '11',
    num_i: str = '54',
    title: str = '我獻上我心',
    language: str | None = 'Chinese',
    tonality: str | None = 'G',
) -> MusicVersion:
    return MusicVersion(
        id=0,
        work_id=0,
        sid=sid,
        num_c=num_c,
        num_i=num_i,
        title=title,
        language=language,
        tonality=tonality,
        lyrics=['p', '我心何等渴望'],
    )


async def _seed_song(session: AsyncSession, sid: str = '1011054', title: str = '我獻上我心') -> MusicVersion:
    """Insert a song via the repository and return the created entity."""
    repo = SqlAlchemySongRepository(session)
    return await repo.create(_make_version(sid=sid, title=title), _make_work(title_original=title))


async def _get_user_token(
    session: AsyncSession,
    hasher: Sha256PasswordHasher,
    token_svc: JwtTokenService,
) -> str:
    token, _user = await get_auth_token(session, hasher, token_svc)
    return token


async def _get_manager_token(
    session: AsyncSession,
    hasher: Sha256PasswordHasher,
    token_svc: JwtTokenService,
    username: str = 'manager',
    email: str = 'manager@example.com',
) -> str:
    token, _user = await get_auth_token(session, hasher, token_svc, username=username, email=email, is_manager=True)
    return token


# ── GET /api/songs/random ─────────────────────────────


class TestGetRandomSongs:
    async def test_returns_songs_with_token(
        self,
        client: AsyncClient,
        api_session: AsyncSession,
        password_hasher: Sha256PasswordHasher,
        token_service: JwtTokenService,
    ):
        """
        GIVEN songs exist and user is authenticated
        WHEN GET /api/songs/random is requested
        THEN it returns a list of songs
        """
        # Arrange
        await _seed_song(api_session, sid='1011054')
        await _seed_song(api_session, sid='1010066', title='前來敬拜')
        token = await _get_user_token(api_session, password_hasher, token_service)

        # Act
        response = await client.get(
            '/api/songs/random?amount=2',
            headers={'Authorization': f'Bearer {token}'},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2
        assert all('sid' in song for song in data)

    async def test_returns_empty_without_token(self, client: AsyncClient):
        """
        GIVEN no authentication token is provided
        WHEN GET /api/songs/random is requested
        THEN it returns an empty list
        """
        # Arrange & Act
        response = await client.get('/api/songs/random')

        # Assert
        assert response.status_code == 200
        assert response.json() == []


# ── GET /api/songs/search ─────────────────────────────


class TestSearchSongs:
    async def test_search_by_title(
        self,
        client: AsyncClient,
        api_session: AsyncSession,
        password_hasher: Sha256PasswordHasher,
        token_service: JwtTokenService,
    ):
        """
        GIVEN a song with title '我獻上我心' exists
        WHEN GET /api/songs/search?mode=title&q=獻上 is requested
        THEN the matching song is returned
        """
        # Arrange
        await _seed_song(api_session)
        token = await _get_user_token(api_session, password_hasher, token_service)

        # Act
        response = await client.get(
            '/api/songs/search?mode=title&q=獻上',
            headers={'Authorization': f'Bearer {token}'},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['sid'] == '1011054'

    async def test_search_requires_auth(self, client: AsyncClient):
        """
        GIVEN no authentication token is provided
        WHEN GET /api/songs/search is requested
        THEN it returns 401
        """
        # Arrange & Act
        response = await client.get('/api/songs/search?mode=title&q=test')

        # Assert
        assert response.status_code == 401


# ── GET /api/songs/browse ─────────────────────────────


class TestBrowseSongs:
    async def test_browse_by_language(
        self,
        client: AsyncClient,
        api_session: AsyncSession,
        password_hasher: Sha256PasswordHasher,
        token_service: JwtTokenService,
    ):
        """
        GIVEN a Chinese song exists
        WHEN GET /api/songs/browse?lang=Chinese is requested
        THEN the matching song is returned
        """
        # Arrange
        await _seed_song(api_session)
        token = await _get_user_token(api_session, password_hasher, token_service)

        # Act
        response = await client.get(
            '/api/songs/browse?lang=Chinese',
            headers={'Authorization': f'Bearer {token}'},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['language'] == 'Chinese'

    async def test_browse_requires_auth(self, client: AsyncClient):
        """
        GIVEN no authentication token is provided
        WHEN GET /api/songs/browse is requested
        THEN it returns 401
        """
        # Arrange & Act
        response = await client.get('/api/songs/browse')

        # Assert
        assert response.status_code == 401


# ── GET /api/songs/{sid} ──────────────────────────────


class TestGetSongBySid:
    async def test_get_existing_song(
        self,
        client: AsyncClient,
        api_session: AsyncSession,
        password_hasher: Sha256PasswordHasher,
        token_service: JwtTokenService,
    ):
        """
        GIVEN a song with SID '1011054' exists
        WHEN GET /api/songs/1011054 is requested
        THEN the song is returned with all fields
        """
        # Arrange
        await _seed_song(api_session)
        token = await _get_user_token(api_session, password_hasher, token_service)

        # Act
        response = await client.get(
            '/api/songs/1011054',
            headers={'Authorization': f'Bearer {token}'},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['sid'] == '1011054'
        assert data['title'] == '我獻上我心'
        assert data['composer'] == 'Reuben Morgan'

    async def test_get_nonexistent_song(
        self,
        client: AsyncClient,
        api_session: AsyncSession,
        password_hasher: Sha256PasswordHasher,
        token_service: JwtTokenService,
    ):
        """
        GIVEN no song with SID '9999999' exists
        WHEN GET /api/songs/9999999 is requested
        THEN it returns 404
        """
        # Arrange
        token = await _get_user_token(api_session, password_hasher, token_service)

        # Act
        response = await client.get(
            '/api/songs/9999999',
            headers={'Authorization': f'Bearer {token}'},
        )

        # Assert
        assert response.status_code == 404

    async def test_get_song_requires_auth(self, client: AsyncClient):
        """
        GIVEN no authentication token is provided
        WHEN GET /api/songs/1011054 is requested
        THEN it returns 401
        """
        # Arrange & Act
        response = await client.get('/api/songs/1011054')

        # Assert
        assert response.status_code == 401


# ── POST /api/admin/songs ─────────────────────────────


class TestCreateSong:
    async def test_create_song_as_manager(
        self,
        client: AsyncClient,
        api_session: AsyncSession,
        password_hasher: Sha256PasswordHasher,
        token_service: JwtTokenService,
    ):
        """
        GIVEN a manager user is authenticated
        WHEN POST /api/admin/songs is requested with song data
        THEN the song is created and the new SID is returned
        """
        # Arrange
        token = await _get_manager_token(api_session, password_hasher, token_service)

        # Act
        response = await client.post(
            '/api/admin/songs',
            json={
                'sid': '9990001',
                'title': '新歌',
                'num_c': '99',
                'num_i': '1',
                'composer': 'Test Composer',
                'lyricist': 'Test Lyricist',
            },
            headers={'Authorization': f'Bearer {token}'},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['NewSID'] == '9990001'

    async def test_create_song_requires_manager(
        self,
        client: AsyncClient,
        api_session: AsyncSession,
        password_hasher: Sha256PasswordHasher,
        token_service: JwtTokenService,
    ):
        """
        GIVEN a normal (non-manager) user is authenticated
        WHEN POST /api/admin/songs is requested
        THEN it returns 403
        """
        # Arrange
        token = await _get_user_token(api_session, password_hasher, token_service)

        # Act
        response = await client.post(
            '/api/admin/songs',
            json={'sid': '9990002', 'title': '新歌', 'num_c': '99', 'num_i': '2'},
            headers={'Authorization': f'Bearer {token}'},
        )

        # Assert
        assert response.status_code == 403


# ── PUT /api/admin/songs/{sid} ────────────────────────


class TestUpdateSong:
    async def test_update_song_as_manager(
        self,
        client: AsyncClient,
        api_session: AsyncSession,
        password_hasher: Sha256PasswordHasher,
        token_service: JwtTokenService,
    ):
        """
        GIVEN a song exists and a manager is authenticated
        WHEN PUT /api/admin/songs/{sid} is requested with updated fields
        THEN the song is updated and success is returned
        """
        # Arrange
        await _seed_song(api_session)
        token = await _get_manager_token(api_session, password_hasher, token_service)

        # Act
        response = await client.put(
            '/api/admin/songs/1011054',
            json={'tonality': 'A', 'album': '新專輯'},
            headers={'Authorization': f'Bearer {token}'},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True

    async def test_update_song_requires_manager(
        self,
        client: AsyncClient,
        api_session: AsyncSession,
        password_hasher: Sha256PasswordHasher,
        token_service: JwtTokenService,
    ):
        """
        GIVEN a normal user is authenticated
        WHEN PUT /api/admin/songs/{sid} is requested
        THEN it returns 403
        """
        # Arrange
        token = await _get_user_token(api_session, password_hasher, token_service)

        # Act
        response = await client.put(
            '/api/admin/songs/1011054',
            json={'tonality': 'A'},
            headers={'Authorization': f'Bearer {token}'},
        )

        # Assert
        assert response.status_code == 403


# ── DELETE /api/admin/songs/{sid} ─────────────────────


class TestDeleteSong:
    async def test_delete_song_as_manager(
        self,
        client: AsyncClient,
        api_session: AsyncSession,
        password_hasher: Sha256PasswordHasher,
        token_service: JwtTokenService,
    ):
        """
        GIVEN a song exists and a manager is authenticated
        WHEN DELETE /api/admin/songs/{sid} is requested
        THEN the song is deleted and success is returned
        """
        # Arrange
        await _seed_song(api_session)
        token = await _get_manager_token(api_session, password_hasher, token_service)

        # Act
        response = await client.delete(
            '/api/admin/songs/1011054',
            headers={'Authorization': f'Bearer {token}'},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True

    async def test_delete_nonexistent_song(
        self,
        client: AsyncClient,
        api_session: AsyncSession,
        password_hasher: Sha256PasswordHasher,
        token_service: JwtTokenService,
    ):
        """
        GIVEN no song with the given SID exists
        WHEN DELETE /api/admin/songs/{sid} is requested by a manager
        THEN it returns 404
        """
        # Arrange
        token = await _get_manager_token(api_session, password_hasher, token_service)

        # Act
        response = await client.delete(
            '/api/admin/songs/9999999',
            headers={'Authorization': f'Bearer {token}'},
        )

        # Assert
        assert response.status_code == 404

    async def test_delete_song_requires_manager(
        self,
        client: AsyncClient,
        api_session: AsyncSession,
        password_hasher: Sha256PasswordHasher,
        token_service: JwtTokenService,
    ):
        """
        GIVEN a normal user is authenticated
        WHEN DELETE /api/admin/songs/{sid} is requested
        THEN it returns 403
        """
        # Arrange
        token = await _get_user_token(api_session, password_hasher, token_service)

        # Act
        response = await client.delete(
            '/api/admin/songs/1011054',
            headers={'Authorization': f'Bearer {token}'},
        )

        # Assert
        assert response.status_code == 403
