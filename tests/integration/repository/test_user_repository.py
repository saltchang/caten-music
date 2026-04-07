from datetime import datetime

from app.core.entities.user import User
from app.repository.user_repository import SqlAlchemyUserRepository
from sqlalchemy.ext.asyncio import AsyncSession


def _make_user(
    username: str = 'testuser',
    email: str = 'test@example.com',
    displayname: str = 'Test User',
) -> User:
    return User(
        id=0,
        username=username,
        email=email,
        password_hash='hashed_pw',
        displayname=displayname,
        registered_at=datetime(2025, 1, 1, 12, 0, 0),
    )


async def test_create_user(async_session: AsyncSession):
    """
    GIVEN a valid User entity
    WHEN creating the user via the repository
    THEN it should persist and return the user with a generated id and default flags
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)
    user = _make_user()

    # Act
    created = await repo.create(user)

    # Assert
    assert created.id is not None
    assert created.id > 0
    assert created.username == 'testuser'
    assert created.email == 'test@example.com'
    assert created.displayname == 'Test User'
    assert created.password_hash == 'hashed_pw'
    assert created.is_active is True
    assert created.is_admin is False


async def test_get_by_username(async_session: AsyncSession):
    """
    GIVEN a user exists in the database
    WHEN querying by username
    THEN it should return the matching user
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)
    await repo.create(_make_user())

    # Act
    found = await repo.get_by_username('testuser')

    # Assert
    assert found is not None
    assert found.username == 'testuser'


async def test_get_by_username_not_found(async_session: AsyncSession):
    """
    GIVEN no user with the given username exists
    WHEN querying by username
    THEN it should return None
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)

    # Act
    found = await repo.get_by_username('nonexistent')

    # Assert
    assert found is None


async def test_get_by_email(async_session: AsyncSession):
    """
    GIVEN a user exists in the database
    WHEN querying by email
    THEN it should return the matching user
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)
    await repo.create(_make_user())

    # Act
    found = await repo.get_by_email('test@example.com')

    # Assert
    assert found is not None
    assert found.email == 'test@example.com'


async def test_get_by_email_not_found(async_session: AsyncSession):
    """
    GIVEN no user with the given email exists
    WHEN querying by email
    THEN it should return None
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)

    # Act
    found = await repo.get_by_email('nonexistent@example.com')

    # Assert
    assert found is None


async def test_get_by_id(async_session: AsyncSession):
    """
    GIVEN a user exists in the database
    WHEN querying by id
    THEN it should return the matching user
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)
    created = await repo.create(_make_user())

    # Act
    found = await repo.get_by_id(created.id)

    # Assert
    assert found is not None
    assert found.id == created.id
    assert found.username == 'testuser'


async def test_get_by_id_not_found(async_session: AsyncSession):
    """
    GIVEN no user with the given id exists
    WHEN querying by id
    THEN it should return None
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)

    # Act
    found = await repo.get_by_id(999)

    # Assert
    assert found is None


async def test_exists_username_true(async_session: AsyncSession):
    """
    GIVEN a user with the given username exists
    WHEN checking if the username exists
    THEN it should return True
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)
    await repo.create(_make_user())

    # Act & Assert
    assert await repo.exists_username('testuser') is True


async def test_exists_username_false(async_session: AsyncSession):
    """
    GIVEN no user with the given username exists
    WHEN checking if the username exists
    THEN it should return False
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)

    # Act & Assert
    assert await repo.exists_username('nonexistent') is False


async def test_exists_email_true(async_session: AsyncSession):
    """
    GIVEN a user with the given email exists
    WHEN checking if the email exists
    THEN it should return True
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)
    await repo.create(_make_user())

    # Act & Assert
    assert await repo.exists_email('test@example.com') is True


async def test_exists_email_false(async_session: AsyncSession):
    """
    GIVEN no user with the given email exists
    WHEN checking if the email exists
    THEN it should return False
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)

    # Act & Assert
    assert await repo.exists_email('nonexistent@example.com') is False


async def test_update_user(async_session: AsyncSession):
    """
    GIVEN a user exists in the database
    WHEN updating its displayname and is_admin flag
    THEN the returned entity and a subsequent fetch should reflect the changes
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)
    created = await repo.create(_make_user())

    # Act
    created.displayname = 'Updated Name'
    created.is_admin = True
    updated = await repo.update(created)

    # Assert
    assert updated.displayname == 'Updated Name'
    assert updated.is_admin is True

    fetched = await repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.displayname == 'Updated Name'
    assert fetched.is_admin is True


async def test_list_all(async_session: AsyncSession):
    """
    GIVEN two users exist in the database
    WHEN listing all users
    THEN it should return both users
    """
    # Arrange
    repo = SqlAlchemyUserRepository(async_session)
    await repo.create(_make_user(username='user1', email='u1@example.com'))
    await repo.create(_make_user(username='user2', email='u2@example.com'))

    # Act
    users = await repo.list_all()

    # Assert
    assert len(users) == 2
    usernames = {u.username for u in users}
    assert usernames == {'user1', 'user2'}
