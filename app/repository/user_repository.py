from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities.user import User
from app.repository.models.user import UserModel


class SqlAlchemyUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_entity(model)

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.username == username))
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_entity(model)

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_entity(model)

    async def create(self, user: User) -> User:
        model = self._to_model(user)
        self._session.add(model)
        await self._session.flush()
        await self._session.commit()
        return self._to_entity(model)

    async def update(self, user: User) -> User:
        result = await self._session.execute(select(UserModel).where(UserModel.id == user.id))
        model = result.scalars().first()
        if model is None:
            raise ValueError(f'User with id {user.id} not found')
        model.username = user.username
        model.email = user.email
        model.password_hash = user.password_hash
        model.displayname = user.displayname
        model.register_time = user.register_time
        model.last_login_time = user.last_login_time
        model.is_authenticated = user.is_authenticated
        model.is_active = user.is_active
        model.is_anonymous = user.is_anonymous
        model.is_admin = user.is_admin
        model.is_manager = user.is_manager
        await self._session.flush()
        await self._session.commit()
        return self._to_entity(model)

    async def exists_username(self, username: str) -> bool:
        result = await self._session.execute(select(UserModel.id).where(UserModel.username == username))
        return result.scalars().first() is not None

    async def exists_email(self, email: str) -> bool:
        result = await self._session.execute(select(UserModel.id).where(UserModel.email == email))
        return result.scalars().first() is not None

    async def list_all(self) -> list[User]:
        result = await self._session.execute(select(UserModel))
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            displayname=model.displayname,
            register_time=model.register_time,
            last_login_time=model.last_login_time,
            is_authenticated=model.is_authenticated,
            is_active=model.is_active,
            is_anonymous=model.is_anonymous,
            is_admin=model.is_admin,
            is_manager=model.is_manager,
        )

    @staticmethod
    def _to_model(user: User) -> UserModel:
        return UserModel(
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            displayname=user.displayname,
            register_time=user.register_time,
            last_login_time=user.last_login_time,
            is_authenticated=user.is_authenticated,
            is_active=user.is_active,
            is_anonymous=user.is_anonymous,
            is_admin=user.is_admin,
            is_manager=user.is_manager,
        )
