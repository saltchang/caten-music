from datetime import datetime

from app.core.entities.songlist import SongList
from app.core.entities.user import User
from app.repository.songlist_repository import SqlAlchemySonglistRepository
from app.repository.user_repository import SqlAlchemyUserRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def _create_test_user(session: AsyncSession) -> User:
    repo = SqlAlchemyUserRepository(session)
    return await repo.create(
        User(
            id=0,
            username='songlistowner',
            email='owner@example.com',
            password_hash='hashed_pw',
            displayname='Owner',
            registered_at=datetime(2025, 1, 1, 12, 0, 0),
        )
    )


def _make_songlist(user_id: int) -> SongList:
    return SongList(
        id=0,
        user_id=user_id,
        description='Test songlist',
        songs_sid_list=['s1', 's2'],
        songs_amount=2,
        created_at=datetime(2025, 6, 15, 10, 0, 0),
        updated_at=datetime(2025, 6, 15, 10, 0, 0),
    )


async def test_create_songlist(async_session: AsyncSession):
    """
    GIVEN a valid SongList entity linked to an existing user
    WHEN creating the songlist via the repository
    THEN it should persist and return the songlist with a generated id and out_id
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemySonglistRepository(async_session)
    songlist = _make_songlist(user.id)

    # Act
    created = await repo.create(songlist)

    # Assert
    assert created.id is not None
    assert created.id > 0
    assert created.out_id is not None
    assert created.out_id != ''
    assert created.title is not None
    assert created.user_id == user.id
    assert created.songs_sid_list == ['s1', 's2']
    assert created.songs_amount == 2


async def test_create_songlist_generates_out_id(async_session: AsyncSession):
    """
    GIVEN a songlist with a specific created_at
    WHEN creating the songlist via the repository
    THEN the generated out_id should start with the date portion of created_at
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemySonglistRepository(async_session)
    songlist = _make_songlist(user.id)

    # Act
    created = await repo.create(songlist)

    # Assert
    assert created.out_id is not None
    assert created.out_id.startswith('20250615')


async def test_get_by_out_id(async_session: AsyncSession):
    """
    GIVEN a songlist exists in the database
    WHEN querying by out_id
    THEN it should return the matching songlist
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemySonglistRepository(async_session)
    created = await repo.create(_make_songlist(user.id))
    assert created.out_id is not None

    # Act
    found = await repo.get_by_out_id(created.out_id)

    # Assert
    assert found is not None
    assert found.id == created.id
    assert found.out_id == created.out_id


async def test_get_by_out_id_not_found(async_session: AsyncSession):
    """
    GIVEN no songlist with the given out_id exists
    WHEN querying by out_id
    THEN it should return None
    """
    # Arrange
    repo = SqlAlchemySonglistRepository(async_session)

    # Act
    found = await repo.get_by_out_id('nonexistent')

    # Assert
    assert found is None


async def test_get_by_user_id(async_session: AsyncSession):
    """
    GIVEN two songlists belonging to the same user exist
    WHEN querying by user_id
    THEN it should return both songlists
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemySonglistRepository(async_session)
    await repo.create(_make_songlist(user.id))
    await repo.create(_make_songlist(user.id))

    # Act
    songlists = await repo.get_by_user_id(user.id)

    # Assert
    assert len(songlists) == 2
    for sl in songlists:
        assert sl.user_id == user.id


async def test_get_by_user_id_empty(async_session: AsyncSession):
    """
    GIVEN no songlists exist for the given user_id
    WHEN querying by user_id
    THEN it should return an empty list
    """
    # Arrange
    repo = SqlAlchemySonglistRepository(async_session)

    # Act
    songlists = await repo.get_by_user_id(999)

    # Assert
    assert songlists == []


async def test_update_songlist(async_session: AsyncSession):
    """
    GIVEN a songlist exists in the database
    WHEN updating its title, description, and privacy flag
    THEN the returned entity and a subsequent fetch should reflect the changes

    Note: This test uses a multi-step pattern (update then fetch) to verify persistence.
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemySonglistRepository(async_session)
    created = await repo.create(_make_songlist(user.id))

    # Act
    created.title = 'Updated Title'
    created.description = 'Updated description'
    created.is_private = True
    updated = await repo.update(created)

    # Assert
    assert updated.title == 'Updated Title'
    assert updated.description == 'Updated description'
    assert updated.is_private is True

    assert created.out_id is not None
    fetched = await repo.get_by_out_id(created.out_id)
    assert fetched is not None
    assert fetched.title == 'Updated Title'


async def test_delete_songlist(async_session: AsyncSession):
    """
    GIVEN a songlist exists in the database
    WHEN deleting the songlist by id
    THEN a subsequent fetch by out_id should return None
    """
    # Arrange
    user = await _create_test_user(async_session)
    repo = SqlAlchemySonglistRepository(async_session)
    created = await repo.create(_make_songlist(user.id))
    assert created.out_id is not None

    # Act
    await repo.delete(created.id)

    # Assert
    found = await repo.get_by_out_id(created.out_id)
    assert found is None
