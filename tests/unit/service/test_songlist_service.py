from unittest.mock import AsyncMock

import pytest
from app.core.entities.songlist import SongList
from app.core.exceptions import PermissionDeniedError, SonglistNotFoundError
from app.service.songlist_service import SonglistService


@pytest.fixture
def songlist_repo():
    return AsyncMock()


@pytest.fixture
def service(songlist_repo):
    return SonglistService(songlist_repo=songlist_repo)


@pytest.fixture
def sample_songlist():
    return SongList(
        id=1,
        out_id='20240101001',
        title='Test List',
        user_id=1,
        songs_sid_list=['1001001'],
        songs_amount=1,
    )


class TestCreateSonglist:
    async def test_create_songlist(self, service, songlist_repo):
        """
        GIVEN valid songlist data
        WHEN create_songlist is called
        THEN a new songlist is persisted and returned
        """
        # Arrange
        created = SongList(id=1, user_id=1, title='New List', out_id='20240101001')
        songlist_repo.create.return_value = created

        # Act
        result = await service.create_songlist(
            user_id=1,
            title='New List',
            song_sid='1001001',
            is_private=False,
        )

        # Assert
        assert result.title == 'New List'
        songlist_repo.create.assert_called_once()


class TestGetSonglist:
    async def test_get_by_out_id(self, service, songlist_repo, sample_songlist):
        """
        GIVEN an existing songlist with the given out_id
        WHEN get_songlist is called by the owner
        THEN the songlist is returned
        """
        # Arrange
        songlist_repo.get_by_out_id.return_value = sample_songlist

        # Act
        result = await service.get_songlist(out_id='20240101001', user_id=1)

        # Assert
        assert result.out_id == '20240101001'

    async def test_get_nonexistent(self, service, songlist_repo):
        """
        GIVEN no songlist exists with the given out_id
        WHEN get_songlist is called
        THEN SonglistNotFoundError is raised
        """
        # Arrange
        songlist_repo.get_by_out_id.return_value = None

        # Act & Assert
        with pytest.raises(SonglistNotFoundError):
            await service.get_songlist(out_id='nonexistent', user_id=1)

    async def test_get_private_by_non_owner(self, service, songlist_repo):
        """
        GIVEN a private songlist owned by another user
        WHEN get_songlist is called by a non-owner
        THEN PermissionDeniedError is raised
        """
        # Arrange
        private_list = SongList(
            id=1,
            out_id='20240101001',
            title='Private',
            user_id=1,
            is_private=True,
        )
        songlist_repo.get_by_out_id.return_value = private_list

        # Act & Assert
        with pytest.raises(PermissionDeniedError):
            await service.get_songlist(out_id='20240101001', user_id=999)

    async def test_get_user_songlists(self, service, songlist_repo, sample_songlist):
        """
        GIVEN a user who owns one songlist
        WHEN get_user_songlists is called
        THEN a list containing that songlist is returned
        """
        # Arrange
        songlist_repo.get_by_user_id.return_value = [sample_songlist]

        # Act
        result = await service.get_user_songlists(user_id=1)

        # Assert
        assert len(result) == 1


class TestEditSonglist:
    async def test_edit_by_owner(self, service, songlist_repo, sample_songlist):
        """
        GIVEN an existing songlist owned by the requesting user
        WHEN edit_songlist is called by the owner
        THEN the songlist is updated
        """
        # Arrange
        songlist_repo.get_by_out_id.return_value = sample_songlist
        songlist_repo.update.return_value = sample_songlist

        # Act
        await service.edit_songlist(
            out_id='20240101001',
            user_id=1,
            title='Updated',
            description='desc',
            is_private=False,
            is_archived=False,
            songs_sid_list=['1001001', '1001002'],
        )

        # Assert
        songlist_repo.update.assert_called_once()

    async def test_edit_by_non_owner(self, service, songlist_repo, sample_songlist):
        """
        GIVEN an existing songlist owned by another user
        WHEN edit_songlist is called by a non-owner
        THEN PermissionDeniedError is raised
        """
        # Arrange
        songlist_repo.get_by_out_id.return_value = sample_songlist

        # Act & Assert
        with pytest.raises(PermissionDeniedError):
            await service.edit_songlist(
                out_id='20240101001',
                user_id=999,
                title='Updated',
                description='desc',
                is_private=False,
                is_archived=False,
                songs_sid_list=[],
            )


class TestDeleteSonglist:
    async def test_delete_by_owner(self, service, songlist_repo, sample_songlist):
        """
        GIVEN an existing songlist owned by the requesting user
        WHEN delete_songlist is called by the owner
        THEN the songlist is deleted
        """
        # Arrange
        songlist_repo.get_by_out_id.return_value = sample_songlist

        # Act
        await service.delete_songlist(out_id='20240101001', user_id=1)

        # Assert
        songlist_repo.delete.assert_called_once_with(1)

    async def test_delete_by_non_owner(self, service, songlist_repo, sample_songlist):
        """
        GIVEN an existing songlist owned by another user
        WHEN delete_songlist is called by a non-owner
        THEN PermissionDeniedError is raised
        """
        # Arrange
        songlist_repo.get_by_out_id.return_value = sample_songlist

        # Act & Assert
        with pytest.raises(PermissionDeniedError):
            await service.delete_songlist(out_id='20240101001', user_id=999)


class TestToggleSong:
    async def test_add_song(self, service, songlist_repo, sample_songlist):
        """
        GIVEN a songlist that does not contain the given song
        WHEN toggle_song is called with that song's sid
        THEN the song is added and action is 'add'
        """
        # Arrange
        songlist_repo.get_by_out_id.return_value = sample_songlist
        songlist_repo.update.return_value = sample_songlist

        # Act
        result = await service.toggle_song(out_id='20240101001', song_sid='1002001', user_id=1)

        # Assert
        assert result['action'] == 'add'

    async def test_remove_song(self, service, songlist_repo, sample_songlist):
        """
        GIVEN a songlist that already contains the given song
        WHEN toggle_song is called with that song's sid
        THEN the song is removed and action is 'remove'
        """
        # Arrange
        songlist_repo.get_by_out_id.return_value = sample_songlist
        songlist_repo.update.return_value = sample_songlist

        # Act
        result = await service.toggle_song(out_id='20240101001', song_sid='1001001', user_id=1)

        # Assert
        assert result['action'] == 'remove'
