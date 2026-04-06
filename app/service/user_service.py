from app.core.entities.user import User
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

    async def update_user_role(self, user_id: int, role: str) -> User:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError('User not found')

        if role == 'admin':
            user.is_admin = True
            user.is_manager = True
        elif role == 'manager':
            user.is_admin = False
            user.is_manager = True
        elif role == 'normal':
            user.is_admin = False
            user.is_manager = False
        else:
            raise InvalidInputError(f'Invalid role: {role}')

        return await self._user_repo.update(user)

    async def update_user_displayname(self, user_id: int, displayname: str) -> User:
        if not validate_displayname(displayname):
            raise InvalidInputError('Invalid displayname format')

        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError('User not found')

        user.displayname = displayname
        return await self._user_repo.update(user)
