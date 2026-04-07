from app.core.entities.user import User
from app.core.enums import UserRole
from app.core.exceptions import InvalidInputError, UserNotFoundError
from app.core.interfaces.user_repository import UserRepository
from app.core.validators import validate_displayname


class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def get_user(self, user_id: int) -> User:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError('User not found')
        return user

    async def list_users(self) -> list[User]:
        return await self._user_repo.list_all()

    async def update_user_role(self, user_id: int, role: UserRole) -> User:
        """Update a user's role.

        Args:
            user_id: Target user ID.
            role: New role to assign.

        Returns:
            Updated User entity.

        Raises:
            UserNotFoundError: If user does not exist.
        """
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError('User not found')

        if role == UserRole.ADMIN:
            user.is_admin = True
            user.is_manager = True
        elif role == UserRole.MANAGER:
            user.is_admin = False
            user.is_manager = True
        else:
            user.is_admin = False
            user.is_manager = False

        return await self._user_repo.update(user)

    async def update_user_displayname(self, user_id: int, displayname: str) -> User:
        if not validate_displayname(displayname):
            raise InvalidInputError('Invalid displayname format')

        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError('User not found')

        user.displayname = displayname
        return await self._user_repo.update(user)
