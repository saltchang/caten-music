from unittest.mock import AsyncMock

import pytest
from app.core.entities.music_version import MusicVersion
from app.core.entities.music_work import MusicWork
from app.service.song_service import SongService


@pytest.fixture
def song_repo():
    return AsyncMock()


@pytest.fixture
def service(song_repo):
    return SongService(song_repo=song_repo)


def _make_version(
    sid: str = '1011054',
    title: str = '我獻上我心',
    composer: str = 'Reuben Morgan',
    lyricist: str = 'Reuben Morgan',
) -> MusicVersion:
    return MusicVersion(
        id=1,
        work_id=1,
        sid=sid,
        num_c='11',
        num_i='54',
        title=title,
        language='Chinese',
        translator='周巽光',
        album='這是真愛',
        tonality='G',
        lyrics=['p', '我心何等渴望'],
        work=MusicWork(
            id=1,
            title_original=title,
            composer=composer,
            lyricist=lyricist,
        ),
    )


class TestSearch:
    async def test_search_by_title(self, service, song_repo):
        """
        GIVEN the repository returns one song matching the title
        WHEN search is called with mode='title'
        THEN the repository search is called with title parameter
        """
        # Arrange
        song_repo.search.return_value = [_make_version()]

        # Act
        result = await service.search(mode='title', query='獻上')

        # Assert
        song_repo.search.assert_called_once_with(title='獻上')
        assert len(result) == 1

    async def test_search_by_lyric(self, service, song_repo):
        """
        GIVEN the repository returns one song matching the lyrics
        WHEN search is called with mode='lyric'
        THEN the repository search is called with lyrics parameter
        """
        # Arrange
        song_repo.search.return_value = [_make_version()]

        # Act
        result = await service.search(mode='lyric', query='渴望')

        # Assert
        song_repo.search.assert_called_once_with(lyrics='渴望')
        assert len(result) == 1

    async def test_search_invalid_mode(self, service, song_repo):
        """
        GIVEN an unsupported search mode
        WHEN search is called
        THEN an empty list is returned without calling the repository
        """
        # Arrange & Act
        result = await service.search(mode='invalid', query='test')

        # Assert
        assert result == []
        song_repo.search.assert_not_called()


class TestBrowse:
    async def test_browse_with_filters(self, service, song_repo):
        """
        GIVEN the repository returns songs matching the browse filters
        WHEN browse is called with lang, collection, and tonality
        THEN the repository search is called with all filters
        """
        # Arrange
        song_repo.search.return_value = [_make_version()]

        # Act
        result = await service.browse(lang='Chinese', collection='11', tonality='G')

        # Assert
        song_repo.search.assert_called_once_with(lang='Chinese', collection='11', tonality='G')
        assert len(result) == 1


class TestGetBySid:
    async def test_get_existing_song(self, service, song_repo):
        """
        GIVEN a song with the given SID exists
        WHEN get_by_sid is called
        THEN the matching version is returned
        """
        # Arrange
        song_repo.get_by_sid.return_value = _make_version()

        # Act
        result = await service.get_by_sid('1011054')

        # Assert
        assert result is not None
        assert result.sid == '1011054'

    async def test_get_nonexistent_song(self, service, song_repo):
        """
        GIVEN no song with the given SID exists
        WHEN get_by_sid is called
        THEN None is returned
        """
        # Arrange
        song_repo.get_by_sid.return_value = None

        # Act
        result = await service.get_by_sid('9999999')

        # Assert
        assert result is None


class TestGetBySids:
    async def test_get_multiple_songs(self, service, song_repo):
        """
        GIVEN two songs exist
        WHEN get_by_sids is called with both SIDs
        THEN both versions are returned
        """
        # Arrange
        song_repo.get_by_sids.return_value = [
            _make_version(sid='1011054'),
            _make_version(sid='1010066', title='前來敬拜'),
        ]

        # Act
        result = await service.get_by_sids(['1011054', '1010066'])

        # Assert
        assert len(result) == 2


class TestGetRandom:
    async def test_get_random_songs(self, service, song_repo):
        """
        GIVEN 3 songs exist
        WHEN get_random(2) is called
        THEN 2 versions are returned
        """
        # Arrange
        song_repo.get_random.return_value = [
            _make_version(sid='1011054'),
            _make_version(sid='1010066', title='前來敬拜'),
        ]

        # Act
        result = await service.get_random(2)

        # Assert
        song_repo.get_random.assert_called_once_with(2)
        assert len(result) == 2


class TestCreateSong:
    async def test_create_song(self, service, song_repo):
        """
        GIVEN valid song data
        WHEN create_song is called
        THEN a new version is created with associated work and the SID is returned
        """
        # Arrange
        created = _make_version(sid='9990001')
        song_repo.create.return_value = created

        data = {
            'sid': '9990001',
            'title': '新歌',
            'num_c': '99',
            'num_i': '1',
            'composer': 'Test',
            'lyricist': 'Test',
        }

        # Act
        new_sid = await service.create_song(data)

        # Assert
        assert new_sid == '9990001'
        song_repo.create.assert_called_once()


class TestDeleteSong:
    async def test_delete_existing_song(self, service, song_repo):
        """
        GIVEN a song with the given SID exists
        WHEN delete_song is called
        THEN the repository delete is called and True is returned
        """
        # Arrange
        song_repo.delete.return_value = True

        # Act
        result = await service.delete_song('1011054')

        # Assert
        assert result is True
        song_repo.delete.assert_called_once_with('1011054')

    async def test_delete_nonexistent_song(self, service, song_repo):
        """
        GIVEN no song with the given SID exists
        WHEN delete_song is called
        THEN False is returned
        """
        # Arrange
        song_repo.delete.return_value = False

        # Act
        result = await service.delete_song('9999999')

        # Assert
        assert result is False


class TestUpdateSong:
    async def test_update_song(self, service, song_repo):
        """
        GIVEN a song with the given SID exists
        WHEN update_song is called with modified fields
        THEN the repository update is called and True is returned
        """
        # Arrange
        existing = _make_version()
        song_repo.get_by_sid.return_value = existing
        song_repo.update.return_value = existing

        # Act
        result = await service.update_song('1011054', {'tonality': 'A', 'album': '新專輯'})

        # Assert
        assert result is True
        song_repo.update.assert_called_once()

    async def test_update_nonexistent_song(self, service, song_repo):
        """
        GIVEN no song with the given SID exists
        WHEN update_song is called
        THEN False is returned
        """
        # Arrange
        song_repo.get_by_sid.return_value = None

        # Act
        result = await service.update_song('9999999', {'tonality': 'A'})

        # Assert
        assert result is False
        song_repo.update.assert_not_called()
