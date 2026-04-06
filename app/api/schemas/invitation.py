from datetime import datetime

from pydantic import BaseModel


class InvitationResponse(BaseModel):
    id: int
    code: str
    created_by: int
    created_at: datetime
    expires_at: datetime
    is_disabled: bool
    usage_count: int


class InvitationToggleRequest(BaseModel):
    is_disabled: bool


class InvitationGenerateResponse(BaseModel):
    id: int
    code: str
    expires_at: datetime
