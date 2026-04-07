from app.core.entities.song_report import SongReport
from app.core.exceptions import InvalidInputError
from app.core.interfaces.report_repository import ReportRepository


class ReportService:
    """Manages song issue reports submitted by users."""

    def __init__(self, report_repo: ReportRepository):
        self._report_repo = report_repo

    async def list_reports(self) -> list[SongReport]:
        """List all reports.

        Returns:
            List of all SongReport entities.
        """
        return await self._report_repo.list_all()

    async def create_report(self, description: str, song_sid: str, user_id: int) -> SongReport:
        """Submit a song problem report.

        Args:
            description: Issue description (minimum 5 characters).
            song_sid: SID of the song being reported.
            user_id: ID of the reporting user.

        Returns:
            The created SongReport entity.

        Raises:
            InvalidInputError: If description is shorter than 5 characters.
        """
        if len(description) < 5:
            raise InvalidInputError('Report description must be at least 5 characters')

        report = SongReport(
            id=0,
            description=description,
            song_sid=song_sid,
            user_id=user_id,
        )
        return await self._report_repo.create(report)
