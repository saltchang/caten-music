from unittest.mock import AsyncMock

import pytest
from app.core.entities.user import User
from app.core.enums import UserRole
from app.core.exceptions import UserNotFoundError
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


class TestUpdateUser:
    async def test_update_role_to_admin(self, service, user_repo, sample_user):
        """
        GIVEN an existing user with normal role
        WHEN update_user is called with role=ADMIN
        THEN the user is granted both admin and manager privileges
        """
        # Arrange
        user_repo.get_by_id.return_value = sample_user
        user_repo.update.return_value = sample_user

        # Act
        result = await service.update_user(user_id=1, role=UserRole.ADMIN)

        # Assert
        assert result.is_admin is True
        assert result.is_manager is True

    async def test_update_role_to_manager(self, service, user_repo, sample_user):
        """
        GIVEN an existing user with normal role
        WHEN update_user is called with role=MANAGER
        THEN the user is granted manager but not admin privileges
        """
        # Arrange
        user_repo.get_by_id.return_value = sample_user
        user_repo.update.return_value = sample_user

        # Act
        result = await service.update_user(user_id=1, role=UserRole.MANAGER)

        # Assert
        assert result.is_admin is False
        assert result.is_manager is True

    async def test_update_role_to_normal(self, service, user_repo, sample_user):
        """
        GIVEN an existing user
        WHEN update_user is called with role=NORMAL
        THEN the user has neither admin nor manager privileges
        """
        # Arrange
        user_repo.get_by_id.return_value = sample_user
        user_repo.update.return_value = sample_user

        # Act
        result = await service.update_user(user_id=1, role=UserRole.NORMAL)

        # Assert
        assert result.is_admin is False
        assert result.is_manager is False

    async def test_update_displayname(self, service, user_repo, sample_user):
        """
        GIVEN an existing user
        WHEN update_user is called with a new displayname
        THEN the user's displayname is updated
        """
        # Arrange
        user_repo.get_by_id.return_value = sample_user
        user_repo.update.return_value = sample_user

        # Act
        result = await service.update_user(user_id=1, displayname='NewName')

        # Assert
        assert result.displayname == 'NewName'

    async def test_update_role_and_displayname(self, service, user_repo, sample_user):
        """
        GIVEN an existing user
        WHEN update_user is called with both role and displayname
        THEN both fields are updated in a single operation
        """
        # Arrange
        user_repo.get_by_id.return_value = sample_user
        user_repo.update.return_value = sample_user

        # Act
        result = await service.update_user(user_id=1, role=UserRole.ADMIN, displayname='AdminUser')

        # Assert
        assert result.is_admin is True
        assert result.displayname == 'AdminUser'
        user_repo.update.assert_called_once()

    async def test_update_nonexistent_user(self, service, user_repo):
        """
        GIVEN no user exists with the given id
        WHEN update_user is called
        THEN UserNotFoundError is raised
        """
        # Arrange
        user_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await service.update_user(user_id=999, role=UserRole.ADMIN)
