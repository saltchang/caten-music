from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities.song_report import SongReport
from app.repository.models.report import SongReportModel


class SqlAlchemyReportRepository:
    """SQLAlchemy repository for SongReport entities backed by PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            session: Async SQLAlchemy session for database operations.
        """
        self._session = session

    async def create(self, report: SongReport) -> SongReport:
        """Persist a new song report.

        Args:
            report: The SongReport entity to create.

        Returns:
            The persisted SongReport with a generated id.
        """
        model = self._to_model(report)
        self._session.add(model)
        await self._session.flush()
        await self._session.commit()
        return self._to_entity(model)

    async def list_all(self) -> list[SongReport]:
        """Fetch all reports ordered by most recent first.

        Returns:
            List of all SongReport entities.
        """
        result = await self._session.execute(select(SongReportModel).order_by(SongReportModel.reported_at.desc()))
        return [self._to_entity(m) for m in result.scalars().all()]

    async def get_by_id(self, report_id: int) -> SongReport | None:
        """Fetch a report by its primary key.

        Args:
            report_id: Primary key of the report.

        Returns:
            The matching SongReport entity, or None if not found.
        """
        result = await self._session.execute(select(SongReportModel).where(SongReportModel.id == report_id))
        model = result.scalars().first()
        if model is None:
            return None
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: SongReportModel) -> SongReport:
        return SongReport(
            id=model.id,
            description=model.description or '',
            song_sid=model.song_sid or '',
            user_id=model.user_id,
            reported_at=model.reported_at,
        )

    @staticmethod
    def _to_model(report: SongReport) -> SongReportModel:
        return SongReportModel(
            description=report.description,
            song_sid=report.song_sid,
            user_id=report.user_id,
            reported_at=report.reported_at,
        )
