from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities.user_profile import UserProfile
from app.repository.models.user_profile import UserProfileModel


class SqlAlchemyUserProfileRepository:
    """SQLAlchemy repository for UserProfile entities backed by PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, profile: UserProfile) -> UserProfile:
        """Persist a new user profile.

        Args:
            profile: The UserProfile entity to create.

        Returns:
            The persisted UserProfile with a generated id.
        """
        model = self._to_model(profile)
        self._session.add(model)
        await self._session.flush()
        await self._session.commit()
        return self._to_entity(model)

    async def get_by_user_id(self, user_id: int) -> UserProfile | None:
        """Fetch a user profile by user ID.

        Args:
            user_id: The owning user's primary key.

        Returns:
            The matching UserProfile entity, or None if not found.
        """
        result = await self._session.execute(select(UserProfileModel).where(UserProfileModel.user_id == user_id))
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: UserProfileModel) -> UserProfile:
        return UserProfile(
            id=model.id,
            user_id=model.user_id,
            about_me=model.about_me,
            phone_number=model.phone_number,
            sex=model.sex,
        )

    @staticmethod
    def _to_model(profile: UserProfile) -> UserProfileModel:
        return UserProfileModel(
            user_id=profile.user_id,
            about_me=profile.about_me,
            phone_number=profile.phone_number,
            sex=profile.sex,
        )
