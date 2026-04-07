from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.core.entities.song_report import SongReport


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
    reported_at: datetime

    @classmethod
    def from_entity(cls, report: SongReport) -> ReportResponse:
        """Build a ReportResponse from a SongReport entity.

        Args:
            report: SongReport domain entity.

        Returns:
            A ReportResponse with all fields mapped.
        """
        return cls(
            id=report.id,
            description=report.description,
            song_sid=report.song_sid,
            user_id=report.user_id,
            reported_at=report.reported_at,
        )
