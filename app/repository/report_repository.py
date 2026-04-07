from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities.song_report import SongReport
from app.repository.models.report import SongReportModel


class SqlAlchemyReportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, report: SongReport) -> SongReport:
        model = self._to_model(report)
        self._session.add(model)
        await self._session.flush()
        await self._session.commit()
        return self._to_entity(model)

    async def get_by_id(self, report_id: int) -> SongReport | None:
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
            reported_time=model.reported_time,
        )

    @staticmethod
    def _to_model(report: SongReport) -> SongReportModel:
        return SongReportModel(
            description=report.description,
            song_sid=report.song_sid,
            user_id=report.user_id,
            reported_time=report.reported_time,
        )
