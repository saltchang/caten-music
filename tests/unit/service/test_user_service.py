from unittest.mock import AsyncMock

import pytest
from app.core.entities.user import User
from app.core.exceptions import InvalidInputError, UserNotFoundError
from app.service.user_service import UserService


@pytest.fixture
def user_repo():
    return AsyncMock()


@pytest.fixture
def service(user_repo):
    return UserService(user_repo=user_repo)


@pytest.fixture
def sample_user():
    return User(
        id=1,
        username='testuser',
        email='test@example.com',
        password_hash='h',
        displayname='TestUser',
        is_admin=False,
        is_manager=False,
    )


class TestGetUser:
    async def test_get_by_id(self, service, user_repo, sample_user):
        """
        GIVEN an existing user in the repository
        WHEN get_user is called with that user's id
        THEN the user entity is returned
        """
        # Arrange
        user_repo.get_by_id.return_value = sample_user

        # Act
        result = await service.get_user(user_id=1)

        # Assert
        assert result.username == 'testuser'

    async def test_get_nonexistent(self, service, user_repo):
        """
        GIVEN no user exists with the given id
        WHEN get_user is called
        THEN UserNotFoundError is raised
        """
        # Arrange
        user_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await service.get_user(user_id=999)


class TestListUsers:
    async def test_list_all(self, service, user_repo, sample_user):
        """
        GIVEN one user exists in the repository
        WHEN list_users is called
        THEN a list containing that user is returned
        """
        # Arrange
        user_repo.list_all.return_value = [sample_user]

        # Act
        result = await service.list_users()

        # Assert
        assert len(result) == 1


class TestUpdateUserRole:
    async def test_set_admin(self, service, user_repo, sample_user):
        """
        GIVEN an existing user with normal role
        WHEN update_user_role is called with role='admin'
        THEN the user is granted both admin and manager privileges

        NOTE: Arrange mutates the entity and asserts on it before the
        repo update returns, verifying the in-memory state change.
        """
        # Arrange
        user_repo.get_by_id.return_value = sample_user
        user_repo.update.return_value = sample_user

        # Act
        result = await service.update_user_role(user_id=1, role='admin')

        # Assert
        assert result.is_admin is True
        assert result.is_manager is True

    async def test_set_manager(self, service, user_repo, sample_user):
        """
        GIVEN an existing user with normal role
        WHEN update_user_role is called with role='manager'
        THEN the user is granted manager but not admin privileges
        """
        # Arrange
        user_repo.get_by_id.return_value = sample_user
        user_repo.update.return_value = sample_user

        # Act
        result = await service.update_user_role(user_id=1, role='manager')

        # Assert
        assert result.is_admin is False
        assert result.is_manager is True

    async def test_set_normal(self, service, user_repo, sample_user):
        """
        GIVEN an existing user
        WHEN update_user_role is called with role='normal'
        THEN the user has neither admin nor manager privileges
        """
        # Arrange
        user_repo.get_by_id.return_value = sample_user
        user_repo.update.return_value = sample_user

        # Act
        result = await service.update_user_role(user_id=1, role='normal')

        # Assert
        assert result.is_admin is False
        assert result.is_manager is False

    async def test_invalid_role(self, service, user_repo, sample_user):
        """
        GIVEN an existing user
        WHEN update_user_role is called with an unrecognized role
        THEN InvalidInputError is raised
        """
        # Arrange
        user_repo.get_by_id.return_value = sample_user

        # Act & Assert
        with pytest.raises(InvalidInputError):
            await service.update_user_role(user_id=1, role='superuser')

    async def test_update_displayname(self, service, user_repo, sample_user):
        """
        GIVEN an existing user
        WHEN update_user_displayname is called with a new name
        THEN the user's displayname is updated
        """
        # Arrange
        user_repo.get_by_id.return_value = sample_user
        user_repo.update.return_value = sample_user

        # Act
        result = await service.update_user_displayname(user_id=1, displayname='NewName')

        # Assert
        assert result.displayname == 'NewName'
