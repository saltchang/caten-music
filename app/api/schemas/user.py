from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from app.core.enums import UserRole

if TYPE_CHECKING:
    from app.core.entities.user import User


class UserResponse(BaseModel):
    """Response body for user data."""

    id: int
    username: str
    email: str
    displayname: str
    is_admin: bool
    is_manager: bool
    is_active: bool
    is_authenticated: bool

    @classmethod
    def from_entity(cls, user: User) -> UserResponse:
        """Build a UserResponse from a User entity.

        Args:
            user: User domain entity.

        Returns:
            A UserResponse with all fields mapped.
        """
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            displayname=user.displayname,
            is_admin=user.is_admin,
            is_manager=user.is_manager,
            is_active=user.is_active,
            is_authenticated=user.is_authenticated,
        )


class UserUpdateRequest(BaseModel):
    displayname: str | None = None
    role: UserRole | None = None
