from typing import Protocol

from app.core.entities.user_profile import UserProfile


class UserProfileRepository(Protocol):
    async def create(self, profile: UserProfile) -> UserProfile: ...
    async def get_by_user_id(self, user_id: int) -> UserProfile | None: ...
