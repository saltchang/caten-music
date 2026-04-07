from unittest.mock import AsyncMock

import pytest
from app.core.entities.music_version import MusicVersion
from app.core.entities.music_work import MusicWork
from app.core.exceptions import SongNotFoundError
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


class TestListSongs:
    async def test_list_by_title(self, service, song_repo):
        """
        GIVEN the repository returns one song matching the title
        WHEN list_songs is called with title filter
        THEN the repository search is called with all parameters
        """
        # Arrange
        song_repo.search.return_value = [_make_version()]

        # Act
        result = await service.list_songs(title='獻上')

        # Assert
        song_repo.search.assert_called_once_with(
            title='獻上', lyrics='', lang='', collection='', tonality='', limit=50, offset=0
        )
        assert len(result) == 1

    async def test_list_by_lyrics(self, service, song_repo):
        """
        GIVEN the repository returns one song matching the lyrics
        WHEN list_songs is called with lyrics filter
        THEN the repository search is called with lyrics parameter
        """
        # Arrange
        song_repo.search.return_value = [_make_version()]

        # Act
        result = await service.list_songs(lyrics='渴望')

        # Assert
        song_repo.search.assert_called_once_with(
            title='', lyrics='渴望', lang='', collection='', tonality='', limit=50, offset=0
        )
        assert len(result) == 1

    async def test_list_with_combined_filters(self, service, song_repo):
        """
        GIVEN the repository returns songs matching combined filters
        WHEN list_songs is called with lang, collection, and tonality
        THEN the repository search is called with all filters
        """
        # Arrange
        song_repo.search.return_value = [_make_version()]

        # Act
        result = await service.list_songs(lang='Chinese', collection='11', tonality='G')

        # Assert
        song_repo.search.assert_called_once_with(
            title='', lyrics='', lang='Chinese', collection='11', tonality='G', limit=50, offset=0
        )
        assert len(result) == 1

    async def test_list_with_pagination(self, service, song_repo):
        """
        GIVEN pagination parameters are provided
        WHEN list_songs is called with limit and offset
        THEN the repository search is called with pagination
        """
        # Arrange
        song_repo.search.return_value = [_make_version()]

        # Act
        result = await service.list_songs(title='test', limit=10, offset=20)

        # Assert
        song_repo.search.assert_called_once_with(
            title='test', lyrics='', lang='', collection='', tonality='', limit=10, offset=20
        )
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
        GIVEN a valid MusicVersion and MusicWork entity
        WHEN create_song is called
        THEN the repository create is called and the created entity is returned
        """
        # Arrange
        created = _make_version(sid='9990001')
        song_repo.create.return_value = created
        version = MusicVersion(id=0, work_id=0, sid='9990001', num_c='99', num_i='1', title='新歌')
        work = MusicWork(id=0, title_original='新歌', composer='Test', lyricist='Test')

        # Act
        result = await service.create_song(version, work)

        # Assert
        assert result.sid == '9990001'
        song_repo.create.assert_called_once_with(version, work)


class TestDeleteSong:
    async def test_delete_existing_song(self, service, song_repo):
        """
        GIVEN a song with the given SID exists
        WHEN delete_song is called
        THEN the repository delete is called without error
        """
        # Arrange
        song_repo.delete.return_value = True

        # Act
        await service.delete_song('1011054')

        # Assert
        song_repo.delete.assert_called_once_with('1011054')

    async def test_delete_nonexistent_song(self, service, song_repo):
        """
        GIVEN no song with the given SID exists
        WHEN delete_song is called
        THEN SongNotFoundError is raised
        """
        # Arrange
        song_repo.delete.return_value = False

        # Act & Assert
        with pytest.raises(SongNotFoundError):
            await service.delete_song('9999999')


class TestUpdateSong:
    async def test_update_song(self, service, song_repo):
        """
        GIVEN a song with the given SID exists
        WHEN update_song is called with a MusicVersion carrying updated fields
        THEN the repository update is called and the updated entity is returned
        """
        # Arrange
        existing = _make_version()
        song_repo.get_by_sid.return_value = existing
        song_repo.update.return_value = existing
        update_version = MusicVersion(id=0, work_id=0, sid='', tonality='A', album='新專輯')

        # Act
        result = await service.update_song('1011054', update_version)

        # Assert
        assert result is not None
        song_repo.update.assert_called_once()

    async def test_update_nonexistent_song(self, service, song_repo):
        """
        GIVEN no song with the given SID exists
        WHEN update_song is called
        THEN SongNotFoundError is raised
        """
        # Arrange
        song_repo.get_by_sid.return_value = None
        update_version = MusicVersion(id=0, work_id=0, sid='', tonality='A')

        # Act & Assert
        with pytest.raises(SongNotFoundError):
            await service.update_song('9999999', update_version)
