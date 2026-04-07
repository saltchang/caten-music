from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.core.entities.invitation_code import InvitationCode


class InvitationResponse(BaseModel):
    """Response body for invitation code data."""

    id: int
    code: str
    created_by: int
    created_at: datetime
    expires_at: datetime
    is_disabled: bool
    usage_count: int

    @classmethod
    def from_entity(cls, code: InvitationCode) -> InvitationResponse:
        """Build an InvitationResponse from an InvitationCode entity.

        Args:
            code: InvitationCode domain entity.

        Returns:
            An InvitationResponse with all fields mapped.
        """
        return cls(
            id=code.id,
            code=code.code,
            created_by=code.created_by,
            created_at=code.created_at,
            expires_at=code.expires_at,
            is_disabled=code.is_disabled,
            usage_count=code.usage_count,
        )


class InvitationUpdateRequest(BaseModel):
    """Request body for updating an invitation code's status."""

    is_disabled: bool


class InvitationGenerateResponse(BaseModel):
    """Response body for a newly generated invitation code."""

    id: int
    code: str
    expires_at: datetime

    @classmethod
    def from_entity(cls, code: InvitationCode) -> InvitationGenerateResponse:
        """Build an InvitationGenerateResponse from an InvitationCode entity.

        Args:
            code: InvitationCode domain entity.

        Returns:
            An InvitationGenerateResponse with id, code, and expiry.
        """
        return cls(
            id=code.id,
            code=code.code,
            expires_at=code.expires_at,
        )
