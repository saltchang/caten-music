from datetime import datetime

from pydantic import BaseModel


class ReportCreateRequest(BaseModel):
    """Request body for creating a song problem report."""

    description: str
    song_sid: str


class ReportResponse(BaseModel):
    """Response body for a song problem report."""

    id: int
    description: str
    song_sid: str
    user_id: int
    reported_time: datetime
