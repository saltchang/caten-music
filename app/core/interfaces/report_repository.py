from typing import Protocol

from app.core.entities.song_report import SongReport


class ReportRepository(Protocol):
    """Repository interface for song problem reports."""

    async def create(self, report: SongReport) -> SongReport: ...
    async def get_by_id(self, report_id: int) -> SongReport | None: ...
    async def list_all(self) -> list[SongReport]: ...
