from app.core.entities.song_report import SongReport
from app.core.exceptions import InvalidInputError
from app.core.interfaces.report_repository import ReportRepository


class ReportService:
    def __init__(self, report_repo: ReportRepository):
        self._report_repo = report_repo

    async def create_report(self, description: str, song_sid: int, user_id: int) -> SongReport:
        if len(description) < 5:
            raise InvalidInputError('Report description must be at least 5 characters')

        report = SongReport(
            id=0,
            description=description,
            song_sid=song_sid,
            user_id=user_id,
        )
        return await self._report_repo.create(report)
