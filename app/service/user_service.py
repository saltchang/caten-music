from app.core.entities.user import User
from app.core.enums import UserRole
from app.core.exceptions import InvalidInputError, UserNotFoundError
from app.core.interfaces.user_repository import UserRepository
from app.core.validators import validate_displayname


class UserService:
    """Admin-facing user management operations."""

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def get_user(self, user_id: int) -> User:
        """Fetch a user by ID.

        Args:
            user_id: Primary key of the user.

        Returns:
            The User entity.

        Raises:
            UserNotFoundError: If user does not exist.
        """
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError('User not found')
        return user

    async def list_users(self) -> list[User]:
        """Fetch all users.

        Returns:
            List of all User entities.
        """
        return await self._user_repo.list_all()

    async def update_user(
        self,
        user_id: int,
        role: UserRole | None = None,
        displayname: str | None = None,
    ) -> User:
        """Update a user's role and/or displayname in a single operation.

        Args:
            user_id: Target user ID.
            role: New role to assign (optional).
            displayname: New display name (optional).

        Returns:
            Updated User entity.

        Raises:
            UserNotFoundError: If user does not exist.
            InvalidInputError: If displayname format is invalid.
        """
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError('User not found')

        if role is not None:
            if role == UserRole.ADMIN:
                user.is_admin = True
                user.is_manager = True
            elif role == UserRole.MANAGER:
                user.is_admin = False
                user.is_manager = True
            else:
                user.is_admin = False
                user.is_manager = False

        if displayname is not None:
            if not validate_displayname(displayname):
                raise InvalidInputError('Invalid displayname format')
            user.displayname = displayname

        return await self._user_repo.update(user)
